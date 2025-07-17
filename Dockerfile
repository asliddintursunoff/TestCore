FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y texlive-latex-base && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run Django commands
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
