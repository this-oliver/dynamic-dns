FROM python:3.15.0-alpine@sha256:2699b90f4d562a22e2dd076c82f964032f64814204bff36d271a54ba4cc2c7e2

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

RUN chown -R 1000:1000 /app
USER 1000

ENTRYPOINT [ "python", "-m", "src.main" ]