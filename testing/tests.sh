#!/bin/bash

py.test
docker rm -f $(docker ps -a | tail --lines=+2 | cut -c -8)
