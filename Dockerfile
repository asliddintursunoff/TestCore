FROM python:3.12-slim

# System dependencies for LaTeX & static builds
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    texlive-latex-extra \
    ghostscript \
    build-essential \
    && apt-get clean

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run Django setup
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Start Gunicorn as the main web server
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
