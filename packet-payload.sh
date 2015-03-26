#!/usr/bin/env bash

command -v tshark >/dev/null 2>&1 || { echo "tshark not found, but required to extract packet payloads. Exiting." 1>&2; exit 1; }

[[ "${#}" -eq 0 || "${#}" -gt 2 ]] && { echo "Usage: ${0} pcap [filter]" 1>&2; exit 1; }

[[ ! -f "${1}" ]] && { echo "Pcap file not found: ${1}" 1>&2; exit 1; }

pcap="${1}"

# Set a filter if supplied by the user
if [[ -z "${2}" ]]; then
  filter=""
else
  filter="${2} and data"
fi

payload=$(tshark -r "${pcap}" -Y "${filter}" -T fields -e data)
rc=$?
# Exit and report if tshark fails
[[ $rc -ne 0 ]] && exit $rc

echo "${payload}" | tr -d "\n" | xxd -p -r
