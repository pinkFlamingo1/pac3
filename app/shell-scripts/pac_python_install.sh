#!/usr/bin/env bash

if [[ $CS_GITROOT = *pac3* ]]
then
    cd $CS_GITROOT
    echo "Remove .venv"
    rm -Rf .venv
    echo "Create .venv"
    python3 -m venv .venv
    source .venv/bin/activate
    cd app/requirements
    echo "Install requirements"
    pip install --upgrade pip
    pip install wheel
    pip install -r requirements.txt
else
    echo "Warning: incorrect $CS_GITROOT"
fi
echo "Upgrade done"
