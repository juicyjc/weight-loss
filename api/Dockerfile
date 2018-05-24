#
# weightloss-api Dockerfile
#
#

# Pull base image.
FROM python:3.6-slim

# Get some custom packages
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    gcc \
    python3-dev \
    mongodb

## make a local directory
RUN mkdir /opt/api

# set "api" as the working directory from which CMD, RUN, ADD references
WORKDIR /opt/api

# now copy all the files in this directory to /code
ADD . .

# pip install the local requirements.txt
RUN pip install -r requirements.txt

# Listen to port 5000 at runtime
EXPOSE 5000

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1

# start the app server
CMD python manage.py runserver
