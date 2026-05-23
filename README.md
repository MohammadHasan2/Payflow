# Payflow Backend

Payment gateway API built with FastAPI and Stripe.

## Setup

1. Clone the repo:
```bash
git clone https://github.com/YOUR_USERNAME/payflow-backend.git
cd payflow-backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Update `.env` with your values:
- `STRIPE_SECRET_KEY`: Your Stripe test key
- `SECRET_KEY`: Generate a secure key
- `DOMAIN`: Your domain

6. Run the server:
```bash
uvicorn app.main:app --reload
```

Server runs at `http://localhost:8000`

## Docker

```bash
docker-compose up
```

## Deployment

Deploy on Render:
1. Connect your GitHub repo
2. Add environment variables in Render dashboard
3. Deploy

## API Endpoints

- `GET /` - Health check
- `POST /merchants` - Create merchant
- `POST /payments` - Create payment

See `app/routes/` for full API documentation.
