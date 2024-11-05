# syntax=docker/dockerfile:1
FROM python:3.13-slim
WORKDIR /app

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

EXPOSE 5000

COPY /src .
CMD ["flask", "run", "--debug"]
# CMD ["python", "app.py"]
# CMD uvicorn 'app:app' --host=0.0.0.0 --port=8000