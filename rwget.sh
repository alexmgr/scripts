#!/usr/bin/env zsh

wget -mk -w 1 -r -H --referer="http://www.google.com" --user-agent="Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6" -D "$1" "$1"
