#!/bin/bash
# Richie Foreman <richie.foreman@gmail.com>
# This script is used to help generate proper certs for use with test_pycrypto_jwt.py


openssl req -new -newkey rsa:2048 -days 3650 -nodes -x509 \
  -keyout privatekey.pem -out publickey.pem \
  -subj "/CN=unit-tests"

openssl rsa -in privatekey.pem -inform PEM -out publickey_der -outform DER

openssl pkcs12 -export -out privatekey.p12 \
  -inkey privatekey.pem -in publickey.pem \
  -name "key" -passout pass:notasecret
