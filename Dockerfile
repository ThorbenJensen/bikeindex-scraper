FROM nvidia/cuda:10.1-cudnn7-devel

# system tools
RUN apt-get update \ 
    && apt-get upgrade -y \
    && apt-get install wget -y

# install miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda2-4.5.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

# build environment
# RUN conda env create -f environment.yml && \
#     activate bikeindex-scraper

# mount project folder
# TODO

RUN [ "/bin/bash" ]
