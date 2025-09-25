#!/bin/bash

DATA_FILE="breeds.json"

if [ ! -f "$DATA_FILE" ]; then
	echo "Error: Data file '$DATA_FILE' not found. Please run fetch data.sh first." >&2
	exit 1
fi

NUM_BREEDS=$(jq '.message | keys | length' "$DATA_FILE")

echo "Total number of unique dog breeds: $NUM_BREEDS"


