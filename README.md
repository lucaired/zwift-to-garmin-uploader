# Zwift to Garmin

This project is aimed at uploading my activities from Zwift to Garmin. 
The goal is to do this without giving Zwift full access to my Garmin data.

### Prerequisites
- Garmin Connect account
- Zwift account
- Working Zwift setup on MacOS

### Setup
1. Add you Garmin credentials to the MacOS keychain as `Garmin`, if not already done:
    ```bash
    security add-internet-password -a <e-mail> -s connect.garmin.com -w <password> -l Garmin
    ```
2. Add and populate the `.env` file:
    ```bash
    cp .env.example .env
    ```
3. Install the dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

### Usage
1. Start the script via python:
    ```bash
    python3 main.py
    ```
2. Supply credentials to access the keychain when prompted
3. Start Zwift and record an activity

The script will automatically upload the activity to Garmin Connect by detecting new activities in the Zwift folder. 