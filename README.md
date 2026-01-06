# 🖥️ System Monitor

## Overview
Python-based system monitor tracking system statistics. Logs statistics to "system_monitor.log" and sends update emails to select email addresses.

## Quickstart
### Windows
```bash
git clone https://github.com/SpectreStorms/system_monitor
cd system_monitor
copy example-config.py config.py
notepad config.py
pip install -r requirements.txt
python monitor.py
```

## Features
* Logging
    * Logs statistics into "system_monitor.log" in the same system directory
* Emailing
    * Sends emails to multiple recipients.
* CPU
    * Overall CPU usage
    * Per-thread usage
* Memory
    * Overall RAM usage
* Storage
    * Used storage per disk
    * Total storage per disk
    * Per-disk usage
