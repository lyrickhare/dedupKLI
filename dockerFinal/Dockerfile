FROM python:3.11.3
WORKDIR /code
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY ./requirements.txt /code/requirements.txt
RUN pip install -U pip wheel cmake
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apt-get install -y tesseract-ocr
RUN apt-get install vim -y
COPY ./app /code/app
COPY . /code/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
