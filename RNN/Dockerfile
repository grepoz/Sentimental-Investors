# have to be < python:3.10.0 because of pytorch comatibility
FROM python:3.10.0
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt  # RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=main.py
CMD python -u src/main.py