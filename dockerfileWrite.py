
import json

f = open('aiomaticConfig.json','r',encoding = 'utf-8')

allInfo = json.loads(f.read())

packageInfoString = "FROM " + (allInfo.get('data')).get('languageVersion') + "\n"


with open("Dockerfile",'w',encoding = 'utf-8') as f:
   f.write(packageInfoString)
   f.write("ADD . /usr/src/app\n")
   f.write("WORKDIR /usr/src/app\n")
   f.write("COPY requirements.txt ./\n")
   f.write("RUN pip install --no-cache-dir -r requirements.txt\n")
   f.write("EXPOSE 8000\n")
   f.write("CMD gunicorn aiomatic.wsgi:application --bind 0.0.0.0:8000\n")
