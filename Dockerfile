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
COPY Pipfile Pipfile.lock recipes.json ratings.json steps.json users.json ./ 
RUN pipenv install --system --deploy --ignore-pipfile

# Copying our application into the container 
COPY backend backend
COPY frontend frontend

# Running our application 
CMD ["bash", "-c", "sleep 1 && flask --app backend run --debug --host 0.0.0.0 --port 6400"]