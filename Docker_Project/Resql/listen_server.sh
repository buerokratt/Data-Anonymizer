#!/bin/bash

PING_ENDPOINT="${PING_ENDPOINT:-http://localhost:8082/healthz}"
while true; do
    status_code=$(curl --write-out %{http_code} --silent --output /dev/null $PING_ENDPOINT)

    if [[ "$status_code" -ne 200 ]] ; then
        echo "Server not started"
    else
        echo "Server started. Launching startup script"
        curl --silent -X 'POST' $STARTUP_ENDPONT
        echo "Startup script finished"
        break
    fi
    sleep 5
done