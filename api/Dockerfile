FROM python:3.12-alpine

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /api
RUN export PYTHONPATH=$PYTHONPATH:/api

COPY . /api
EXPOSE 4201

ENTRYPOINT ["python"]
CMD ["app.py"]

