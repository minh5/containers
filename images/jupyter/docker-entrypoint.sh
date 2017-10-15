#! /bin/bash
jupyter nbextensions_configurator enable --user && \
jupyter contrib nbextension install --user && \
jupyter nbextension enable codefolding/main
jupyter nbextension enable --py widgetsnbextension --sys-prefix

# useradd -m -s /bin/bash -N -u 1000 user
# USER_HOME="/home/user"
# groupadd supergroup
# usermod -a -G supergroup user

jupyter notebook --no-browser --ip=0.0.0.0 --allow-root
