FROM nvidia/cuda:10.1-cudnn7-devel

# system tools
RUN apt-get update \ 
    && apt-get upgrade -y \
    && apt-get install -y \
    wget \
    git

# install python
RUN apt-get install -y \
    python3.7 \
    python3-pip

# install dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN python3.7 -m pip install -r requirements.txt

