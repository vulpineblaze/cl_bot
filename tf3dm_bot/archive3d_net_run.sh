#!/bin/sh

python archive3d_net_bot.py $1 2>&1 | tee archive3d_net_bot_output.log

# in case of too many
# killall -9 phantomjs