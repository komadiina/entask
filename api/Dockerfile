FROM python:3.12-alpine

WORKDIR /api
COPY . /api

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
RUN export PYTHONPATH=$PYTHONPATH:/api
EXPOSE 4201

ENTRYPOINT ["python"]
CMD ["app.py"]