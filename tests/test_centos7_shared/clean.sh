#!/bin/bash
./destroy.sh && rm -r files/ssh-keys roles terraform_tmp verify.d/__pycache__ && unlink venv
