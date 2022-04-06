#!/bin/sh
eval $( fixuid )
echo '123456'|sudo -S rm -f /var/run/fixuid.ran
/bin/bash
