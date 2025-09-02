FROM python:3.9.23

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

# cache big packages
RUN pip install nvidia-cublas-cu12==12.8.4.1
RUN pip install nvidia-cudnn-cu12==9.10.2.21
RUN pip install nvidia_cufft_cu12==11.3.3.83
RUN pip install nvidia_cusolver_cu12==11.7.3.90
RUN pip install nvidia_cusparse_cu12==12.5.8.93
RUN pip install nvidia_cusparselt_cu12==0.7.1
RUN pip install nvidia_nccl_cu12==2.27.3
RUN pip install MarkupSafe-3.0.2filelock==3.19.1
RUN pip install fsspec==2025.7.0
RUN pip install importlib-metadata==8.7.0
RUN pip install jinja2==3.1.6
RUN pip install mpmath==1.3.0
RUN pip install networkx==3.2.1
RUN pip install nvidia-cublas-cu12==12.8.4.1
RUN pip install nvidia-cuda-cupti-cu12==12.8.90
RUN pip install nvidia-cuda-nvrtc-cu12==12.8.93
RUN pip install nvidia-cuda-runtime-cu12==12.8.90
RUN pip install nvidia-cudnn-cu12==9.10.2.21
RUN pip install nvidia-cufft-cu12==11.3.3.83
RUN pip install nvidia-cufile-cu12==1.13.1.3
RUN pip install nvidia-curand-cu12==10.3.9.90
RUN pip install nvidia-cusolver-cu12==11.7.3.90
RUN pip install nvidia-cusparse-cu12==12.5.8.93
RUN pip install nvidia-cusparselt-cu12==0.7.1
RUN pip install nvidia-nccl-cu12==2.27.3
RUN pip install nvidia-nvjitlink-cu12==12.8.93
RUN pip install nvidia-nvtx-cu12==12.8.90
RUN pip install sympy==1.14.0
RUN pip install torch==2.8.0
RUN pip install triton==3.4.0
RUN pip install typing-extensions==4.15.0
RUN pip install zipp==3.23.0
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