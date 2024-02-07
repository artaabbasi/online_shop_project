FROM python:3.12.0a7-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app


COPY .env.prod /app/.env
RUN ls
RUN pwd
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]