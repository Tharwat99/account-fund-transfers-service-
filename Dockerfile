FROM python:3.12.0a2-alpine3.16
LABEL org.opencontainers.image.authors="sarwatm225@gmail.com"
ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

EXPOSE 8000

CMD python manage.py runserver