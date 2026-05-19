"""
Document Management Agent
=========================
Agente experto en normativa ISO 9001 y Gestión Documental.
Autogenera la pirámide documental basada en el proceso AS-IS.
"""

from __future__ import annotations

import json
import logging
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.models.document_management import DocumentManagementModel
from app.models.process_case import ProcessCaseModel
from app.services.llm_client_service import LLMClientService
from app.services.llm_router_service import AgentTask

logger = logging.getLogger(__name__)

DOC_AGENT_PROMPT = """Eres un Agente experto en Gestión Documental y Sistemas de Gestión de Calidad (ISO 9001).
Tu objetivo es redactar documentos oficiales corporativos basándote en la información del proceso.

La pirámide documental exige:
1. Política (Nivel Estratégico): Directrices generales, compromiso de la dirección.
2. Procedimiento (Nivel Táctico): Qué se hace, quién lo hace, cuándo.
3. Instructivo (Nivel Operativo): Paso a paso detallado de una tarea específica.
4. Formato/Registro (Nivel Evidencia): Plantilla estructurada para recolectar datos.

REGLAS DE REDACCIÓN:
- Usa un lenguaje formal, claro e imperativo.
- Organiza el contenido estructurado en Markdown.
- Para el formato/registro, devuelve una tabla Markdown que sirva como plantilla.
- Siempre devuelve la respuesta en JSON válido con la siguiente estructura estricta:
{
  "code": "COD-PRO-001",
  "title": "Título del Documento",
  "objective": "Objetivo principal",
  "scope": "Alcance del documento",
  "responsibilities": "Responsables clave",
  "content": "El contenido detallado en formato Markdown..."
}
NO DEVUELVAS NADA FUERA DEL JSON.
"""

class DocumentManagementAgent:
    def __init__(self, db: Session) -> None:
        self.db = db
        self._llm = LLMClientService()

    def generar_documento(
        self,
        case_id: str | UUID,
        doc_type: str,
        contexto_proceso: str,
        tema_especifico: str = ""
    ) -> DocumentManagementModel:
        """
        Genera un documento estructurado ISO usando el LLM.
        doc_type puede ser: 'policy', 'procedure', 'instruction', 'format_record'
        """
        case = self.db.get(ProcessCaseModel, str(case_id))
        if not case:
            raise ValueError(f"Caso {case_id} no encontrado")

        nombres_tipo = {
            "policy": "Política Corporativa",
            "procedure": "Procedimiento Operativo Estandar",
            "instruction": "Instructivo de Trabajo",
            "format_record": "Formato de Registro"
        }

        user_message = (
            f"Por favor, genera un documento de tipo '{nombres_tipo.get(doc_type, doc_type)}' "
            f"para el proceso '{case.name}'.\n\n"
        )
        if tema_especifico:
            user_message += f"Enfócate específicamente en: {tema_especifico}\n\n"
            
        user_message += (
            f"Contexto del Proceso AS-IS / Información base:\n"
            f"{contexto_proceso}\n\n"
            "Genera el JSON estructurado."
        )

        response = self._llm.completar(
            system_prompt=DOC_AGENT_PROMPT,
            user_message=user_message,
            tarea=AgentTask.as_is,
        )

        if not response.success:
            raise RuntimeError(f"Fallo del LLM al generar documento: {response.error}")

        try:
            # Extraer el JSON (ignorar cualquier texto alrededor, ej. bloques markdown de código)
            text = response.content.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
                
            data = json.loads(text.strip())
        except Exception as e:
            logger.error(f"Fallo al parsear JSON del documento: {e}\nContent: {response.content}")
            raise ValueError("El LLM no devolvió un JSON válido") from e

        doc = DocumentManagementModel(
            id=str(uuid4()),
            case_id=str(case.id),
            doc_type=doc_type,
            code=data.get("code", "DOC-001"),
            title=data.get("title", f"Documento de {case.name}"),
            objective=data.get("objective"),
            scope=data.get("scope"),
            responsibilities=data.get("responsibilities"),
            content=data.get("content", ""),
            status="draft",
            created_by="Agente Gestión Documental"
        )
        
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc
