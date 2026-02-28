<<<<<<< HEAD
# Ullas Student WhatsApp Chatbot — Middleware Layer

A lightweight Python (Flask) middleware that receives WhatsApp messages via the Meta
Cloud API, authenticates students with OTP, and responds with formatted menu-driven
query results.

> **Note:** This version uses **mock data** (no Oracle DB connection). Replace
> `mock_data.py` with real DB queries when ready.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill in your env file
copy .env.example .env          # Windows
# cp .env.example .env          # Linux/Mac

# 3. Start the server
python app.py
```

The server starts on `http://localhost:5000`.

---

## Endpoints

| Route       | Method | Purpose                              |
|-------------|--------|--------------------------------------|
| `/health`   | GET    | Health check → `{"status": "ok"}`    |
| `/webhook`  | GET    | Meta webhook verification handshake  |
| `/webhook`  | POST   | Receive incoming WhatsApp messages   |

---

## Connecting to WhatsApp

1. Create a **Meta Business App** at https://developers.facebook.com
2. Enable the **WhatsApp** product
3. Get your **Temporary Access Token** and **Phone Number ID** from the API Setup page
4. Set them in your `.env` file
5. Expose your local server with [ngrok](https://ngrok.com):
   ```bash
   ngrok http 5000
   ```
6. In Meta Dashboard → WhatsApp → Configuration → set the **Callback URL** to:
   ```
   https://<your-ngrok-id>.ngrok-free.app/webhook
   ```
   Set **Verify Token** to the same value as `VERIFY_TOKEN` in your `.env`

---

## Mock Data / Test Students

| Ullas ID             | Phone          | Scenarios                              |
|----------------------|----------------|----------------------------------------|
| UL-09-2026-00456     | 919876543210   | Verified, centre allocated, 75% att.   |
| UL-10-2025-00789     | 919876543211   | Rejected, no centre, 25% att., failed  |
| UL-11-2024-01023     | 919876543212   | Verified, centre allocated, 100% att.  |

---

## Conversation Flow

```
User sends "Hi"
  → Bot asks for Ullas ID or Phone
    → User enters ID
      → Bot sends OTP (shown in response for testing)
        → User enters OTP
          → ✅ Main Menu (7 options)
            → User picks 1-7 → query result
            → "menu" → back to menu
            → "exit" → logout
```

---

## Project Structure

```
bot/
├── app.py             # Flask app + webhook + state machine
├── config.py          # Env-based configuration
├── auth.py            # OTP & session management
├── handlers.py        # Menu handlers (mock data formatted responses)
├── mock_data.py       # Sample student data
├── whatsapp.py        # WhatsApp Cloud API message sender
├── requirements.txt
├── .env.example
└── README.md
```
=======
# Ullas Student WhatsApp Chatbot — Middleware Layer

A lightweight Python (Flask) middleware that receives WhatsApp messages via the Meta
Cloud API, authenticates students with OTP, and responds with formatted menu-driven
query results.

> **Note:** This version uses **mock data** (no Oracle DB connection). Replace
> `mock_data.py` with real DB queries when ready.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill in your env file
copy .env.example .env          # Windows
# cp .env.example .env          # Linux/Mac

# 3. Start the server
python app.py
```

The server starts on `http://localhost:5000`.

---

## Endpoints

| Route       | Method | Purpose                              |
|-------------|--------|--------------------------------------|
| `/health`   | GET    | Health check → `{"status": "ok"}`    |
| `/webhook`  | GET    | Meta webhook verification handshake  |
| `/webhook`  | POST   | Receive incoming WhatsApp messages   |

---

## Connecting to WhatsApp

1. Create a **Meta Business App** at https://developers.facebook.com
2. Enable the **WhatsApp** product
3. Get your **Temporary Access Token** and **Phone Number ID** from the API Setup page
4. Set them in your `.env` file
5. Expose your local server with [ngrok](https://ngrok.com):
   ```bash
   ngrok http 5000
   ```
6. In Meta Dashboard → WhatsApp → Configuration → set the **Callback URL** to:
   ```
   https://<your-ngrok-id>.ngrok-free.app/webhook
   ```
   Set **Verify Token** to the same value as `VERIFY_TOKEN` in your `.env`

---

## Mock Data / Test Students

| Ullas ID             | Phone          | Scenarios                              |
|----------------------|----------------|----------------------------------------|
| UL-09-2026-00456     | 919876543210   | Verified, centre allocated, 75% att.   |
| UL-10-2025-00789     | 919876543211   | Rejected, no centre, 25% att., failed  |
| UL-11-2024-01023     | 919876543212   | Verified, centre allocated, 100% att.  |

---

## Conversation Flow

```
User sends "Hi"
  → Bot asks for Ullas ID or Phone
    → User enters ID
      → Bot sends OTP (shown in response for testing)
        → User enters OTP
          → ✅ Main Menu (7 options)
            → User picks 1-7 → query result
            → "menu" → back to menu
            → "exit" → logout
```

---

## Project Structure

```
bot/
├── app.py             # Flask app + webhook + state machine
├── config.py          # Env-based configuration
├── auth.py            # OTP & session management
├── handlers.py        # Menu handlers (mock data formatted responses)
├── mock_data.py       # Sample student data
├── whatsapp.py        # WhatsApp Cloud API message sender
├── requirements.txt
├── .env.example
└── README.md
```
>>>>>>> dcac34ae394b737d3d1a4418eaed2730891f06a7
