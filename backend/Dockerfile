FROM python:3.11-slim AS base
ENV FLASK_APP=league_push_ups_backend.app
RUN pip install Flask>=2 Werkzeug==2.1.2 Flask-RESTful flask-cors
COPY league_push_ups_backend /src
COPY setup.py /src/setup.py
WORKDIR /src
CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0"]

FROM base AS dev
ENV FLASK_ENV=development
RUN pip install -e .[test]

FROM base AS prod
ENV FLASK_ENV=production
RUN pip install .
