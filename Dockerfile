FROM python:3.9-alpine3.13

COPY . /app

WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt

ENV PATH="/py/bin:$PATH"
# your welcome
CMD ["python", "src/start.py"]