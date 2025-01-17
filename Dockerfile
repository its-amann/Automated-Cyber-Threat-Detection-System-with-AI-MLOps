FROM python:3.10-slim-buster
USER root
RUN mkdir /app
COPY . /app/
WORKDIR /app/
RUN pip3 install -r requirements.txt
ENV AWS_DEFAULT_REGION = "us-east-1"
ENV BUCKET_NAME="networksecurity3"
ENV PREDICTION_BUCKET_NAME="network-security-prediction"
ENV AIRFLOW_HOME="/app/airflow"
ENV AIRFLOW_CORE_DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW_CORE_ENABLE_XCOM_PICKLING=True
ENV PYTHONPATH="/app:${PYTHONPATH}"
RUN airflow db init
RUN airflow users create -e amanagnihotri902@gmail.com -f aman -l hhhhh -p admin -r Admin -u admin
RUN chmod 777 start.sh
RUN apt update -y
ENTRYPOINT [ "/bin/sh" ]
CMD ["start.sh"]
WORKDIR /app
COPY . /app/
RUN apt update -y && apt install  awscli -y
RUN apt-get update && pip install -r requirements.txt

CMD ["python3", "app.py"]
