FROM python:3.12.3-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    build-essential \
    libpq-dev \
    && apt-get clean

WORKDIR /app
ENV PYTHONPATH="/app"

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Railway
EXPOSE 8080

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8080", "--log-level", "debug"]
