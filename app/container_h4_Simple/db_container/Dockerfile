FROM postgres:latest
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=artigow_db
COPY init.sql /docker-entrypoint-initdb.d/
VOLUME /var/lib/postgresql/data
