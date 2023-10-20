# builder base image
FROM python:3.11 as builder

LABEL maintainer="Yash Jain <yash@licensemate.ca>"

# install poetry
RUN pip install poetry==1.6.1

# set environment variables
ENV POETRY_NO_INTERACTION=1 \
	POETRY_VIRTUALENVS_IN_PROJECT=1 \
	POETRY_VIRTUALENVS_CREATE=1 \
	POETRY_CACHE_DIR=/tmp/poetry_cache
WORKDIR /server

# copy the poetry files
COPY server/pyproject.toml server/poetry.lock ./

# install python dependcies
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --with prod --no-root

# runner base image
FROM python:3.11-slim as runtime

# set environment variables
ENV VIRTUAL_ENV=/server/.venv \
	PATH="/server/.venv/bin:$PATH"

# copy the virtual environment and server files
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY server ./server
WORKDIR /server

# expose port
EXPOSE 80

# flask dev environment
ENTRYPOINT ["gunicorn", "main:app", "--bind=0.0.0.0:80", "--reload"]