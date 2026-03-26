from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.base import Base
from enums import SeniorityLevel


class CandidateSeniority(Base):
    __tablename__ = "candidate_seniority"

    seniority_id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidate_profile.candidate_id", ondelete="CASCADE")
    )
    level: Mapped[SeniorityLevel] = mapped_column(Enum(SeniorityLevel))

    candidate: Mapped["CandidateProfile"] = relationship(
        back_populates="seniority", uselist=False
    )
