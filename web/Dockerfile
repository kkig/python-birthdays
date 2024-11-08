# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /code

# # Prevents Python from writing pyc files.
# ENV PYTHONDONTWRITEBYTECODE=1

# # Keeps Python from buffering stdout and stderr to avoid situations where
# # the application crashes without emitting any logs due to buffering.
# ENV PYTHONUNBUFFERED=1

# # Create a non-privileged user that the app will run under.
# # See https://docs.docker.com/go/dockerfile-user-best-practices/
# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/nonexistent" \
#     --shell "/sbin/nologin" \
#     --no-create-home \
#     --uid "${UID}" \
#     appuser

# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

# RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt /code
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

# RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP app.py
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 8000
ENV FLASK_RUN_HOST 0.0.0.0

# # Switch to the non-privileged user to run the application.
# USER appuser

EXPOSE 8000

# COPY /web .
CMD ["flask", "run"]
# CMD ["python", "app.py"]
# CMD uvicorn 'app:app' --host=0.0.0.0 --port=8000


FROM builder AS dev-envs

RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /

CMD ["flask", "run"]