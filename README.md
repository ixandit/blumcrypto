# Automation experiment for blum.io Telegram Mini App
This repository contains a Python script designed to interact with the BLUM telegram bot [https://t.me/BlumCryptoBot](t.me/BlumCryptoBot/app?startapp=ref_f5KQfgPIdz).

## Disclaimer
Please Note: The code and information provided in this repository are intended solely for educational and research purposes, with a specific focus on Telegram Mini Apps (TMAs). The author does not condone or encourage any illegal or unethical activities. It is essential to adhere to ethical guidelines and obtain proper authorization before engaging in any security testing attempts. The author is not responsible for any misuse or damage caused by this script.

## Features

- **Claim Tasks:** Automatically claim tasks available on the platform.
- **Check Balance:** Check the current balance of your account.
- **Start Farming:** Start the farming process on the platform.
- **Play Games:** Automate playing games to earn points.

## Prerequisites

Before you can use this script, make sure you have the following installed:

- Python 3.6 or higher
- `requests` library

You can install the required library using pip:

```bash
pip3 install requests
```
## Usage
To use this script, you will need your authorization token from the BLUM platform. This token will be used to authenticate your requests.
<br>**Note**: The procedure for obtaining the authorization token has been intentionally omitted.

Command-Line Arguments
token: (Required) Authorization token for the BLUM platform.
- `--check-balance`: Check the current balance of your account.
- `--claim-tasks`: Claim available tasks on the platform.
- `--start-farming`: Start the farming process.
- `--play-games`: Specify the number of games to play for earning points.

## Examples
### Check Balance
To check the balance of your account, run:

```
python3 blum.py your_authorization_token --check-balance
```
### Claim Tasks
To claim available tasks, run:

```
python3 blum.py your_authorization_token --claim-tasks
```

### Start Farming
To start farming, run:

```
python3 blum.py your_authorization_token --start-farming
```
### Play Games
To play a specified number of games, run:

```
python3 blum.py your_authorization_token --play-games number_of_games
```
