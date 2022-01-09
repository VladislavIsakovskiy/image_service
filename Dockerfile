FROM python:3.9.5-slim

WORKDIR /usr/local/app/

RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -U poetry

COPY pyproject.toml poetry.lock poetry.toml .env ./
COPY image_service ./image_service/
COPY static ./static/
COPY images ./images/

RUN poetry install --no-dev -n

EXPOSE 5555

CMD [".venv/bin/python", "-m", "image_service"]
#CMD bash
