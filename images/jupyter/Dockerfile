FROM minh5/spark

RUN apt-get install -y python3 python3-pip python3-dev

COPY ./requirements.txt root/

# configure extensions
RUN pip3 install -r /root/requirements.txt && \
    jupyter nbextensions_configurator enable --user && \
    jupyter contrib nbextension install --user && \
    jupyter nbextension enable codefolding/main

# make directory to store notebooks
RUN mkdir -p root/notebooks && \
    chmod +x root/docker-entrypoint.sh

EXPOSE 8888
VOLUME root/notebooks

COPY docker-entrypoint.sh root/
ENTRYPOINT ["root/docker-entrypoint.sh"]