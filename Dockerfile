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

WORKDIR /app
ENV PYTHONPATH="/app"

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

EXPOSE 8080

CMD sh -c "python manage.py collectstatic --noinput && \
           python manage.py migrate && \
           gunicorn testcore.wsgi:application --bind 0.0.0.0:${PORT}"
