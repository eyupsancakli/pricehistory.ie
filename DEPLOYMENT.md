# Deployment Guide for pricehistory.ie

This guide explains how to deploy your Django application to a modern cloud platform like **Render**, **Railway**, or **Heroku**.

## 1. Preparation (Already Completed)

Your project has been configured for production:
-   **`requirements.txt`**: Lists all dependencies, including production-only packages like `gunicorn` and `psycopg2-binary`.
-   **`Procfile`**: Tells the server how to run your app (`web: gunicorn price_tracker.wsgi`).
-   **`settings.py`**: Updated to read configuration from Environment Variables (Secrets).
-   **`staticfiles`**: Configured with `WhiteNoise` to serve CSS/JS efficiently.

## 2. Environment Variables

When you deploy, you MUST set the following Environment Variables in your hosting dashboard:

| Variable | Value | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | *(A long random string)* | Generates cryptographic signatures. Use a generator to make a new one. |
| `DEBUG` | `False` | **CRITICAL**. Never run with True in production. |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` | The domain name of your live site. |
| `DATABASE_URL` | *(Provided by Host)* | Connection string for your PostgreSQL database. |

## 3. Deploying to Render.com (Recommended)

1.  **Push to GitHub**: Ensure your code is in a GitHub repository.
2.  **Create New Web Service**: In Render, connect your repo.
3.  **Settings**:
    -   **Runtime**: Python 3
    -   **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
    -   **Start Command**: `gunicorn price_tracker.wsgi --log-file -`
4.  **Add Environment Variables**: Add the variables listed above.

## 4. Local Development

You can continue to run the app locally as usual:
```bash
python manage.py runserver
```
The settings are configured to fallback to local defaults (SQLite, Debug=True) if Environment Variables are missing.
