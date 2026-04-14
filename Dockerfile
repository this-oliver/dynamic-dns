FROM python:3.15.0a8-slim@sha256:a28758f9978680d6aa6145e75cb3032b1b9fe4dcd3abc46471b3a6bda57f0daf

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

USER 1001

ENTRYPOINT [ "python", "-m", "src.main" ]