FROM python:alpine

WORKDIR /Team-3

COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

CMD  ["gunicorn", "-w", "2", "--bind", "0.0.0.0:8082", "flask_API:app"]