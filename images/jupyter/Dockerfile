FROM minh5/spark

RUN apt-get install -y python3-pip

COPY ./requirements.txt root/

# configure extensions
RUN pip3 install -r /root/requirements.txt && \
    jupyter nbextensions_configurator enable --user && \
    jupyter contrib nbextension install --user && \
    jupyter nbextension enable codefolding/main

# make directory to store notebooks
RUN mkdir -p root/notebooks && \
    chmod +x root/docker-entrypoint.sh

# set for pyspark notebook
ENV PYSPARK_DRIVER_PYTHON jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS 'notebook'
ENV SPARK_OPTS --driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info

EXPOSE 8888
VOLUME root/notebooks

COPY docker-entrypoint.sh root/
ENTRYPOINT ["root/docker-entrypoint.sh"]