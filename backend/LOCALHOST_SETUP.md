# SubTrack Localhost Setup

This guide is for running SubTrack on a local machine with the Vue frontend,
the Flask backend, and either SQLite or PostgreSQL.

## What You Need

- Node.js 18+ recommended
- Python 3.10+ recommended
- PostgreSQL only if you want the app to use a real local database instead of SQLite

## Project Layout

- Frontend root: `/Users/austin/Documents/New project/SubTrack`
- Backend folder: `/Users/austin/Documents/New project/SubTrack/backend`

## 1. Frontend Setup

Open a terminal in the project root:

```bash
cd "/Users/austin/Documents/New project/SubTrack"
npm install
```

Start the frontend:

```bash
npm run dev
```

The Vite config is pinned to:

```text
http://127.0.0.1:5173
```

Use that exact URL in the browser during local development.

## 2. Backend Setup

Open another terminal:

```bash
cd "/Users/austin/Documents/New project/SubTrack/backend"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Start the backend:

```bash
python app.py
```

The backend runs at:

```text
http://127.0.0.1:5000
```

## 3. Database Options

### Option A: SQLite

This is the easiest local setup.

Use this in `backend/.env`:

```env
DATABASE_URL=sqlite:///subtrack.db
```

The backend will create the SQLite file automatically inside `backend/`.

### Option B: PostgreSQL

Use PostgreSQL when you want a persistent local database that is easier to inspect with SQL queries.

Create the database:

```bash
createdb subtrack
```

Load the schema:

```bash
cd "/Users/austin/Documents/New project/SubTrack/backend"
psql -U <your_postgres_user> -d subtrack -f postgres_schema.sql
```

If your machine does not have a `postgres` role, use your actual PostgreSQL username.
On one local setup this was `austin`, so the command looked like:

```bash
psql -U austin -d subtrack -f postgres_schema.sql
```

Then update `backend/.env`.

TCP example:

```env
DATABASE_URL=postgresql+psycopg://<your_postgres_user>:<your_password>@localhost:5432/subtrack
```

Unix socket example:

```env
DATABASE_URL=postgresql+psycopg://<your_postgres_user>@/subtrack
```

If you do not want to type a password each time and your local PostgreSQL already trusts your user, the socket form is usually simpler.

## 4. History and Mock Data Notes

- New users can start with seeded sample subscriptions
- Deleted subscriptions now persist in History through the backend
- History survives browser refresh because deleted records are stored in the database instead of only in frontend memory

## 5. Quick Verification

After both servers are running:

1. Open `http://127.0.0.1:5173`
2. Register a new account
3. Log in
4. Add a subscription
5. Delete a subscription
6. Open History and refresh the page

If the setup is working, the deleted item should still appear in History after refresh.

## 6. Useful Checks

Verify the backend is reachable:

```bash
curl -i http://127.0.0.1:5000/api/user
```

Expected logged-out result:

```text
401 Authentication required
```

List PostgreSQL tables:

```bash
psql -U <your_postgres_user> -d subtrack -c '\dt'
```

List current subscriptions:

```bash
psql -U <your_postgres_user> -d subtrack -c "SELECT subscription_id, subscription_name, is_active, deleted_at FROM subscriptions ORDER BY subscription_id DESC;"
```

## 7. Common Problems

### Blank page on the frontend

- Make sure the backend is running
- Make sure you opened `http://127.0.0.1:5173`
- Restart `npm run dev` after pulling new frontend changes

### Backend says port 5000 is in use

Another process is already bound to port `5000`. Check it with:

```bash
lsof -nP -iTCP:5000 -sTCP:LISTEN
```

### PostgreSQL role does not exist

Your local database user may not be named `postgres`.

Check available roles:

```bash
psql -d postgres -c '\du'
```

### Frontend says it cannot reach the backend

- Confirm Flask is running on `127.0.0.1:5000`
- Confirm the browser is using `127.0.0.1:5173`
- Restart both servers after changing `.env`
