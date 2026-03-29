# SubTrack Backend

This folder contains the Flask backend for the SubTrack project.

## What it does

- Registers users and stores hashed passwords
- Logs users in and out with Flask sessions
- Lets a logged-in user create, view, update, and delete subscriptions
- Stores notification settings for each subscription
- Returns upcoming subscription dues
- Returns a monthly cost summary
- Seeds default categories on first run
- Supports SQLite now and PostgreSQL later
- Works cleanly with a Vue frontend

## Folder structure

```text
backend/
├── app.py
├── config.py
├── requirements.txt
├── models/
├── routes/
└── utils/
```

## Default seeded categories

These categories are inserted automatically the first time the app starts:

1. Entertainment
2. Productivity
3. Music
4. Cloud Storage
5. Education

## How to run locally

1. Open a terminal in the backend folder:

```bash
cd /Users/austin/Documents/New\ project/SubTrack/backend
```

2. Create a virtual environment:

```bash
python3 -m venv venv
```

3. Activate it:

```bash
source venv/bin/activate
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

5. Create your local environment file:

```bash
cp .env.example .env
```

6. Start the Flask server:

```bash
python app.py
```

The backend will run on `http://127.0.0.1:5000`.

The SQLite database file will be created automatically as:

```text
backend/subtrack.db
```

## Using PostgreSQL later

When you are ready to move from SQLite to PostgreSQL, update the `DATABASE_URL` in `.env`.

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/subtrack_db
```

You do not need to change the model code for that switch because SQLAlchemy handles the database connection.

## Important for frontend integration

- The backend uses session-based authentication
- Your frontend should send requests with credentials included
- Example in `fetch`:

```javascript
fetch("http://127.0.0.1:5000/api/user", {
  credentials: "include",
});
```

- Example in `axios`:

```javascript
axios.get("http://127.0.0.1:5000/api/user", {
  withCredentials: true,
});
```

## Sample JSON request bodies

### Register

`POST /api/auth/register`

```json
{
  "username": "austin",
  "email": "austin@example.com",
  "password": "password123"
}
```

### Login

`POST /api/auth/login`

```json
{
  "email": "austin@example.com",
  "password": "password123"
}
```

### Create subscription

`POST /api/subscriptions`

```json
{
  "category_id": 1,
  "subscription_name": "Netflix Premium",
  "amount": 549.00,
  "billing_cycle": "monthly",
  "start_date": "2026-03-01",
  "due_day": 15,
  "is_active": true,
  "notification_setting": {
    "notify_days_before": 3,
    "notification_enabled": true
  }
}
```

### Update subscription

`PUT /api/subscriptions/1`

```json
{
  "amount": 599.00,
  "due_day": 18,
  "notification_setting": {
    "notify_days_before": 5,
    "notification_enabled": true
  }
}
```

### Logout

`POST /api/auth/logout`

No request body is required.

## Endpoint list

### Auth

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`

### User

- `GET /api/user`

### Subscriptions

- `GET /api/subscriptions`
- `POST /api/subscriptions`
- `GET /api/subscriptions/<id>`
- `PUT /api/subscriptions/<id>`
- `DELETE /api/subscriptions/<id>`
- `GET /api/subscriptions/upcoming`
- `GET /api/subscriptions/summary`

## Brief file explanation

- `app.py`: Starts Flask, loads config, enables CORS, registers routes, and creates the database tables.
- `config.py`: Stores settings such as the secret key, database URL, and allowed frontend origins.
- `models/`: Contains the database tables and relationships.
- `routes/`: Contains the API endpoints for authentication, user data, and subscriptions.
- `utils/`: Contains helper logic for auth checks, validation, date calculations, and default category seeding.
- `requirements.txt`: Lists the Python packages needed to run the backend.
- `.env.example`: Shows the environment variables needed for local development.
