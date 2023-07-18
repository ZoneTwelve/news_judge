$!/bin/zsh

ROOT=prompts

get_prompt() {
    file=$1
    # read file from $ROOT/$file
    prompt=$(cat "$ROOT/$file")
    # return prompt
    echo "$prompt"
}
