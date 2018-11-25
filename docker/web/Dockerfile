FROM python:2

RUN mkdir /code
WORKDIR /code

# Copy in your requirements file
ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# dependency to make django and our entrypoint script to work.
RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client \
		postgresql-client libpq-dev \
		sqlite3 \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

ADD . /code
WORKDIR /code
EXPOSE 8000

# Add any custom, static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=coopproject.settings

RUN ["chmod", "+x", "/code/docker/web/docker-entrypoint.sh"]
ENTRYPOINT ["/code/docker/web/docker-entrypoint.sh"]

CMD python manage.py runserver 0.0.0.0:8000