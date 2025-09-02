FROM python:3.12.11-alpine

RUN apk add curl
RUN export PYTHONPATH=$PYTHONPATH:/gateway/proxy/ws

WORKDIR /gateway/proxy/ws
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE ${WS_PROXY_PORT}

ENTRYPOINT [ "python" ]
CMD ["app.py"]