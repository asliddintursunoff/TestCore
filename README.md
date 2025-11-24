AUTHOR: @asliddintursunoff

# TestCore

TestCore is a small experimental project I built to explore how an AI-powered exam preparation platform could work for universities in Uzbekistan. The idea was simple: create a place where pupils and teachers can access mock entrance exams, generate new questions, and check answers with the help of AI.

This project is currently **stopped**. It reached MVP level and did what I needed, so development is on pause.

---

## 🎯 Project Purpose

The goal behind TestCore was to build an environment where users can:

* Browse mock entrance exams for different universities in Uzbekistan
* Practice full tests with real-style difficulty and structure
* Ask AI to analyze or explain any question with one click
* Let teachers generate new exam packages automatically from sample PDFs

It was meant to mimic a full exam preparation system from generating tests to analyzing answers.

---

## 🧩 Main Features

### 🔐 Dual Authentication

Two roles exist: **teachers** and **pupils**.
Authentication is done **once** using a Telegram bot.

### 👨‍🏫 Teacher Tools

Teachers can upload example exam PDFs (e.g., “INHA University Grand Exam”).
The system reads the PDF, understands the format and difficulty, and generates a new PDF with the same structure.

* PDF parsing with PyMuPDF
* Question generation via **Gemini Pro**
* Math expressions rendered using LaTeX for clean formatting
* Output saved as PDF again

### 🎓 Pupil Features

Pupils can practice exam questions and take mock exams.
When they can’t solve something, they tap one button to ask AI for an explanation.

### 💳 Subscription (Not Fully Finished)

Payme integration is connected, but the subscription layer itself wasn’t completed.
I planned to disable expired subscriptions using Celery jobs.

### 🤖 AI Stack

AI functionality is powered by **Gemini Pro**.
Most of the development was done using their free tier to keep this as a simple MVP.

### 🐳 Docker

For production, the project was deployed using **Docker**.
I used Docker to keep the environment clean and make sure Celery, Redis, the bot, and the Django API all ran consistently without manual setup.

---

## 🛠️ Tech Overview

* **Backend:** Django, Django REST Framework
* **Tasks:** Celery + Redis
* **AI:** Google Gemini Pro
* **PDF / Parsing:** PyMuPDF, WeasyPrint, LaTeX rendering
* **Payments:** Payme
* **Auth:** Telegram bot
* **Deployment:** Docker, Gunicorn, Gevent, Whitenoise
* **Storage:** AWS S3 (django-storages)

The full list of dependencies is visible in the repository.

---

## 🔄 Project Status

This project is **on hold**.
It served as a personal MVP to experiment with AI workflows and service integrations, and I stopped before polishing everything.

---

## 📦 Repository

GitHub: [https://github.com/asliddintursunoff/TestCore](https://github.com/asliddintursunoff/TestCore)

---

## 📌 Notes

* No license included
* This was never meant to be a polished production system — just a learning and testing project
