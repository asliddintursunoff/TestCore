FROM python:3.12.3-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    build-essential \
    libpq-dev \
    && apt-get clean

# Set work directory
WORKDIR /app

# Set PYTHONPATH so Django can find modules
ENV PYTHONPATH="/app"

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run server with gunicorn
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn project.wsgi:application --bind 0.0.0.0:8080"]
