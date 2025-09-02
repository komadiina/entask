FROM python:3.12.11-alpine
RUN apk add curl

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /services/llm
RUN export PYTHONPATH=$PYTHONPATH:/services/llm

COPY . /services/llm
EXPOSE ${LLM_SERVICE_PORT}

ENTRYPOINT ["python"]
CMD ["app.py"]

