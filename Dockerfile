FROM python:3.9 

# RUN apt-get update && apt-get install -y postgresql-client libpq-dev 
RUN apt-get update && \
        apt-get install -y  postgresql-client libpq-dev libcurl4-openssl-dev libssl-dev && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*

RUN pip install pipenv

# Setting the working directory 
WORKDIR . 

# Install pipenv dependencies 
COPY Pipfile Pipfile.lock recipes.json ratings.json users.json ./ 
RUN pipenv install --system --deploy --ignore-pipfile

# Copying our application into the container 
COPY backend backend
COPY frontend frontend

ARG SQLALCHEMY_DATABASE_URI
ARG JSON_SORT_KEYS
ARG CELERY_BROKER_URL
ARG CELERY_RESULT_BACKEND
ENV SQLALCHEMY_DATABASE_URI=$SQLALCHEMY_DATABASE_URI
ENV JSON_SORT_KEYS=$JSON_SORT_KEYS
ENV CELERY_BROKER_URL=$CELERY_BROKER_URL
ENV CELERY_RESULT_BACKEND=$CELERY_RESULT_BACKEND

# Running our application 
CMD ["sh", "-c", "sleep 3 && gunicorn -b 0.0.0.0:6400 backend:app"]