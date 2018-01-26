FROM frolvlad/alpine-python2
 
ENV PYTHONUNBUFFERED 1
RUN mkdir /home/game
RUN pip install flask
RUN pip install flask-restful
RUN pip install docker