FROM python:3.7
COPY kafka /opt/kafka
COPY producer/* /opt/
RUN pip install -r /opt/requirements.txt
CMD  python /opt/producer.py
