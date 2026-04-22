# Vercel Deployment Guide

## Prerequisites

1. Install Vercel CLI (optional, for local testing):
   ```bash
   npm install -g vercel
   ```

2. Have a Vercel account at https://vercel.com

---

## Step 1: Deploy the Backend

### Option A: Deploy via Vercel Dashboard (Recommended)

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Set the **Root Directory** to `backend`
4. Add the following **Environment Variables**:

| Name | Value | Description |
|------|-------|-------------|
| `SECRET_KEY` | `efbffb43bd385039ddb1c6d88c137b2ba5aef738541c11a0e6668ea40310985b` | Session security (generate new one for production) |
| `CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173,https://your-frontend.vercel.app` | Allowed frontend URLs |
| `FLASK_ENV` | `production` | Environment flag |
| `DATABASE_URL` | (coming soon) | PostgreSQL URL when database is set up |

5. Click **Deploy**

### Option B: Deploy via CLI

```bash
cd backend
vercel --prod
```

Then add environment variables in the Vercel dashboard under **Settings > Environment Variables**.

---

## Step 2: Get Your Backend URL

After deployment, Vercel will give you a URL like:
```
https://subtrack-backend.vercel.app
```

Copy this URL - you'll need it for the frontend configuration.

---

## Step 3: Configure Frontend API URL

### For Local Development

Create a `.env` file in the frontend root (next to `vite.config.js`):

```bash
# Use empty for localhost backend
VITE_API_BASE_URL=
```

Or point to a local backend:
```bash
VITE_API_BASE_URL=http://127.0.0.1:5000
```

### For Production Build

When building for production, set the environment variable:

```bash
VITE_API_BASE_URL=https://your-backend.vercel.app npm run build
```

Or create `.env.production`:
```bash
VITE_API_BASE_URL=https://your-backend.vercel.app
```

---

## Step 4: Deploy the Frontend

### If Frontend and Backend are in the Same Repo

1. In Vercel, create a **second project** for the frontend
2. Set **Root Directory** to the repo root (where `vite.config.js` is)
3. Add **Environment Variable**:
   - `VITE_API_BASE_URL` = `https://your-backend.vercel.app`
4. Deploy

### Build Command
```bash
npm run build
```

### Output Directory
```
dist
```

---

## Step 5: Update CORS Origins

After deploying the frontend, go back to your **Backend** project in Vercel and update the `CORS_ORIGINS` environment variable to include your frontend URL:

```
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,https://your-frontend.vercel.app
```

Redeploy the backend for changes to take effect.

---

## Environment Variables Summary

### Backend (Vercel)

| Variable | Required | Example |
|----------|----------|---------|
| `SECRET_KEY` | Yes (production) | `your-64-char-hex-string` |
| `CORS_ORIGINS` | Yes | `https://frontend.vercel.app` |
| `FLASK_ENV` | Yes | `production` |
| `DATABASE_URL` | Soon | `postgresql://user:pass@host/db` |

### Frontend (Vercel)

| Variable | Required | Example |
|----------|----------|---------|
| `VITE_API_BASE_URL` | Yes (production) | `https://backend.vercel.app` |

---

## Testing Locally

### Run Backend
```bash
cd backend
source ../venv/bin/activate  # or your venv activation
python app.py
```

Backend runs at: `http://127.0.0.1:5000`

### Run Frontend
```bash
npm run dev
```

Frontend runs at: `http://127.0.0.1:5173`

---

## Troubleshooting

### CORS Errors in Production

1. Verify `CORS_ORIGINS` in backend includes your frontend URL exactly (no trailing slash)
2. Redeploy backend after changing environment variables
3. Clear browser cache and hard refresh

### API Not Found

1. Check `VITE_API_BASE_URL` is set correctly in frontend
2. Verify backend deployment URL is accessible
3. Test backend directly: `https://your-backend.vercel.app/api/user`

### Session Issues

1. Ensure `SECRET_KEY` is set in Vercel
2. Check that `SESSION_COOKIE_SECURE` matches your HTTPS setup
3. Vercel is always HTTPS, so cookies need secure flag

---

## Next Steps: Database Setup

When ready to add a database:

1. Choose a hosted PostgreSQL provider:
   - **Neon** (free tier): https://neon.tech
   - **Supabase** (free tier): https://supabase.com
   - **Railway** (paid): https://railway.app

2. Get the connection URL (looks like):
   ```
   postgresql://user:password@host:5432/database
   ```

3. Add to Vercel backend environment variables as `DATABASE_URL`

4. Redeploy backend

5. Remove the SQLite fallback from `config.py` if desired
