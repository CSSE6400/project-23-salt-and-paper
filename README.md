# project-23-salt-and-paper

## Set-Up

1. Use the `environment.yml` file to create a conda environment with the required packages for this project:

    `conda env create --name envname --file=environments.yml`

2. Run this command to start the backend server:

    `flask --app backend run -p 6400`

3. Check that the service endpoints are running successfully on your local machine. These are the steps to follow if you use VSCode (you can check the endpoints using CURL or Postman as well):

    1. Ensure that the flask app is still running and open a new terminal.

    2. Go to the Extensions tab in VSCode and install "Rest Client" by Huachao Mao.

    3. Open the `endpoints.http` file and run each of the endpoints. You should get a 200 Response Code for each of the health endpoints.
