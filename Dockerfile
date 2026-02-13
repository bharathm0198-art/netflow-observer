FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for building some python packages)
# For psycopg2-binary, usually no extra system deps are needed for runtime on slim
# but good to have if we switch to non-binary psycopg2
# RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# We'll run main.py from the parent directory of app, so we set PYTHONPATH or run as module
# Assuming we mount or copy the root to /app, but here we copied app/ to /app/app/
# Let's adjust slightly: copy contents into /app structure nicely.

# Better structure for container:
# /project/app
# /project/main.py? No, main is inside app/main.py
# So if specific structure is app/main.py, we can run "python -m app.main" if app is a package
# Or just "python app/main.py"

ENV PYTHONPATH=/app

CMD ["python", "app/main.py"]
