# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

EXPOSE ${PORT:-8001}
# Install pip requirements
COPY ./src/api/requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# Use root bc fastapi can reade but can't change sql database from container
USER root

ENV PWD=/app
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
RUN cd /
CMD ["python", "main_api.py"]
