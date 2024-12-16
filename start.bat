@echo off
start python server.py
timeout /t 5
cd path_to_ngrok_folder
ngrok http 5000
