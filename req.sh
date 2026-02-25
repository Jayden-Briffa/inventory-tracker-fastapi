#!/bin/bash
url=http://127.0.0.1:8000/api/

if [[ "${1^^}" == "GET" ]]; then
    if [[ -n "$2" ]]; then
        curl -X GET ${url}items/$2/ \
        -H "Content-Type: application/json"
    else
        curl -X GET ${url}items/ \
        -H "Content-Type: application/json"
    fi
fi

if [[ "${1^^}" == "POST" ]]; then
    curl -X POST ${url}items/ \
    -H "Content-Type: application/json" \
    -d '{
        "qrCode": "12345qr12345",
        "name": "Sample Item",
        "description": "A sample item",
        "isCollection": false
    }'
fi

if [[ "${1^^}" == "PUT" ]]; then
    curl -X PUT ${url}items/$2/ \
    -H "Content-Type: application/json" \
    -d '{
        "qrCode": "12345qr12345",
        "name": "New Item",
        "description": "A newer item",
        "isCollection": false
    }'
fi

if [[ "${1^^}" == "DELETE" ]]; then
    curl -X DELETE ${url}items/$2/ \
    -H "Content-Type: application/json"
fi