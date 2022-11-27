FROM continuumio/miniconda3

# add user
RUN useradd -ms /bin/bash user
USER user

WORKDIR /Team-3

RUN conda create -n tf tensorflow
SHELL ["conda", "run", "-n", "tf", "/bin/bash", "-c"]
RUN python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))" \
    && pip install --upgrade pip \
    && pip install gunicorn

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=user . /Team-3

ENTRYPOINT  ["conda", "run", "--no-capture-output", "-n", "tf", "gunicorn", "-w", "1", "--bind", "0.0.0.0:8082", "--timeout", "90", "flask_API:app", "--log-level", "debug"]
