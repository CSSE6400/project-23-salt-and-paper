# project-23-salt-and-paper

## Requirements

1. Install PSQL : https://www.timescale.com/blog/how-to-install-psql-on-mac-ubuntu-debian-windows/
2. Install the latest PgAdmin : https://www.pgadmin.org/docs/pgadmin4/development/pgagent_install.html

## Set-Up - Run with Docker Compose 

1. Uncomment the `db_uri` variable that is set for running with docker. Set the hostname to your IP address if 'db' doesn't work.

2. Make sure you have Docker desktop and WSL installed.

3. Run the docker containers using : `docker-compose up --build` or `sudo docker-compose up --build`

4. Open the `endpoints.http` file and run each of the endpoints. You should get a 200 Response Code for each of the health endpoints.

## Set-Up - Run Locally

1. Uncomment the `db_uri` variable that is set for running without docker.

2. Use the `environment.yml` file to create a conda environment with the required packages for this project:

   `conda env create --name envname --file=environments.yml`

3. Run this command to start the backend server:

   `flask --app backend run -p 6400`

4. Check that the service endpoints are running successfully on your local machine. These are the steps to follow if you use VSCode (you can check the endpoints using CURL or Postman as well):

   1. Ensure that the flask app is still running and open a new terminal.

   2. Go to the Extensions tab in VSCode and install "Rest Client" by Huachao Mao.

   3. Open the `endpoints.http` file and run each of the endpoints. You should get a 200 Response Code for each of the health endpoints.
