FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y texlive-latex-base && \
    apt-get clean

# Set workdir
WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files and run the app
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
