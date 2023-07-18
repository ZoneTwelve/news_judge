#!/bin/zsh
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
    output=$(curl https://api.openai.com/v1/chat/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $OPENAI_API_KEY" \
      -d "$data" | jq -r '.choices[0].message.content')
    echo "$output"
}

out=$(submit "You're a helpful machine, your name is 'Wilson'" "Who are you? What's your name?")
echo "Output: $out"
