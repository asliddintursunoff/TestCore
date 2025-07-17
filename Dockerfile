# Use Python slim image
FROM python:3.12.3-slim


# Install required Linux packages (LaTeX)
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    && apt-get clean

# Set working directory inside the container
WORKDIR /app

# Set PYTHONPATH so Django finds modules
ENV PYTHONPATH="/app"

# Copy project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run server
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && python manage.py runserver"]
