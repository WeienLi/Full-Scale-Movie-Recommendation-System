FROM jupyter/pyspark-notebook:latest

COPY . .
RUN pip3 install -r requirements.txt

CMD  ["python", "-m", "flask", "--app=flask_API/main.py", "run", "--host=0.0.0.0", "--port=8082"]