# Backend (FastAPI)

This directory contains the API server for the Hackathon project. It is written in FastAPI and deployed on Vercel using the `@vercel/python` builder.

## Local setup

1. **Copy environment file**
   ```bash
   cp .env.example .env
   ```
   and then fill in the Supabase URL/keys and the URLs used for CORS.

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

## Environment variables

The application uses [pydantic Settings](https://pydantic-docs.helpmanual.io/usage/settings/) to load configuration values. It reads values from the environment and, during local development, from the `.env` file.

Variables used:

- `SUPABASE_URL` – your Supabase project URL
- `SUPABASE_KEY` – anon/public API key
- `SUPABASE_SERVICE_KEY` – service role key for server operations
- `BACKEND_URL` – base URL of the backend (for generating links)
- `FRONTEND_URL` – address of the frontend for CORS and link generation

> **Important:** Do not check real keys into version control. Use `.env` locally and set the same variables via the Vercel dashboard in production.

## Deployment notes

The root `vercel.json` routes `/api/*` to `backend/main.py` and builds both backend and frontend together. The `requirements.txt` file must exist so Vercel can install dependencies.

### CORS

Allowed origins are read from `FRONTEND_URL` environment variable, so make sure it matches the deployed frontend domain (e.g. `https://my-app.vercel.app`).


### ローカルで動かすには
- `backend/` フォルダ内の `.env.example` をコピーして `.env` を作成し、Supabase の情報を設定。
- `python -m venv .venv && .\.venv\Scripts\activate` で仮想環境を作り、
  `pip install -r backend/requirements.txt` で依存関係をインストール。
- `uvicorn backend.main:app --reload` を実行すると `http://localhost:8000` で API が起動します。