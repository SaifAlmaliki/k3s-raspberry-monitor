FROM python:3.9

RUN pip install psutil pyembedded paho-mqtt

COPY raspi_monitor.py ./

CMD ["python","./raspi_monitor.py"]