FROM python:3.9

# Configure apt and install packages
RUN apt-get update -y && \
    apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    git \
    # cleanup
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists

RUN pip install nvidia-cublas-cu12
RUN pip install nvidia-cudnn-cu12
RUN pip install nvidia_cufft_cu12
RUN pip install nvidia_cusolver_cu12
RUN pip install nvidia_cusparse_cu12
RUN pip install nvidia_cusparselt_cu12
RUN pip install nvidia_nccl_cu12
RUN pip install torch
RUN pip install spacy
RUN pip install sentence-transformers
    
    
WORKDIR /converters/term-extractor
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /converters/term-extractor/requirements.txt
RUN export PYTHONPATH=$PYTHONPATH:/converters/term-extractor

COPY . .

ENTRYPOINT [ "python" ]
CMD ["app.py"]