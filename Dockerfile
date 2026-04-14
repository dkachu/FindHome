# --- Stage 1: Build Tailwind ---
FROM node:20-bookworm AS tailwind-builder
WORKDIR /app
COPY . /app/
# Go to the tailwind source folder and build the CSS
RUN cd theme/static_src && npm install && npm run build

# --- Stage 2: Build Django ---
FROM python:3.12-bookworm
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Install system dependencies for Python
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project from the local folder
COPY . /app/
# 🟣 CRITICAL: Copy the compiled CSS from the first stage
COPY --from=tailwind-builder /app/theme/static/css/dist/styles.css /app/theme/static/css/dist/styles.css

# Prepare static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
