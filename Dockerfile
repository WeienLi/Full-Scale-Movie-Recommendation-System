FROM python:alpine

WORKDIR /Team-3
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD  ["gunicorn", "-w", "2", "--bind", "0.0.0.0:8082", "--timeout", "90", "flask_API:app", "--log-level", "debug"]