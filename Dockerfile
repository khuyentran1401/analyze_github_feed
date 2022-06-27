FROM python:3.8-buster

RUN mkdir -p /usr/src/app 

COPY . /usr/src

WORKDIR /usr/src

RUN pip install -r requirements.txt 

ENTRYPOINT ["streamlit", "run", "streamlit_app.py"]