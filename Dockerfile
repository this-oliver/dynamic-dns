FROM python:3.15.0b2-slim@sha256:4c6413e9d36127c1322ef2e602b0a680dd726be10f9c2c3265b6928807810841

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

USER 1001

ENTRYPOINT [ "python", "-m", "src.main" ]