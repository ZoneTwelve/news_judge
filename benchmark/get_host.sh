#!/bin/zsh
get_host() {
    url=$1
    host=${url#*://}
    host=${host%%/*}
    echo "$host"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo $(get_host "$1")
fi
