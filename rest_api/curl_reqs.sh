#!/bin/sh

curl -i -X GET http://127.0.0.1:5000/items
curl -i -X GET http://127.0.0.1:5000/items/1
curl -i -X POST -H 'Content-Type: application/json' -d'{"name" : "Grapes"}' http://127.0.0.1:5000/items
curl -i -X GET http://127.0.0.1:5000/items
