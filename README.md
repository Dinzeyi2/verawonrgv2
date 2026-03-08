# Legal-to-Go — Backend API

AI-powered divorce filing & life-transition document generator.

## What it does

1. **AI Interview** — Claude conducts a conversational intake (~10 min)
2. **Document Generation** — Generates a complete packet of PDFs:
   - Divorce Petition (all 50 states)
   - Name Change Packet (SSA, DMV, Passport)
   - Asset Transfer Letters (banks, QDRO notice, property)
   - Co-Parenting Plan (if children)
   - Financial Reset Guide (W-4, beneficiary audit, budget)
3. **Payment** — Stripe checkout at $199
4. **Download** — User downloads zip of all PDFs

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy and fill in env vars
cp .env.example .env

# Initialize database
python init_db.py

# Run locally
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/session/create` | Start a new session |
| GET | `/api/session/{id}` | Get session state |
| POST | `/api/intake/start` | Begin the AI interview |
| POST | `/api/intake/message` | Send interview message |
| GET | `/api/intake/{id}/summary` | Get collected data |
| POST | `/api/payment/checkout` | Create Stripe checkout |
| POST | `/api/payment/webhook` | Stripe webhook handler |
| GET | `/api/payment/status/{id}` | Check payment status |
| POST | `/api/documents/generate` | Trigger doc generation |
| GET | `/api/documents/status/{id}` | Check generation status |
| GET | `/api/documents/download/{id}` | Download zip packet |

## Deploy to Railway

1. Push to GitHub
2. Connect repo in Railway dashboard
3. Add environment variables in Railway settings
4. Railway auto-deploys on push

## Frontend (Lovable.dev) Integration

The typical user flow:

```
1. POST /api/session/create → get session_id
2. POST /api/intake/start → get first AI message
3. Loop: POST /api/intake/message → show reply, check is_complete
4. When is_complete=true → show summary, redirect to payment
5. POST /api/payment/checkout → redirect to Stripe URL
6. On success: POST /api/documents/generate
7. Poll GET /api/documents/status until ready=true
8. Show download button → GET /api/documents/download
```

## Stripe Webhook Setup

In Stripe Dashboard → Webhooks → Add endpoint:
- URL: `https://your-railway-app.up.railway.app/api/payment/webhook`
- Events: `checkout.session.completed`

## Notes on UPL (Unauthorized Practice of Law)

This is a **document preparation service**, not legal advice.
- Users review and submit forms themselves
- All documents include legal disclaimer
- Not a law firm, not providing legal counsel
- Same model as LegalZoom, Rocket Lawyer
