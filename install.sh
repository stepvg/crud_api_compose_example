#!/bin/bash

docker-compose up -d --build
sudo cp -r memory_notifier/memory_notifier.service /etc/systemd/system/memory_notifier.service
sudo cp -r memory_notifier/memory_notifier.py /usr/local/bin/memory_notifier.py
sudo systemctl enable memory_notifier.service
sudo systemctl start memory_notifier.service

