FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD gunicorn -b :$PORT --chdir itutor app:app