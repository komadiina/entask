FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get -y install tesseract-ocr \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

RUN apt update \
  && apt-get install ffmpeg libsm6 libxext6 -y
RUN pip3 install pytesseract
RUN pip3 install opencv-python
RUN pip3 install pillow
WORKDIR /converters/text-recognizer

# huge ass packages, docker-cache these build steps
RUN pip install torch
RUN pip install nvidia-cublas-cu12
RUN pip install nvidia-cudnn-cu12
RUN pip install nvidia_cufft_cu12
RUN pip install nvidia_cusolver_cu12
RUN pip install nvidia_cusparse_cu12
RUN pip install nvidia_cusparselt_cu12
RUN pip install nvidia_nccl_cu12
RUN pip install triton


COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /converters/text-recognizer/requirements.txt
RUN export PYTHONPATH=$PYTHONPATH:/converters/text-recognizer

COPY . .

ENTRYPOINT [ "python" ]
CMD ["app.py"]