FROM python:3.12-alpine
RUN apk add curl

WORKDIR /services/notifier
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ENTRYPOINT [ "python" ]
CMD ["app.py"]