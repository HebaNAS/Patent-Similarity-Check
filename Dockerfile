# VERSION 1.10.2
# AUTHOR: Matthieu "Puckel_" Roisil
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t puckel/docker-airflow .
# SOURCE: https://github.com/puckel/docker-airflow

# Base image
FROM puckel/docker-airflow:1.10.2
# FROM puckel/docker-airflow@sha256:82654d8b384be9fe79cca5d41a599cf1d2504c7e57b3d97cb577b978dcf84779
LABEL maintainer="Puckel_"

# Set user as root
USER root

# Set shell to bash
SHELL ["/bin/bash", "-c"]

# Copy python requirements file inside the container
COPY requirements.txt /requirements.txt

# Copy needed scripts inside the container
COPY ./sources.list.append .
COPY ./chemspot-script.sh .
COPY ./opsin-script.sh .

# Append a new debian packages repository to current sources list and delete the old file
RUN cat ./sources.list.append >> /etc/apt/sources.list && rm -f ./sources.list.append

# Move needed scripts to where the system in the container expects them
RUN mv ./chemspot-script.sh /usr/local/bin/
RUN mv ./opsin-script.sh /usr/local/bin/

# Create folder for library manuals
RUN mkdir -p /usr/share/man/man1

# Install linus dependencies
RUN apt-get clean \
	&& apt-get update -yq \
	&& apt-get dist-upgrade -yq \
	&& apt-get upgrade -yq \
	&& apt-get install -yq \
	sudo \
	wget \
	zip \
	unzip \
	git \
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
	libleptonica-dev \
	python-numpy \
	python-scipy \
	python-opengl \
	cython \
	python-matplotlib \
	python-qt4-gl \
	python-qt4 \
	libbz2-dev \
	libfreetype6-dev \
	ghostscript \
	gsfonts \
	libjbig-dev \
	liblcms2-dev \ 
	libltdl-dev \
	liblzma-dev \
	libtiff5-dev \
	libwebp-dev \
	libwmf-dev \
	libx11-dev \
	libxext-dev \
	libsm-dev \
	libxml2-dev \
	lzip \
	libmagic1 \
	libmagic-dev \
	openjdk-8-jre \
	cython \
	cython3 \
	python-setuptools \
	cmake \
	fontconfig \
	libfontconfig1-dev \
	libopenjp2-7-dev \
	openbabel \
	libopenbabel4v5 \
	libopenbabel-dev \
	libboost-dev \
	libboost-all-dev \
	python-rdkit \
	librdkit1 \
	rdkit-data

# Install python dependencies
RUN pip install Cython setuptools

# Install libraries (from source) needed by OSRA - Chemical structure OCR
RUN wget https://sourceforge.net/projects/graphicsmagick/files/graphicsmagick/1.3.33/GraphicsMagick-1.3.33.tar.gz/download \
	&& tar -xvzf ./download \
	&& cd ./GraphicsMagick-1.3.33 \
	&& cp Magick++/lib/Magick++.h /usr/local/lib/ \
	&& cp -r Magick++/lib/Magick++ /usr/local/lib/ \
	&& export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/ \
	&& sudo ldconfig \
	&& sudo ./configure --enable-shared \
	&& sudo make -j4 \
	&& sudo make install \
	&& cd ../ \
	&& rm -r ./GraphicsMagick-1.3.33 \
	&& rm ./download

RUN wget http://potrace.sourceforge.net/download/1.15/potrace-1.15.tar.gz \
	&& tar -xvzf ./potrace-1.15.tar.gz \
	&& cd ./potrace-1.15 \
	&& sudo ./configure --with-libpotrace --disable-shared \
	&& sudo make -j4 \
	&& sudo make install \
	&& cd ../ \
	&& rm -r ./potrace-1.15 \
	&& rm ./potrace-1.15.tar.gz

RUN wget https://cactus.nci.nih.gov/osra/gocr-0.50pre-patched.tgz \
	&& tar -xvzf ./gocr-0.50pre-patched.tgz \
	&& cd ./gocr-0.50pre-patched \
	&& ./configure \
	&& make -j4 libs \
	&& sudo make install \
	&& cd ../ \
	&& rm -r ./gocr-0.50pre-patched ./gocr-0.50pre-patched.tgz

RUN wget http://mirror.squ.edu.om/gnu/ocrad/ocrad-0.27.tar.lz \
	&& tar --lzip -xvf ./ocrad-0.27.tar.lz \
	&& cd ./ocrad-0.27 \
	&& ./configure \
	&& make -j4 \
	&& sudo make install \
	&& cd ../ \
	&& rm -r ./ocrad-0.27 ./ocrad-0.27.tar.lz

RUN wget https://sourceforge.net/projects/tclap/files/tclap-1.2.2.tar.gz/download \
	&& tar -xvzf ./download \
	&& cd ./tclap-1.2.2 \
	&& ./configure \
	&& make -j4 \
	&& sudo make install \
	&& cd ../ \
	&& rm -r ./tclap-1.2.2 ./download

RUN wget https://poppler.freedesktop.org/poppler-data-0.4.9.tar.gz \
	&& tar -xvzf ./poppler-data-0.4.9.tar.gz \
	&& cd ./poppler-data-0.4.9 \
	&& sudo make install \
	&& cd ../ \
	&& rm -r ./poppler-data-0.4.9 ./poppler-data-0.4.9.tar.gz

RUN wget https://poppler.freedesktop.org/poppler-0.79.0.tar.xz \
	&& tar xf ./poppler-0.79.0.tar.xz \
	&& cd ./poppler-0.79.0 \
	&& mkdir build \
	&& export PKG_CONFIG_PATH=$(apt-file search fontconfig.pc) \
	&& sudo ldconfig \
	&& cd build \
	&& sudo cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=release \
	&& sudo make \
	&& sudo make install \
	&& cd ../../ \
	&& rm -r ./poppler-0.79.0 ./poppler-0.79.0.tar.xz

# Install Tesseract OCR from source
RUN wget http://deb.debian.org/debian/pool/main/t/tesseract/tesseract_4.0.0.orig.tar.xz \
	&& tar xf tesseract_4.0.0.orig.tar.xz \
	&& cd tesseract-4.0.0 \
	&& ./autogen.sh \
	&& ./configure \
	&& make \
	&& sudo make install \
	&& cd ../ \
	&& rm -r tesseract-4.0.0 \
	&& rm tesseract_4.0.0.orig.tar.xz

RUN wget http://deb.debian.org/debian/pool/main/t/tesseract-lang/tesseract-lang_4.00~git30-7274cfa.orig.tar.xz \
	&& tar xf tesseract-lang_4.00~git30-7274cfa.orig.tar.xz \
	&& mv tesseract-lang-4.00~git30-7274cfa/* /usr/local/share/tessdata/ \
	&& cd ../ \
	&& rm -rf tesseract-lang-4.00~git30-7274cfa \
	tesseract-lang_4.00~git30-7274cfa.orig.tar.xz \
	&& sudo ldconfig

# Install OSRA from source (chemical srtucture OCR library)
RUN wget https://sourceforge.net/projects/osra/files/latest/download \
	&& tar -xvzf ./download \
	&& cd ./osra-2.1.0-1 \
	&& ./configure --with-tesseract \
	&& make -j4 \
	&& sudo make install \
	&& cd ../ \
	&& rm -r ./osra-2.1.0-1 ./download

# INstall Chemspot (Chemical named entity recognition library)
RUN wget http://www.informatik.hu-berlin.de/forschung/gebiete/wbi/resources/chemspot/chemspot-2.0.zip \
	&& unzip ./chemspot-2.0.zip \
	&& cd ./chemspot-2.0 \
	&& cp ./chemspot.jar /usr/local/bin \
	&& export CHEMSPOT_DATA_PATH=~/chemspot-2.0

# Install Opsin (Parser for IUPAC chemical nomenclature)
RUN wget https://bitbucket.org/dan2097/opsin/downloads/opsin-2.4.0-jar-with-dependencies.jar \
	&& mv opsin-2.4.0-jar-with-dependencies.jar /usr/local/bin/opsin.jar

# Put changes into efferct
RUN sudo ldconfig

# Install python dependencies from requirements file
RUN pip install --upgrade pip
RUN pip install --default-timeout=1000 -r /requirements.txt

# Open ports on container to be accessible (airflow 8080, jupyter 8888)
EXPOSE 8080 8888

# Revert user to airflow and drop privileges (better for security for containers running in clusters)
# Commented out due to permission problems when running airflow scripts
USER airflow

