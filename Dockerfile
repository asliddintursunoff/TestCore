FROM python:3.12.3-slim

# Install LaTeX and system dependencies
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    build-essential \
    libpq-dev \
    && apt-get clean

# Set working directory
WORKDIR /app

# Set PYTHONPATH for Django
ENV PYTHONPATH="/app"

# Copy your project into the image
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
