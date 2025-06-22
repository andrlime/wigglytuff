FROM python:3.12.4-bookworm AS base

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
