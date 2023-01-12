#!/bin/bash

./start_server.sh & if [[ -n "$STARTUP_ENDPONT" ]]; then ./listen_server.sh; fi && wait