# TWITTER / X AUTODEACTIVATE

Python script to automatically deactivate your Twitter/X account and prevent it from being permanently deleted.

## ⚠️ Disclaimer
This project is provided for educational and personal-use purposes only.
Use it responsibly. Automating actions on X may violate their Terms of Service.

## Installation

Clone the repository and install all required dependencies:

```
pip install -r requirements.txt
```

## Configuration

Edit the file data.json and set your account credentials:
```json
{
  "USERNAME": "your_username_or_email",
  "PASSWORD": "your_password",
  "DEACTIVATE": false
}
```

If your account is already deactivated, set "DEACTIVATE": true.

## Usage

Run the script:

```
pyhon autodeactivate.py
```

The script will:

    1. Launch Chrome in incognito mode with remote debugging enabled.
    2. Log in automatically using pyautogui.
    3. Connect Selenium to the same browser session.
    4. Deactivate your account safely.
    5. A file called `status.log` will be created showing the result and the reactivation deadline.
