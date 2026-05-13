from datetime import UTC, datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ProcessCaseModel(Base):
    __tablename__ = "process_cases"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    area: Mapped[str | None] = mapped_column(String(120))
    objective: Mapped[str | None] = mapped_column(String(500))
    scope: Mapped[str | None] = mapped_column(Text)
    owner: Mapped[str | None] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
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

    repository: Mapped["ProcessRepositoryModel"] = relationship(
        back_populates="process_case",
        cascade="all, delete-orphan",
        uselist=False,
    )
    stakeholders: Mapped[list["ProcessStakeholderModel"]] = relationship(
        back_populates="process_case",
        cascade="all, delete-orphan",
    )
    interviews: Mapped[list["ProcessInterviewModel"]] = relationship(
        back_populates="process_case",
        cascade="all, delete-orphan",
    )
    as_is_elements: Mapped[list["ProcessAsIsElementModel"]] = relationship(
        back_populates="process_case",
        cascade="all, delete-orphan",
    )
    orchestration_run: Mapped["OrchestrationRunModel"] = relationship(
        back_populates="process_case",
        cascade="all, delete-orphan",
        uselist=False,
    )
