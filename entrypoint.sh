#!/usr/bin/env bash

echo python -m loolmonitor \
        -w "http://${serveur}/alfresco/s/" \
        -u "${username}" \
        -p "${password}"

python -m loolmonitor \
        -w "http://${serveur}/alfresco/s/" \
        -u "${username}" \
        -p "${password}"

