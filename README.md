# Demo User Registration Rest API

Demo project to show how to to build and design RESTful web services using Python, Flask, Docker and MongoDB.

#End-Points :
This WS is handling a user system registration by exposing endpoints to handle different use-cases:
- '/healthcheck' : return a simple msg to check that the WS is workign fine
- '/register' : handle user inscription 
- '/dashboard' : return data for a specific user
- '/update' : handle personnal user data update
- '/confirm' : handle confirmation mecanisme

## Docker and docker-compose

Inside the root project you can run

```shell
sudo docker-compose build
```

and then run the folowing to start the container and expose the API:

```shell
sudo docker-compose up
```

Once the container is running, you can access it by opening your browser and typing in localhost:5000/healthcheck. This should
display a "Working fine!" message.

## Using postman

When using postman to test your rest endpoints, be sure to add content-type: application/json to your headers.

If you don't want to specify content type in the header then you can use
request.get_json(force=True) inside your endpoint when fetching the data from the request
to force the data to be read as JSON.

## @Todo
- Test mail SMPT 
- Do some code refactor/optimisations 
- Do more TU for specific use-cases
- Test user input data (valid email, valid username ..)
