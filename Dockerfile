FROM python:3.7.1-slim
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY . /aiomatic
WORKDIR /aiomatic
CMD python manage.py runserver