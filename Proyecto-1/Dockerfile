FROM python:3.14

WORKDIR /app
COPY requirements.txt .
COPY prueba.txt /app/prueba.txt

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000"]