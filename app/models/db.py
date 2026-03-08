from sqlalchemy import Column, String, JSON, Boolean, DateTime, Integer, Text, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    state = Column(String, nullable=False)          # US state
    county = Column(String, nullable=True)
    case_type = Column(String, default="divorce")   # divorce | small_claims
    data = Column(JSON, default={})                 # all collected user data
    conversation = Column(JSON, default=[])         # chat history
    stage = Column(String, default="intro")         # intro | interview | review | payment | complete
    paid = Column(Boolean, default=False)
    stripe_session_id = Column(String, nullable=True)
    stripe_payment_intent = Column(String, nullable=True)
    packet_path = Column(String, nullable=True)     # generated packet file path
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class CourtForm(Base):
    """
    Cached court forms fetched from official government websites.
    On first request: fetched live, stored here.
    On subsequent requests: served from DB (fallback if URL goes down).
    """
    __tablename__ = "court_forms"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    feature = Column(String, nullable=False)        # e.g. "01_divorce", "02_name_change"
    state = Column(String, nullable=False)          # e.g. "Georgia", "_FEDERAL"
    filename = Column(String, nullable=False)        # e.g. "GA_divorce_petition.pdf"
    source_url = Column(String, nullable=False)      # official government URL
    pdf_data = Column(LargeBinary, nullable=True)    # raw PDF bytes cached in DB
    file_size_kb = Column(Integer, nullable=True)
    fetch_status = Column(String, default="pending") # pending | cached | failed
    last_fetched = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class GeneratedPacket(Base):
    __tablename__ = "generated_packets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    document_types = Column(JSON, default=[])       # list of doc types included
    created_at = Column(DateTime, server_default=func.now())
