FROM python:3.12.4-bookworm AS base

RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates fonts-liberation libnss3 libxss1 libasound2 libatk1.0-0 libgtk-3-0 libgbm1 \
    chromium chromium-driver

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV DISPLAY=:99

FROM base AS deps
WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry
RUN poetry install


FROM deps AS dev
WORKDIR /app

COPY --from=deps /app/. .
COPY . .

EXPOSE 9000:9000
CMD ["poetry", "run", "python", "-m", "main", "-c", "config.yaml"]


FROM deps AS prod
WORKDIR /app

COPY --from=deps /app/. .
COPY . .

CMD ["poetry", "run", "python", "-m", "main", "-c", "config.yaml"]
