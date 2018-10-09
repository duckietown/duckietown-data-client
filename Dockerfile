# FROM python:2.7
FROM duckietown/rpi-duckiebot-raspberrypi3-python:master18


COPY requirements.txt /duckietown-data-client/requirements.txt
RUN pip install -r /duckietown-data-client/requirements.txt


COPY src /duckietown-data-client/src
COPY setup.py /duckietown-data-client/setup.py
COPY README.md /duckietown-data-client/README.md


RUN cd /duckietown-data-client && \
    python setup.py install

CMD dt-dc
