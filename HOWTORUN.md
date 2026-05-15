# How To Run SubTrack

This project has two parts:

- Vue frontend
- Flask backend

The frontend runs on `127.0.0.1:5173`.
The backend runs on `127.0.0.1:5001`.

`5001` is intentional. On some macOS setups, port `5000` is already used by system services.

## 1. Install frontend dependencies

From the project root:

```bash
cd "/Users/austin/Documents/New project/SubTrack"
npm install
```

## 2. Set up the backend virtual environment

```bash
cd "/Users/austin/Documents/New project/SubTrack/backend"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If `venv` already exists, you only need:

```bash
cd "/Users/austin/Documents/New project/SubTrack/backend"
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Choose the database

The backend reads its database connection from:

- [backend/.env.example](/Users/austin/Documents/New%20project/SubTrack/backend/.env.example)

Create your local backend env file:

```bash
cd "/Users/austin/Documents/New project/SubTrack/backend"
cp .env.example .env
```

Then edit `backend/.env` and set `DATABASE_URL`.

### Option A: SQLite

Use this if you want the fastest and most reliable local setup:

```env
DATABASE_URL=sqlite:///subtrack.db
```

You do not need to run any SQL manually for SQLite. Flask will create the tables on startup.

### Option B: Supabase / PostgreSQL

Use a valid Supabase or PostgreSQL connection string:

```env
DATABASE_URL=postgresql+psycopg://username:password@host:port/database
```

If you use Supabase, use the exact connection string from the Supabase dashboard.

Important:

- if your machine cannot resolve the Supabase host, the backend will not start
- for a time-sensitive demo, SQLite is the safer fallback

## 4. Run the backend

```bash
cd "/Users/austin/Documents/New project/SubTrack/backend"
source venv/bin/activate
python app.py
```

Expected local backend URL:

- `http://127.0.0.1:5001`

## 5. Run the frontend

Open a second terminal:

```bash
cd "/Users/austin/Documents/New project/SubTrack"
npm run dev
```

Expected frontend URL:

- `http://127.0.0.1:5173`

Open that URL in the browser.

## 6. If the frontend says it cannot reach the backend

Check these in order:

1. Make sure the backend terminal is still running.
2. Make sure the backend is on `127.0.0.1:5001`, not `5000`.
3. Make sure the frontend is opened from `127.0.0.1:5173`.
4. Restart both frontend and backend after changing any `.env` value.

## 7. If the backend says `No module named 'flask'`

You are not inside the backend virtual environment. Run:

```bash
cd "/Users/austin/Documents/New project/SubTrack/backend"
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## 8. If the backend fails on Supabase DNS or connection

Switch back to SQLite in `backend/.env`:

```env
DATABASE_URL=sqlite:///subtrack.db
```

Then restart the backend.

## 9. Notes about recurrence

Subscriptions now support:

- daily
- weekly
- monthly
- yearly
- custom intervals like every 3 days
- forever recurrence
- recurrence until a chosen end date

The calendar should reflect those recurring dates as long as the backend is running and the subscription data loads successfully.
