FROM python:3.10
WORKDIR /insta
COPY requirements.txt /insta/
RUN pip install -r requirements.txt
COPY . /insta
CMD python insta.py
