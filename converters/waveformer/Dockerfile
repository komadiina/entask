FROM python:3.12-alpine AS builder
RUN apk add curl

WORKDIR /converters/waveformer
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /converters/waveformer/requirements.txt
RUN export PYTHONPATH=$PYTHONPATH:/converters/waveformer

COPY . .

ENTRYPOINT [ "python" ]
CMD ["app.py"]