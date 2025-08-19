FROM python:3.12-alpine
RUN apk add curl

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /services/version-api
RUN export PYTHONPATH=$PYTHONPATH:/services/version-api

COPY . /services/version-api
EXPOSE ${VERSION_API_PORT}

ENTRYPOINT ["python"]
CMD ["app.py"]

