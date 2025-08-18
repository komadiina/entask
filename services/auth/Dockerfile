FROM python:3.12-alpine

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /services/auth
RUN export PYTHONPATH=$PYTHONPATH:/services/auth

COPY . /services/auth
EXPOSE 4201

ENTRYPOINT ["python"]
CMD ["app.py"]

