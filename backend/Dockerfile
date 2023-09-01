FROM python:3.11-slim AS base
RUN apt update && apt install -y libsasl2-dev libldap2-dev libssl-dev gcc
COPY . /src
WORKDIR /src
CMD ["python", "/src/league_push_ups_backend/app.py"]

FROM base AS dev
RUN pip install -e .[test]

FROM base AS prod
RUN pip install .
