# Bot for extract Leads with Home Advisor account

This Python script allows you to automatically extract Leads to a Home Advisor account.

## Requirements
* Windows
* [GIT for Windows](https://github.com/git-for-windows/git/releases/latest) - Make sure to select: Add to system `$PATH` at the end of the installation.
* [Python 3.7.0](https://www.python.org/downloads/release/python-374/) - Make sure to select: Add to system `$PATH`.

## Installing the script
1. Option from git clone: Run the following command on CMD-DOS:
```shell
git clone https://github.com/Raukdv/HA-GENERAL.git
```
2. Option from github: Download the full folder in repo and unzip:
```
cd foldername
```
3. Run the next command in root level
```
python setup.py install
```

## Running the script

Make sure that you are inside the folder that contains the propper files.

```shell
bot porch

```


## Dotenv example
you will need to create a `.env` under the folder that you will run the bot.

## Main Values
RETRIES = 100
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
USE_CSV = "true"
```
HA_USERNAME=""
HA_PASSWORD=""
HA_AIRTABLE="https://api.airtable.com/v0/API-ID/TABLE-NAME"
HA_AIRTABLE_KEY="API-KEY"
```
## Additional values
```
STATUS_PROCESSING=1
STATUS_APPROVED=2
STATUS_DENY=3
```