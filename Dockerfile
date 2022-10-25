FROM continuumio/miniconda3

# add user
RUN useradd -ms /bin/bash user
USER user

WORKDIR /Team-3

# Install conda+tensorflow
RUN conda create -n tf tensorflow
SHELL ["conda", "run", "-n", "tf", "/bin/bash", "-c"]
RUN python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

ENTRYPOINT  ["conda", "run", "--no-capture-output", "-n", "tf", "gunicorn", "-w", "1", "--bind", "0.0.0.0:8082", "--timeout", "90", "flask_API:app", "--log-level", "debug"]