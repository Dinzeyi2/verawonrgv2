from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import intake, documents, session
from app.core.config import settings

app = FastAPI(
    title="Legal-to-Go API",
    description="AI-powered divorce filing & life transition document generator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session.router, prefix="/api/session", tags=["Session"])
app.include_router(intake.router, prefix="/api/intake", tags=["Intake"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(payment.router, prefix="/api/payment", tags=["Payment"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "legal-to-go"}
