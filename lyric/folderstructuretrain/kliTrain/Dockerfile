FROM python:3.11.4
WORKDIR /code
RUN apt-get update
RUN apt-get -y install gcc
COPY ./requirements.txt /code/requirements.txt
RUN pip install -U pip wheel cmake
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY . /code/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
