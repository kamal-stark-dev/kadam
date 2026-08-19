"""
SQLAlchemy models for Kadam.

Updated to match the richer rules schema (id/certificate_type split,
structured prerequisites/documents/rejection reasons). See data/rules.json
and docs/rules-schema.md for the canonical shape.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    display_name = Column(String, nullable=False)
    preferred_language = Column(String, default="en")

    cases = relationship("Case", back_populates="user")


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    life_event = Column(String, nullable=False)  # e.g. "death"
    status = Column(String, nullable=False, default="DRAFT")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="cases")
    sub_cases = relationship("SubCase", back_populates="case", order_by="SubCase.id")
    timeline_events = relationship("TimelineEvent", back_populates="case")


class SubCase(Base):
    __tablename__ = "sub_cases"

    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    rule_id = Column(String, ForeignKey("rules.rule_id"), nullable=False)  # e.g. "death__legal_heir_certificate"
    status = Column(String, nullable=False, default="LOCKED")
    depends_on_sub_case_id = Column(Integer, ForeignKey("sub_cases.id"), nullable=True)
    unlocked_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)

    case = relationship("Case", back_populates="sub_cases")
    documents = relationship("Document", back_populates="sub_case")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    sub_case_id = Column(Integer, ForeignKey("sub_cases.id"), nullable=False)
    doc_id = Column(String, nullable=False)  # matches required_documents[].id in the rule
    filename = Column(String, nullable=False)
    validated = Column(Boolean, default=False)
    validation_notes = Column(Text, nullable=True)

    sub_case = relationship("SubCase", back_populates="documents")


class Rule(Base):
    """
    Mirrors one entry in data/rules.json. Loaded/synced at startup via
    scripts/seed_rules.py — never hand-edited through the API.

    rule_id is globally unique and scoped to the life event
    (e.g. "death__property_mutation" vs "property_transfer__property_mutation"),
    while certificate_type is the shared label used for display/grouping.
    """

    __tablename__ = "rules"

    id = Column(Integer, primary_key=True)
    rule_id = Column(String, unique=True, nullable=False)          # e.g. "death__legal_heir_certificate"
    certificate_type = Column(String, nullable=False)               # e.g. "legal_heir_certificate"
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    life_event = Column(String, nullable=False)                     # e.g. "death"
    department = Column(String, nullable=False)                     # must start with "[SAMPLE]"
    office = Column(String, nullable=False)                         # must start with "[SAMPLE]"

    prerequisites_json = Column(Text, nullable=False, default="[]")       # [{"rule_id": "...", "reason": "..."}]
    required_documents_json = Column(Text, nullable=False)                 # [{"id","name","required","source_rule"}]
    outputs_json = Column(Text, nullable=False)                            # [{"id","name","type"}]
    enables_json = Column(Text, nullable=False, default="[]")              # ["rule_id", ...] — forward pointers

    avg_days = Column(Integer, nullable=False)                      # numeric, for ETA math
    estimated_processing_time_display = Column(String, nullable=False)  # e.g. "7-15 working days"

    common_rejection_reasons_json = Column(Text, nullable=False, default="[]")
    next_step = Column(Text, nullable=True)
    citizen_guidance = Column(Text, nullable=True)


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    sub_case_id = Column(Integer, ForeignKey("sub_cases.id"), nullable=True)
    event_type = Column(String, nullable=False)  # e.g. "STATE_CHANGE", "AI_INFERENCE"
    payload_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="timeline_events")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    channel = Column(String, nullable=False)  # "sms" | "whatsapp" | "email" | "in_app"
    message = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    mock = Column(Boolean, default=True)


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True)
    actor = Column(String, nullable=False)  # "system" | "ai" | "user:<id>"
    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    payload_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
