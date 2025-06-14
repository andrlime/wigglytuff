FROM python:3.12.4-bookworm AS base

FROM base AS deps
WORKDIR /app

COPY config.yaml pyproject.toml poetry.lock* ./

RUN pip install poetry
RUN poetry install


FROM deps AS dev
WORKDIR /app

COPY --from=deps /app/. .
COPY . .

EXPOSE 9000:9000
CMD ["poetry", "run", "python", "-m", "main"]


FROM deps AS prod
WORKDIR /app

COPY --from=deps /app/. .
COPY . .

EXPOSE 9000:9000
CMD ["poetry", "run", "waitress-serve", "--port=9000", "--call", "notifier.core.flask.factory:create_flask_app"]
