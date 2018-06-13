#!/usr/bin/env bash
sudo sh -c "crontab -l > tmp"
sudo sh -c "cat crontab.sh >> tmp"
sudo crontab < tmp
sudo rm tmp