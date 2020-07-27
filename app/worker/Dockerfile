FROM alpine:latest
RUN apk add --no-cache gcc musl-dev bash wget git \
      gfortran openblas-dev lapack-dev \
	  py-pip python3 python3-dev postgresql-dev \
	&& apk add --virtual scipy-build \
        build-base openblas-dev freetype-dev pkgconfig gfortran \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
	&& apk del scipy-build \
    && apk add --virtual scipy-runtime \
        freetype libgfortran libgcc libpng  libstdc++ musl openblas tcl tk \
    && rm -rf /var/cache/apk/*

RUN pip install --upgrade pip setuptools wheel
RUN wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
RUN mkdir /src
ADD src/ /src/
RUN pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl
RUN pip install --upgrade pip \
	&& pip install --no-use-pep517 -r src/requirements.txt
ENV APP_DIR /src
CMD ["python", "/src/main.py"]
