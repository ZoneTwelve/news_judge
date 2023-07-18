#!/bin/bash
read -r -p "Enter your message: " user_input

# Remove newline characters from user input
user_input=$(echo "$user_input" | tr -d '\n')

# Encode the user input into JSON without character escaping
encoded_json=$(jq -n --arg msg "$user_input" '{"message": $msg}')

echo "Encoded JSON: $encoded_json"

