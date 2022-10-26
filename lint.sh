#!/bin/bash

pip install pylint flake8 pycodestyle isort black autoflake
echo "Running black"
black .
echo "Running autoflake"
autoflake --remove-unused-variables --remove-all-unused-imports --in-place --recursive .
echo "Running pylint"
pylint .
echo "Running flake8"
flake8 --max-line-length=200 .
echo "Running pycodestyle"
pycodestyle --max-line-length=200 .
echo "Running isort"
isort .
