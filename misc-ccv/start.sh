#!/bin/bash

while [ true ]; do
	su -l $USER -c "socat -dd TCP4-LISTEN:9000,fork,reuseaddr,nodelay,pktinfo EXEC:'/usr/src/app/server.py',pty,echo=0,rawer,iexten=0"
done;