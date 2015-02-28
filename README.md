# SimpliSafeAutomation
This script allows you to schedule your Home Alarm System "SimpliSafe" to automatically Arm/Disarm on a predefine schedule.

You can use a Raspberry PI to run this script and automate the process.

## Using Terminal to control the alarm system (Mac users).

```
###### Turn alarm ON/OFF using default settings.
python alarmsystem.py

###### Turn alarm ON in home mode
python alarmsystem.py home

###### Turn alarm ON in away mode
python alarmsystem.py away

###### Turn alarm OFF
python alarmsystem.py off
```

## Raspberry PI Setup

You need to create a <b>cron job</b> that will run the alarmsystem.py script on a predefined schedule.  You also have to make sure the <b>cron job</b> starts automatically when the raspberry pi bootup.

Clone this repository into a folder called alarm
```
pi@raspberry ~ $ git clone https://github.com/eddieespinal/SimpliSafeAutomation.git alarm
```

#### Create the cron job
Assuming you are already logged in as 'pi' user on your raspberry pi.

Switch to root user using sudo bash
```
pi@raspberry ~ $ sudo bash 
```

Now run the command crontab -e, this will launch the <b>nano editor</b> with an empty document.
```
root@raspberrypi:/home/pi# crontab -e
```

Copy and paste the following entry. This cron job will run the script at 11:00PM to activate it and at 6:00AM to deactivate it. You can change this schedule to fit your needs. You can find some good cron job tips here. [15 Awesome Cron Job Examples](http://www.thegeekstuff.com/2009/06/15-practical-crontab-examples)
```
00 23 * * * /usr/bin/python /home/pi/alarm/alarmsystem.py home >/home/pi/alarm/script.log 2>&1
00 06 * * * /usr/bin/python /home/pi/alarm/alarmsystem.py off >/home/pi/alarm/script.log 2>&1
```
Hold control + X to exit the nano editor. You will be prompted to save the changes, press Y to save it. and then return key to close.

Now run this command to verify your changes were saved sucessfully.  You should see the cron job you just created.
```
root@raspberrypi:/home/pi# crontab -l
```

Start cron service by running /etc/init.d/cron start
```
root@raspberrypi:/home/pi# /etc/init.d/cron start
```

Last step is to run the cron job at startup. Edit the <b>/etc/rc.local</b> file and add the following line <b>/etc/init.d/cron/start</b> be sure to add it before the `exit 0`.

```
root@raspberrypi:/home/pi# nano /etc/rc.local
```

Copy and Paste the following command at the bottom of this file, right before exit 0.
```
/etc/init.d/cron start
```
Hold control + X to exit, you will be prompted to save the changes, press Y to save it. and then return key to close.

You should restart your raspberry pi
```
root@raspberrypi:/home/pi# sudo reboot
```

Done!
