#!/bin/bash
read -p "Enter channel url: " url 
curl -s $url | sed -n 's/.*title="RSS"\s\+href="\([^"]\+\).*/\1/p'
