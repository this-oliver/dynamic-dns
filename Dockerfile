FROM python:3.15.0b1-slim@sha256:89a7e6cfaeb87cc9884cf07c481a760b11e501b3dca0b31fa25d9360ab1e12f9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

USER 1001

ENTRYPOINT [ "python", "-m", "src.main" ]