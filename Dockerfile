FROM python:3.8-slim

WORKDIR /Team-3
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Verify TensorFlow is installed
RUN python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

CMD  ["gunicorn", "-w", "1", "--bind", "0.0.0.0:8082", "--timeout", "90", "flask_API:app", "--log-level", "debug"]