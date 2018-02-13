#!/bin/bash
set -evx

mkdir ~/.endorphincore

# safety check
if [ ! -f ~/.endorphincore/.endorphin.conf ]; then
  cp share/endorphin.conf.example ~/.endorphincore/endorphin.conf
fi
