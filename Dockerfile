FROM python:3.9.7-alpine3.14

# load source code into image
RUN mkdir /hoops
COPY hoops /hoops
# only copy production requirements
COPY requirements/prod.txt /requirements.txt
# Enable easy dev on active container by using a bind mount via -v
# to give the container access to the source code on your machine
# For example, assuming you have a project directory structure like this:
# .
# |_ Dockerfile
# |_ README
# |_ .gitignore
# |_ .env/ ... python environment, local only
# |_ .python-version
# |_ requirements.txt
# |_ .pylintrc
# |_ hoops/
#   |_ app.py
#     ... more application files here
#
# and you wanted to be able to develop the application files while
# running a container for dev purposes, you would bind the ./hoops
# directory in your project directory to the container's /hoops
# directory using `docker run -v ./hoops:/hoops ...` from your project root
VOLUME /hoops

# install python dependencies
RUN apk add --no-cache --virtual .build-deps \
    # needed to build psycopg2 & yarl
    gcc \
    # needed to build yarl
    musl-dev \
    # needed to build psycopg2
    postgresql-dev \
    # runtime dependency for psycopg2
    && apk add --no-cache libpq \
    # install python packages
    && pip install -r requirements.txt \
    # then remove build dependencies
    && apk del .build-deps

# start server
WORKDIR /hoops
ENTRYPOINT ["python"]
# tell flask to use 0.0.0.0 instead of localhost to allow 
# connections from outside docker container
CMD ["-m", "flask", "run", "--host=0.0.0.0"]
