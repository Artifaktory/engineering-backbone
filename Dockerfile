# Tooling image for this repository; application images stay project-owned.
# The immutable official Python image includes Git, required by Copier.
FROM python:3.12-bookworm@sha256:5560e9ab8709f459489e5b8aa696eda8a07ef821e14bb122be62d91234bfa98b

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH=/opt/backbone-venv/bin:$PATH

WORKDIR /workspace
COPY requirements.lock /tmp/requirements.lock
RUN python -m venv /opt/backbone-venv \
    && /opt/backbone-venv/bin/python -m pip install --no-cache-dir --require-hashes --only-binary=:all: -r /tmp/requirements.lock \
    && /opt/backbone-venv/bin/python -m pip check \
    && git --version \
    && groupadd --gid 10001 backbone \
    && useradd --uid 10001 --gid backbone --create-home backbone

COPY . /workspace
USER backbone
CMD ["python", "scripts/validate.py"]
