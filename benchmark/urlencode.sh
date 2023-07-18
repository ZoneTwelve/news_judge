#!/bin/bash

urlencode() {
  local string="$1"
  local length="${#string}"
  local encoded=""
  local pos c o

  for ((pos = 0; pos < length; pos++)); do
    c="${string:$pos:1}"
    case "$c" in
      [-_.~a-zA-Z0-9])
        o="${c}"
        ;;
      *)
        printf -v o '%%%02x' "'$c"
        ;;
    esac
    encoded+="${o}"
  done

  echo "$encoded"
}

