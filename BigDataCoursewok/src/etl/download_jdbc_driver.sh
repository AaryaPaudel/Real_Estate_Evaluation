#!/bin/bash

DRIVER_VERSION="42.7.3"
DRIVER_FILENAME="postgresql-${DRIVER_VERSION}.jar"
DOWNLOAD_URL="https://repo1.maven.org/maven2/org/postgresql/postgresql/${DRIVER_VERSION}/${DRIVER_FILENAME}"

SCRIPT_DIR=$(dirname "$0")

wget -O "${SCRIPT_DIR}/${DRIVER_FILENAME}" "${DOWNLOAD_URL}"

if [ $? -eq 0 ]; then
    echo "Successfully downloaded ${DRIVER_FILENAME} to ${SCRIPT_DIR}"
else
    echo "Failed to download ${DRIVER_FILENAME}"
    exit 1
fi
