#!/bin/bash

openssl pkcs12 -passin pass:notasecret -in privatekey.p12 -nocerts -passout pass:notasecret -out key.pem

# this next line is kind of odd -- but the key is exported with some metadata at the beginning that PyCrypto can't digest.
tail -n +5 key.pem > privatekey.pem
rm key.pem
