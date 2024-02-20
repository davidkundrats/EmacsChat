#!/bin/zsh

# Default IP address of the Flask app
IP_ADDRESS="localhost:5000"

if [ ! -z "$1" ]
  then
    IP_ADDRESS=$1
fi

# interactive session 
echo "Enter your messages below (type 'exit' to quit):"
while true; do
    read -p "> " MESSAGE
    
    if [[ "$MESSAGE" == "exit" ]]; then
        echo "Exiting chat..."
        break
    fi

    RESPONSE=$(curl -s -X POST http://$IP_ADDRESS/chat \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"$MESSAGE\"}")
    
    echo "Bot: $RESPONSE"
done
