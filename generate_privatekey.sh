#!/bin/bash

openssl pkcs12 -passin pass:notasecret -in privatekey.p12 -nocerts -passout pass:notasecret -out key.pem
openssl pkcs8 -nocrypt -in key.pem -passin pass:notasecret -topk8 -out privatekey.pem
rm key.pem
