# Dockerfile

# pull the official docker image
FROM python:3.9.4-slim

RUN mkdir /stock
RUN mkdir /stock/www
# set work directory
WORKDIR /stock

# # set env variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

EXPOSE 8080/tcp

VOLUME /stock/www

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
#ENTRYPOINT ["uvicorn", "stock.main:app"]
CMD ["uvicorn", "stock.main:app", "--host", "0.0.0.0", "--port", "8080"]

