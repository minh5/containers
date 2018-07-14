#!/bin/bash
# install jupyter and libraries
CONFIG_DIR="/tmp/config"
USER_HOME="/home/user"

pip3 install --no-cache -r ${CONFIG_DIR}/requirements.txt
jupyter nbextensions_configurator enable --user
jupyter contrib nbextension install --user
jupyter nbextension enable codefolding/main
if [[ -e ${CONFIG_DIR}/jupyter_notebook_config.py ]]; then
    mkdir -p $USER_HOME/.jupyter
    cp ${CONFIG_DIR}/jupyter_notebook_config.py $USER_HOME/.jupyter/
    chown -R user $USER_HOME && cd $USER_HOME
else
    echo "ERROR: Could not find jupyter_notebook_config.py in $CONFIG_DIR"
    exit 1
fi

# install scala kernel
git clone https://github.com/jupyter-scala/jupyter-scala.git
cd jupyter-scala
./jupyter-scala