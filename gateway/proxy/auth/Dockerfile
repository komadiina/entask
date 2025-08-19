FROM python:3.12-alpine
RUN apk add curl

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /gateway/proxy/auth
RUN export PYTHONPATH=$PYTHONPATH:/gateway/proxy/auth

COPY . /gateway/proxy/auth
EXPOSE ${AUTH_PROXY_PORT}

ENTRYPOINT ["python"]
CMD ["app.py"]

