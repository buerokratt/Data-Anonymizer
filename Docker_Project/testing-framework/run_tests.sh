#!/bin/bash

PING_ENDPOINT="${PING_ENDPOINT:-http://resql:8082/healthz}"
while true; do
    status_code=$(curl --write-out %{http_code} --silent --output /dev/null $PING_ENDPOINT)

    if [[ "$status_code" -ne 200 ]] ; then
        echo "Waiting for resql to boot..."
    else
        echo "Resql started. Executing Tests."
        sleep 5
        break
    fi
    sleep 5
done
npm test