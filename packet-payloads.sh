#!/usr/bin/env bash

[[ "${#}" -eq 0 || "${#}" -gt 2 ]] && { echo "Usage: ${0} pcap [filter]" 1>&2; exit 1; }
[[ ! -d "${1}" ]] && { echo "Pcap folder not found: ${1}" 1>&2; exit 1; }

function strip_extension {
  [[ ! -n "${1}" ]] && return 1
  # Grab filename wihtout the extension
  if [[ "${1}" == *"."* ]]; then
    filename=$(echo "${1}"|sed -r 's/(.*)\.(.+)$/\1/')
  else
    filename="${1}"
  fi
  echo "${filename}"
}

for pcap in $(find "${1}" -type f); do
  filename=$(strip_extension "${pcap}")
  # Bash can't handle null bytes, so need to hexlify the data
  payload=$(./packet-payload.sh "${pcap}" "${2}" | xxd -p | tr -d '\n')
  [[ -z "${payload}" ]] && echo "Failed to extract payload from ${pcap}" 1>&2 || echo -ne "${payload}" | xxd -p -r > "${filename}.bin"
done
