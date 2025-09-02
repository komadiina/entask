FROM python:3.12.11-alpine AS builder
RUN apk add curl

RUN apk add ffmpeg

WORKDIR /converters/thumbnailer
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /converters/thumbnailer/requirements.txt
RUN export PYTHONPATH=$PYTHONPATH:/converters/thumbnailer

COPY . .

ENTRYPOINT [ "python" ]
CMD ["app.py"] 