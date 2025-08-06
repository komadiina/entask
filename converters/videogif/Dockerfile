FROM python:3.12-alpine AS builder

WORKDIR /converters/videogif
COPY . .
RUN pip install --no-cache-dir --upgrade -r /converters/videogif/requirements.txt
RUN export PYTHONPATH=$PYTHONPATH:/converters/videogif
RUN chown $USER:$USER -R /api

ENTRYPOINT [ "python" ]
CMD ["app.py"]