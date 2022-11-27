FROM python:alpine

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip \
    && pip install pykafka \
    && pip install redis \
    && pip install prometheus_client \
    && pip install supabase==0.7.1

WORKDIR /Team-3
COPY . .
ENTRYPOINT ["python", "-m", "kafka_consumer.monitor.py"]