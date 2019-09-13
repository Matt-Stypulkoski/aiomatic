# AI-o-matic

Install Django

```
pip install Django
```

To run the project

```
python manage.py runserver
```

To use docker

build the docker image from root directory:
```
docker build --tag aiomatic . 
```
run the docker image
```
docker run --name aiomatic-app -p 8000:8000 aiomatic
```
`aiomatic-app` is the container name.

and go to http://127.0.0.1:8000/aiomaticProject/

To stop `docker run`, open another terminal in you working directory and run:
```
docker stop aiomatic-app
``` 
