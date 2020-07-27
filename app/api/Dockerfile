FROM alpine:latest
RUN apk add --no-cache gcc bash wget git \
      musl-dev postgresql-dev \
	  py-pip python3 python3-dev \
	  nginx uwsgi uwsgi-python \
    && rm -rf /var/cache/apk/*

RUN pip install --upgrade pip setuptools wheel
RUN mkdir /src
ADD src/ /src/
RUN pip install --upgrade pip \
	&& pip install -r src/requirements.txt
ENV APP_DIR /src
ENV FLASK_APP /src/api.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
