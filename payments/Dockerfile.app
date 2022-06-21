# 
FROM python:3.9

LABEL version="1.0"

RUN mkdir /app-payments
RUN mkdir /app-payments/www

WORKDIR /app-payments

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080/tcp

VOLUME /app-payments/www

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

