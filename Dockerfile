FROM alpine:latest
RUN apk add --no-cache gcc musl-dev bash wget git \
	  py-pip python3 python3-dev postgresql-dev \
	  nginx uwsgi uwsgi-python \
	&& apk add --virtual scipy-build \
        build-base openblas-dev freetype-dev pkgconfig gfortran \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
	&& apk del scipy-build \
    && apk add --virtual scipy-runtime \
        freetype libgfortran libgcc libpng  libstdc++ musl openblas tcl tk \
    && rm -rf /var/cache/apk/*

RUN wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
RUN mkdir /src
ADD src/ /src/
RUN pip install --upgrade pip \
	&& pip install -r src/requirements.txt
ENV APP_DIR /src
ENV FLASK_APP /src/app.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
