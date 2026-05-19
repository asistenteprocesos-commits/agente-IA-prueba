from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DocumentManagementModel(Base):
    """
    Gestión Documental del Proceso (ISO 9001 / Pirámide Documental).
    - Nivel 1: Manuales / Políticas (policy)
    - Nivel 2: Procedimientos / Procesos (procedure)
    - Nivel 3: Instructivos de Trabajo (instruction)
    - Nivel 4: Formatos / Registros (format_record)
    """
    __tablename__ = "document_management"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    case_id: Mapped[str] = mapped_column(
        ForeignKey("process_cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    doc_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True) # policy, procedure, instruction, format_record
    code: Mapped[str] = mapped_column(String(40), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    version: Mapped[str] = mapped_column(String(20), default="1.0", nullable=False)
    
    # ISO 9001 Metadata
    objective: Mapped[str | None] = mapped_column(Text)
    scope: Mapped[str | None] = mapped_column(Text)
    responsibilities: Mapped[str | None] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    status: Mapped[str] = mapped_column(String(40), default="draft") # draft, in_review, approved, obsolete
    created_by: Mapped[str] = mapped_column(String(120), default="Agent IA")
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    process_case: Mapped["ProcessCaseModel"] = relationship()
