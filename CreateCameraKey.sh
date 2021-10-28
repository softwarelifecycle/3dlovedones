#!/bin/bash

rm -f ~/.ssh/id_rsa
rm -f ~/.ssh/id_rsa.pub

echo "Creating key!"
echo -e "\n" | ssh-keygen -t rsa -N ""

echo "Copying to server!"
echo -e "!Alexandria1\n" | ssh-copy-id hchattaway@192.168.0.123
