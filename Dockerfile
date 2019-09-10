FROM python:3.7.4-buster

# install basic tools
RUN apt-get update
RUN apt-get install -yq \
    vim

# set up murphy
RUN mkdir /home/murphy
ENV HOME=/home/murphy
ENV USER=murphy
WORKDIR /home/murphy

# install requirements
ADD ./requirements.txt /home/murphy/requirements.txt
RUN pip install -r /home/murphy/requirements.txt --src /usr/local/src

# install library
ADD ./hermes /home/murphy/hermes
ADD ./main.py /home/murphy/main.py
ADD ./setup.py /home/murphy/setup.py
RUN pip install -e .

# create necessary runtime directories
RUN mkdir /home/murphy/logs
RUN mkdir /home/murphy/cache

# setup default command
CMD ["python", "/home/murphy/main.py"]