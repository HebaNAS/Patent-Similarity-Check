# VERSION 1.10.2
# AUTHOR: Matthieu "Puckel_" Roisil
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t puckel/docker-airflow .
# SOURCE: https://github.com/puckel/docker-airflow

FROM puckel/docker-airflow:1.10.2
LABEL maintainer="Puckel_"

USER root

COPY requirements.txt /requirements.txt

COPY ./sources.list.append .
RUN cat ./sources.list.append >> /etc/apt/sources.list  && rm -f ./sources.list.append

RUN apt-get clean \
        && apt-get update -yq \
        && apt-get dist-upgrade -yq \
        && apt-get upgrade -yq \
        && apt-get install -yq \
        sudo \
        wget \
        poppler-utils \
        tesseract-ocr \
        libtesseract-dev \
        imagemagick \
        libsm6 \
        libxext6 \
        libxrender-dev \
        xz-utils \
        g++ \
        autoconf \
        automake \
        libtool \
        pkg-config \
        libpng-dev \
        libjpeg62-turbo-dev \
        libtiff5-dev \
        zlib1g-dev \
        libleptonica-dev

RUN wget http://deb.debian.org/debian/pool/main/t/tesseract/tesseract_4.0.0.orig.tar.xz \
        && tar xf tesseract_4.0.0.orig.tar.xz \
        && cd tesseract-4.0.0 \
        && ./autogen.sh \
        && ./configure \
        && make \
        && make install

RUN wget http://deb.debian.org/debian/pool/main/t/tesseract-lang/tesseract-lang_4.00~git30-7274cfa.orig.tar.xz \
        && tar xf tesseract-lang_4.00~git30-7274cfa.orig.tar.xz \
        && mkdir tesserdata \
        && mv tesseract-lang-4.00~git30-7274cfa/* /usr/local/share/tessdata/ \
        && rm -rf tesseract-lang-4.00~git30-7274cfa \
        tesseract-lang_4.00~git30-7274cfa.orig.tar.xz \
        tesseract_4.0.0.orig.tar.xz \
        tesseract-4.0.0

RUN ldconfig

RUN pip install --upgrade pip
RUN pip install --default-timeout=1000 -r /requirements.txt

CMD mkdir /usr/local/share/nltk_data

RUN python -m nltk.downloader -d /usr/local/share/nltk_data popular

EXPOSE 8080 8888 5555 8793

USER airflow
