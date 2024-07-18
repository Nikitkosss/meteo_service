FROM python:3.9

WORKDIR /app

COPY requirements.txt /app
COPY app.py /app
COPY templates /app/templates

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "app.py"]
