FROM python:3.9.7

# load source code into image
RUN mkdir /src
COPY src /src
# only copy production requirements
COPY requirements/prod.txt /requirements.txt
VOLUME /src

# install python dependencies
RUN pip install -r requirements.txt

# start server
ENTRYPOINT ["python"]
# tell fastapi to use 0.0.0.0 instead of localhost to allow
# connections from outside docker container
CMD ["-m", "uvicorn", "src:app", "--host=0.0.0.0"]
