#!/bin/bash
source ../.env

submit() {
    sys_input=$1
    usr_input=$2
    json='{
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": $sysin},
            {"role": "user",   "content": $usrin}
        ],
        "temperature": 0.0
    }'
    data=$(jq -n --arg sysin "$sys_input" --arg usrin "$usr_input" "$json")
    output=$(curl -s https://api.openai.com/v1/chat/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $OPENAI_API_KEY" \
      -d "$data" | jq -r '.choices[0].message.content')
    echo "$output"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    sys_input="You're a helpful machine, your name is 'Wilson'."
    usr_input="Who are you? What's your name?"
    if [ ! -z "$1" ]; then
        sys_input="$1"
    fi
    if [ ! -z "$2" ]; then
        usr_input="$2"
    fi
    out=$(submit "$sys_input" "$usr_input")
    echo "$out"
fi

