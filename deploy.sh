#!/bin/bash

set -u

zip ebskeeper.zip lambda_function.py
aws s3 cp ebskeeper.zip s3://ebskeeper/ebskeeper.zip
rm -f ebskeeper.zip
