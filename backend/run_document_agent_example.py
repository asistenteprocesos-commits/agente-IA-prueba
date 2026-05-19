import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.db.session import SessionLocal
from app.models.process_case import ProcessCaseModel
from app.services.document_management_agent import DocumentManagementAgent
from app.core.config import settings

def main():
    print("=" * 60)
    print("EJEMPLO: Agentes IA redactando Pirámide Documental ISO 9001")
    print("=" * 60)
    
    db = SessionLocal()
    
    # 1. Crear un caso de prueba
    print("\n1. Creando/Buscando caso de proceso de prueba...")
    case = db.query(ProcessCaseModel).filter_by(name="Proceso de Reclutamiento de Personal").first()
    if not case:
        import uuid
        case = ProcessCaseModel(
            id=str(uuid.uuid4()),
            name="Proceso de Reclutamiento de Personal",
            area="Recursos Humanos",
            objective="Asegurar la contratación de talento calificado y alineado a la cultura.",
            status="analysis"
        )
        db.add(case)
        db.commit()
    print(f"Caso seleccionado: {case.name}")

    contexto_proceso = """
    El proceso de reclutamiento inicia cuando un líder de área emite una 'Solicitud de Personal'. 
    Recursos Humanos (RRHH) evalúa el presupuesto. Si está aprobado, se publica la vacante en LinkedIn y Computrabajo. 
    RRHH filtra las hojas de vida y hace una primera entrevista de filtro cultural. 
    Los candidatos seleccionados pasan a una entrevista técnica con el líder del área. 
    Si el líder aprueba, se hace un estudio de seguridad. Si el candidato pasa, se le hace una oferta formal. 
    Finalmente, el candidato firma contrato y se inicia el Onboarding.
    """
    
    print("\n2. Inicializando Agente de Gestión Documental...")
    agent = DocumentManagementAgent(db)

    # Limpiar documentos previos para que no haya conflicto de UNIQUE code
    from app.models.document_management import DocumentManagementModel
    db.query(DocumentManagementModel).filter(DocumentManagementModel.case_id == str(case.id)).delete()
    db.commit()

    # =========================================================================
    # INYECCIÓN DE DATOS FICTICIOS (MOCK) PARA EVITAR LLAMADAS A LA API / LLM
    # =========================================================================
    from app.services.llm_client_service import LLMResponse

    def mock_completar(*args, **kwargs):
        # Según el tipo de documento solicitado en el prompt, devolvemos un JSON distinto.
        prompt = kwargs.get('user_message', '')
        if "Política Corporativa" in prompt:
            content = '''{
                "code": "POL-RH-001",
                "title": "Política de Selección y Contratación",
                "objective": "Garantizar la igualdad de oportunidades y la contratación de talento calificado.",
                "scope": "Aplica a todos los procesos de contratación de la empresa.",
                "responsibilities": "Dirección de Recursos Humanos y Líderes de Área.",
                "content": "# Política de Selección\\n1. No discriminación.\\n2. Transparencia en ofertas.\\n3. Evaluación basada en méritos."
            }'''
        elif "Procedimiento Operativo" in prompt:
            content = '''{
                "code": "PRO-RH-001",
                "title": "Procedimiento de Reclutamiento",
                "objective": "Estandarizar los pasos para cubrir una vacante.",
                "scope": "Desde la solicitud hasta el onboarding.",
                "responsibilities": "Analista de Selección.",
                "content": "# Pasos\\n1. Solicitud.\\n2. Aprobación.\\n3. Publicación.\\n4. Entrevistas.\\n5. Contratación."
            }'''
        elif "Instructivo" in prompt:
            content = '''{
                "code": "INS-RH-001",
                "title": "Instructivo de Publicación en LinkedIn",
                "objective": "Paso a paso para crear una vacante en LinkedIn.",
                "scope": "Uso exclusivo del equipo de Atracción de Talento.",
                "responsibilities": "Reclutador.",
                "content": "# Instrucciones\\n1. Iniciar sesión en LinkedIn Recruiter.\\n2. Clic en 'Publicar Empleo'.\\n3. Llenar los campos obligatorios.\\n4. Activar filtros de pre-selección."
            }'''
        else:
            content = '''{
                "code": "FOR-RH-001",
                "title": "Formato de Entrevista de Filtro Cultural",
                "objective": "Registrar la evaluación de alineación cultural del candidato.",
                "scope": "Primera entrevista RRHH.",
                "responsibilities": "Analista de Selección.",
                "content": "| Criterio | Calificación | Observaciones |\\n|---|---|---|\\n| Trabajo en equipo | | |\\n| Adaptabilidad | | |\\n| Comunicación | | |"
            }'''

        return LLMResponse(
            content=content,
            provider="Mock-Provider",
            model="mock-model",
            tokens_used=60,
            error=None
        )

    # Sobrescribir el método real por nuestro Mock
    agent._llm.completar = mock_completar
    print("[MOCK] Se ha inyectado un LLM falso para pruebas offline.")
    # =========================================================================

    
    try:
        # A. Política
        print("\n[Agente] Generando Política Corporativa (Nivel 1)...")
        doc_policy = agent.generar_documento(
            case.id, 
            "policy", 
            contexto_proceso,
            "Política general de selección, no discriminación y tiempos de respuesta."
        )
        print(f"✔ Documento creado: {doc_policy.code} - {doc_policy.title}")
        print(f"  Objetivo: {doc_policy.objective[:100]}...")
        
        # B. Procedimiento
        print("\n[Agente] Generando Procedimiento (Nivel 2)...")
        doc_proc = agent.generar_documento(
            case.id, 
            "procedure", 
            contexto_proceso,
            "Descripción paso a paso del reclutamiento desde la vacante hasta el onboarding."
        )
        print(f"[OK] Documento creado: {doc_proc.code} - {doc_proc.title}")
        print(f"  Alcance: {doc_proc.scope[:100]}...")
        
        # C. Instructivo
        print("\n[Agente] Generando Instructivo de Trabajo (Nivel 3)...")
        doc_inst = agent.generar_documento(
            case.id, 
            "instruction", 
            contexto_proceso,
            "Paso a paso exacto para publicar la vacante en LinkedIn y realizar el primer filtro cultural."
        )
        print(f"✔ Documento creado: {doc_inst.code} - {doc_inst.title}")
        
        # D. Formato
        print("\n[Agente] Generando Plantilla/Formato (Nivel 4)...")
        doc_format = agent.generar_documento(
            case.id, 
            "format_record", 
            contexto_proceso,
            "Formato tabular estructurado para evaluar a un candidato en la entrevista de filtro cultural."
        )
        print(f"✔ Documento creado: {doc_format.code} - {doc_format.title}")
        
        print("\n" + "=" * 60)
        print("EJEMPLO DE CONTENIDO GENERADO (Formato de Filtro Cultural):")
        print("=" * 60)
        print(doc_format.content)

    except Exception as e:
        print(f"\n[ERROR] al ejecutar el agente: {e}")
        print("Nota: Asegurate de tener configurado tu API KEY en backend/.env o tener Ollama corriendo.")

if __name__ == "__main__":
    main()
