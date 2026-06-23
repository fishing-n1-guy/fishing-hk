#!/bin/bash
# Keep the localhost.run tunnel alive
# Restarts it if it dies

URL_FILE="/opt/data/fishing-hk/.tunnel_url"
PID_FILE="/opt/data/fishing-hk/.tunnel_pid"

start_tunnel() {
    # Start the tunnel and capture the URL
    ssh -o StrictHostKeyChecking=accept-new \
        -o ServerAliveInterval=30 \
        -o ServerAliveCountMax=3 \
        -R 80:localhost:9120 \
        nokey@localhost.run 2>&1 | \
    while read line; do
        if [[ "$line" == *".lhr.life"* ]]; then
            url=$(echo "$line" | grep -oP 'https://[a-z0-9]+\.lhr\.life')
            echo "$url" > "$URL_FILE"
            echo "Tunnel URL: $url"
        fi
        echo "$line"
    done
}

# Main loop
while true; do
    echo "Starting tunnel..."
    start_tunnel
    echo "Tunnel died, restarting in 5 seconds..."
    sleep 5
done
