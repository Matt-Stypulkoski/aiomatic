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
docker build . --tag aiomatic (or some other name) . 
```
run the docker image
```
docker run --name aiomatic-app (or some other name) -p 8000:8000 aiomatic
```

and go to http://127.0.0.1:8000/aiomaticProject/
