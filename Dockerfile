FROM python:3.10-bullseye
RUN apt-get install -y default-libmysqlclient-dev
COPY src/requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
COPY src src
RUN python3 -m pip install src/
CMD ["get_raw_data"]
