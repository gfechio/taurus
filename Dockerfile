FROM alpine:latest
RUN apk add --no-cache bash git python3 nginx uwsgi uwsgi-python py-pip gcc python3-dev musl-dev postgresql-dev \
	&& pip install --upgrade pip \
	&& pip install flask psycopg2 \
	&& pip install flask_restx
RUN mkdir /src
ADD src/ /src/
ENV APP_DIR /src
ENV FLASK_APP /src/app.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
