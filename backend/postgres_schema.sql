BEGIN;

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS subscriptions (
    subscription_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories(category_id),
    subscription_name VARCHAR(120) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
    billing_cycle VARCHAR(20) NOT NULL CHECK (
        billing_cycle IN ('weekly', 'monthly', 'annual')
    ),
    start_date DATE NOT NULL,
    due_day INTEGER NOT NULL CHECK (due_day BETWEEN 1 AND 31),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    deleted_at TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS notification_settings (
    notification_id SERIAL PRIMARY KEY,
    subscription_id INTEGER NOT NULL UNIQUE
        REFERENCES subscriptions(subscription_id) ON DELETE CASCADE,
    notify_days_before INTEGER NOT NULL DEFAULT 3
        CHECK (notify_days_before >= 0),
    notification_enabled BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO categories (category_id, category_name)
VALUES
    (1, 'Entertainment'),
    (2, 'Productivity'),
    (3, 'Music'),
    (4, 'Cloud Storage'),
    (5, 'Education')
ON CONFLICT (category_id) DO UPDATE
SET category_name = EXCLUDED.category_name;

SELECT setval(
    pg_get_serial_sequence('categories', 'category_id'),
    COALESCE((SELECT MAX(category_id) FROM categories), 1),
    true
);

COMMIT;
