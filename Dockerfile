FROM python:3.12.3-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    locales \
    tesseract-ocr \
    libtesseract-dev \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    build-essential \
    libpq-dev \
    && apt-get clean

# Enable UTF-8 locale
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

WORKDIR /app
ENV PYTHONPATH="/app"

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["sh", "-c", "python manage.py collectstatic --noinput && \
                 python manage.py migrate && \
                 gunicorn project.wsgi:application --worker-class=gevent --workers=2 --bind 0.0.0.0:8080"]
