FROM python:3.9
MAINTAINER Lucian Murphy "lucian@uoregon.edu"
RUN apt-get update -y

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["flask_brevets.py"]
