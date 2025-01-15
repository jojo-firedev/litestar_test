#
# docker run -p 8000:80 -v ".:/app" litestar_api

FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 80

CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "80", "--reload"]
