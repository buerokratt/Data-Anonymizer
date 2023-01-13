#!/bin/bash
chmod +x listen_server.sh
chmod +x start_server.sh
./start_server.sh & if [[ -n "$STARTUP_ENDPONT" ]]; then ./listen_server.sh; fi && wait