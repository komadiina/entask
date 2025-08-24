FROM python:3.12-alpine AS builder
RUN apk add curl

WORKDIR /converters/term-extractor
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /converters/term-extractor/requirements.txt
RUN export PYTHONPATH=$PYTHONPATH:/converters/term-extractor

COPY . .

ENTRYPOINT [ "python" ]
CMD ["app.py"]