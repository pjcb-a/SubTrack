# SubTrack

SubTrack is a full-stack subscription tracking app built with Vue, Vite, and Flask. It helps users manage recurring payments, monitor upcoming renewals, and keep a record of deleted subscriptions through the history view.

## Features

- User registration and login with Flask session-based authentication
- Dashboard for active subscriptions
- Add, update, and delete subscription flows
- History view for deleted subscriptions
- Filter subscriptions by billing cycle
- Upcoming renewal and spending summaries
- Local development support for both SQLite and PostgreSQL

## Stack

- Frontend: Vue 3, Vue Router, Vite
- Backend: Flask, Flask-SQLAlchemy, Flask-CORS
- Database: SQLite or PostgreSQL

## Run Locally

Clone the repository and open the project folder:

```bash
git clone https://github.com/pjcb-a/SubTrack.git
cd SubTrack
```

Frontend:

```bash
npm install
npm run dev
```

Backend:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Default local URLs:

- Frontend: `http://127.0.0.1:5173`
- Backend: `http://127.0.0.1:5000`

## Database Setup

The backend reads its database connection from:

[`backend/.env.example`](./backend/.env.example)

Copy it first:

```bash
cd backend
cp .env.example .env
```

Then set `DATABASE_URL` in `backend/.env`.

SQLite example:

```env
DATABASE_URL=sqlite:///subtrack.db
```

PostgreSQL over TCP:

```env
DATABASE_URL=postgresql+psycopg://<your_postgres_user>:<your_password>@localhost:5432/subtrack
```

PostgreSQL over Unix socket:

```env
DATABASE_URL=postgresql+psycopg://<your_postgres_user>@/subtrack
```

If you use PostgreSQL, create the database and load the schema first:

```bash
createdb subtrack
psql -U <your_postgres_user> -d subtrack -f postgres_schema.sql
```

After changing `backend/.env`, restart the backend:

```bash
cd backend
source venv/bin/activate
python app.py
```

For full localhost and PostgreSQL setup instructions, see [backend/LOCALHOST_SETUP.md](./backend/LOCALHOST_SETUP.md).

For backend-specific configuration details, see [backend/README.md](./backend/README.md).

## Project Structure

- `src/components/dashboard/`: dashboard UI
- `src/components/history/`: subscription history view
- `src/composables/`: shared frontend state and API interaction
- `src/style.css`: global theme and UI tokens
- `backend/`: Flask API, models, routes, and database setup
