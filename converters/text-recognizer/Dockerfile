
FROM python:3.12-alpine AS builder
RUN apk add curl

WORKDIR /converters/text-recognizer
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /converters/text-recognizer/requirements.txt
RUN export PYTHONPATH=$PYTHONPATH:/converters/text-recognizer

COPY . .

ENTRYPOINT [ "python" ]
CMD ["app.py"]