#!/bin/bash

wget http://www.clips.uantwerpen.be/conll2000/chunking/train.txt.gz
wget http://www.clips.uantwerpen.be/conll2000/chunking/test.txt.gz
gunzip train.txt.gz
gunzip test.txt.gz

pip install -r requirements.txt
