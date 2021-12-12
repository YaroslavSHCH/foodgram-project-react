FROM python:3.9
LABEL author="rorshih@gmail.com"
WORKDIR /backend
COPY . .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000