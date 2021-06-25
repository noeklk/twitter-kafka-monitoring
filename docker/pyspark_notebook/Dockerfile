FROM jupyter/pyspark-notebook:python-3.8.8

COPY ./requirements.txt .
RUN pip install -r requirements.txt
#RUN spark-submit --packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.0.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 sparkJob.py
#RUN spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 ...