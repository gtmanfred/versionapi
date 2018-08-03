FROM python:3.6
WORKDIR /versionapi/
COPY . .
RUN pip install -r requirements.txt
RUN pip install .
