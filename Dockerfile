ARG py_version=3.13
ARG uv_version=0.7.8

FROM ghcr.io/astral-sh/uv:${uv_version}-alpine AS requirements-stage

WORKDIR /tmp
COPY ./pyproject.toml ./uv.lock* /tmp/
RUN uv export --no-dev --no-hashes --output-file requirements.txt


FROM python:${py_version}-slim

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN find /tmp -mindepth 1 -delete

COPY ./src/tplapi /app/tplapi

RUN sed -i '/^upload_dir:/s|:.*|: "/var/uploads"|' /app/tplapi/config/config.yaml

RUN mkdir -p /var/uploads/TEMPLATES
COPY ./tests/resources/templates/dose_response.json /var/uploads/TEMPLATES/3c22a1f0-a933-4855-848d-05fcc26ceb7a.json

ENV TEMPLATE_API_CONFIG="/app/tplapi/config/config.yaml"
EXPOSE 80
WORKDIR /app

CMD ["uvicorn", "tplapi.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]
