#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

DATASET_NAME=$1
echo "Downloading $DATASET_NAME ground truth data"

wget http://pascal.inrialpes.fr/data2/act-detector/downloads/cache/$DATASET_NAME-GT.pkl

echo "Done."

