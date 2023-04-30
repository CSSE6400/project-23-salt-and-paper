FROM ubuntu:20.04
# Installing dependencies and cleaning up
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip postgresql-client libpq-dev libcurl4-openssl-dev libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Install pipenv
RUN pip3 install pipenv
# Setting the working directory and copying the files
WORKDIR /app
COPY . /app
# Installing dependencies and running the application
RUN pipenv install --system --deploy --ignore-pipfile
CMD ["/app/bin/docker-entrypoint", "serve"]