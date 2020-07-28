FROM python:3.7-stretch
LABEL maintainer="Woodmac"

# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=1.10.9
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

# Disable noisy "Handling signal" log messages:
# ENV GUNICORN_CMD_ARGS --log-level WARNING

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_USER_HOME} airflow \
    && pip install -U pip setuptools wheel \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install requests \
    && pip install spark \
    && pip install boto3 \
    && pip install apache-airflow[crypto,celery,postgres,hive,jdbc,mysql,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION} \
    && pip install 'redis==3.2' \
    && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi \
    && pip uninstall -y SQLAlchemy \
    && pip install SQLAlchemy==1.3.15 \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY script/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg

RUN chown -R airflow: ${AIRFLOW_USER_HOME}

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]

USER root

# Install Java
RUN apt-get update \
	&& apt-get -y install sudo

RUN mkdir -p /usr/share/man/man1

RUN sudo mkdir -p /var/lib/apt/lists/partial \
    && apt-get install --no-install-recommends -y openjdk-8-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

ARG SPARK_VERSION=2.4.1
ARG HADOOP_VERSION=2.6.5
ARG SPARK_PY4J=python/lib/py4j-0.10.4-src.zip

ARG hadoop_home=/opt/hadoop
ENV HADOOP_HOME=${hadoop_home}
ENV PATH=${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin

ENV SPARK_HOME=/opt/spark-${SPARK_VERSION}
ENV PATH=$PATH:${SPARK_HOME}/bin
ENV PYTHONPATH=${SPARK_HOME}/${SPARK_PY4J}:${SPARK_HOME}/python
ENV PYSPARK_SUBMIT_ARGS="--driver-memory 8g --py-files ${SPARK_HOME}/python/lib/pyspark.zip pyspark-shell"

# Download Spark
ARG SPARK_EXTRACT_LOC=/sparkbin
RUN ["/bin/bash", "-c", "set -eoux pipefail && \
    (curl https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | \
    tar -xz -C /opt/) && \
    mv /opt/hadoop-${HADOOP_VERSION} /opt/hadoop && \
    mkdir -p ${SPARK_EXTRACT_LOC} && \
    (curl https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION:0:3}.tgz | \
    tar -xz -C ${SPARK_EXTRACT_LOC}) && \
    mkdir -p ${SPARK_HOME} && \
    mv ${SPARK_EXTRACT_LOC}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION:0:3}/* ${SPARK_HOME} && \
    rm -rf ${SPARK_EXTRACT_LOC} && \
    echo SPARK_HOME is ${SPARK_HOME} && \
    ls -al --g ${SPARK_HOME}"]