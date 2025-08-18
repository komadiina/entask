FROM python:3.12-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /gateway/router
RUN export PYTHONPATH=$PYTHONPATH:/gateway/router

COPY . /gateway/router
EXPOSE ${G_ROUTER_PORT}

ENTRYPOINT ["python"]
CMD ["app.py"]