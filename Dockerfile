# VERSION 1.10.2
# AUTHOR: Matthieu "Puckel_" Roisil
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t puckel/docker-airflow .
# SOURCE: https://github.com/puckel/docker-airflow

FROM puckel/docker-airflow:1.10.2
LABEL maintainer="Puckel_"

USER root

COPY requirements.txt /requirements.txt

RUN apt-get update -yq \
    && apt-get upgrade -yq \
    && apt-get install -yq \
        sudo \
        poppler-utils \
        tesseract-ocr \
        imagemagick
    
RUN pip install -r /requirements.txt

CMD mkdir /usr/local/share/nltk_data

RUN python -m nltk.downloader -d /usr/local/share/nltk_data popular

EXPOSE 8080 8888 5555 8793

USER airflow
