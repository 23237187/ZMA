#!/usr/bin/env bash
query_url=http://0.0.0.0:8000/queries.json

echo {"user": $1, "num": $2} | http POST $query_url