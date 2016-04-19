# MBMBaM_Uploader
A Python application which automatically uploads the new episode of MBMBaM to your Dropbox.

This is my biggest program thus far. It uses urllib.requests and beautifulsoup to collect the latest episode of the podcast My Brother My Brother and Me, downloads it to my machine temporarily, and then uses the Dropbox API to upload to my Dropbox. After this is completed it uses the Pushbullet API to send me a note saying that there is a new episode available.

I am not too experienced when it comes to programming so I am quite proud of this. That being said, I am sure there are parts of my code that are messy/not pythonic so if anyone comes across this and would like to critique my code feel free.

And of course if anyone would like to use this code for its intended purpose don't hesitate!

You will obviously need your own access tokens from Dropbox and Pushbullet in order to use their APIs.

The cronjob was a nightmare for me so just in case anyone else has trouble I'll document how I got that to work.

To edit the cron file:

`crontab -e`

To run every hour, the cron command is:

`0 * * * * <command>`

Since this program needs to open/edit text files it needs to be executed in the directory where the program resides. On my Pi, it wanted to execute from the `/etc` folder. To resolve this:

`0 * * * * cd path/to/dir && ./script.py`
