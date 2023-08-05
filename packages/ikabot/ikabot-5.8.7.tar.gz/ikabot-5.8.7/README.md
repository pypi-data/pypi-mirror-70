## ikabot ~ Ikariam Bot  
[![Downloads](https://pepy.tech/badge/ikabot)](https://pepy.tech/project/ikabot)

_Ikabot is a program written in python that grants iqual and even more functionality than a premium account in ikariam, without spending ambrosia!_

### Features

0. Exit

	Closes the main menu, returning to the normal console. You can also use `ctrl-c`. When closing _ikabot_, all the actions that you configured will continue running in the background. You can list them with `ps aux | grep ikabot`.

1. Construction list

	The user selects a building, the number of levels to upload, _ikabot_ calculates if it has enough resources and uploads the selected number of levels. If you don't have enough resources, it can send them automatically from the cities that you specify.
	
2. Send resources
 
	It sends unlimited amount of resources from one city to another. It doesn't matter how many boats you have, _ikabot_ will send all the trips that were necessary. The destination city can be own by the user or by other.

3. Distribute resources

	It sends whatever resource you choose from the cities that produce it to cities that do not. The same amount is sent to all cities, unless a city has little free storage space. (Very useful to send wine)

4. Distribute resources evenly

	This function attempts to distribute all of a given type of resource evenly among all cities, regardless of if they're production cities or non-production cities.
	
5. Account status

	It shows information such as levels of the buildings, time until the wine runs out, resources among other things from all the cities.
	
6. Donate

	It allows you to donate (WOW!).
	
7. Search for new spaces

	This functionality alerts by telegram, if a city disappears or if someone founds in any of the islands where the user has at least one city.
	
8. Login daily

	For those who do not want to spend a day without their account login.
	
9. Alert attacks

	It alerts by telegram if you are going to be attacked. You can configure how often _ikabot_ checks for incoming attacks.

10. Donate automatically

	_Ikabot_ enters once a day and donates all the available wood from all cities to the luxury good or the forest.

11. Alert wine running out

	It warns you by Telegram when less than N hours are needed for a city to run out of wine. The number of hours is specified by the user.

12. Buy resources

	It allows you to choose what type of resource to buy and how much. It automatically purchases the different offers from the cheapest to the most expensive.
	
13. Sell resources

	It allows you to choose what type of resource to sell and how much. It does not matter how much storage you have, it automatically updates the offers as pĺayers buy from you. When it sells all the resources, it let's you know via Telegram.

14. Activate Vacation Mode

	Sets the account in vacation mode and closes _ikabot_.

15. Activate miracle

	It allows you to activate any miracle you have available N times in a row.

16. Train troops

	It allows you to easily create large amounts of troops in one city. If there are not enough resources to train all of them, it will train all the troops it can and when it finishes it will try to train the rest. It also allows you to build your army in multiple small steps so that you can use it as fast as possible.
	
17. Train fleet

	The same as before but with boats.

18. See movements

	Let's you see movements coming to/from your cities. This includes attacks, transports, etc.

19. Construct building

	It allows you to contruct a building (WOW!, again).

20. Update Ikabot

	It tells you how to update _ikabot_

21. Update the Telegram data

	It allows you to set or update your Telegram contact information.

When you set an action in _ikabot_, you can enter and play ikariam without any problems. The only drawback that you may have is that the session expires, this is normal and if it happens just re-enter.

### Discord
Join us in discord at:`https://discord.gg/3hyxPRj`

### Install

```
python3 -m pip install --user ikabot
```
with the `ikabot` command you access the main menu.

### Build from sources
```
git clone https://github.com/physics-sp/ikabot
cd ikabot
python3 setup.py sdist bdist_wheel
python3 -m pip install dist/*.whl
rm -rf build dist ikabot.egg-info
```

### Uninstall

```
python3 -m pip uninstall ikabot
```
### Requirements

In order to install and use _ikabot_, python3 and pip must be installed. It must be run on **Linux**, it does not work on **Windows**.

#### - Python 3
It is probably installed by default in your system.

To check if it is installed by default, just run `python3 --version`.

If it is not installed, visit the [official website](https://www.python.org/) 

#### - Pip
It is a tool to install python packages.

To check if it is installed by default, just run `python3 -m pip -V`.

To install it, you must download the _get-pip.py_ file from [this page](https://pip.pypa.io/en/stable/installing/) and run `python3 get-pip.py`.

Or just excecute:
```
curl https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
rm get-pip.py
```

### Telegram

Some features (such as alerting attacks) are communicated to you via Telegram messages.

This messages are only visible for you.

Setting this up is highly recommended, since it allows you to enjoy all the functionality of _ikabot_.

To configure this, you just need to enter two pieces of information:

1) The token of the bot you are going to use

	If you want to use the 'official' bot of _ikabot_, enter Telegram and search with the magnifying glass @DaHackerBot, talk to it and you will see that a /start is sent. Once this is done you can close Telegram.
	
	Then, when _ikabot_ asks you to enter the bot's token, use the following: `409993506: AAFwjxfazzx6ZqYusbmDJiARBTl_Zyb_Ue4`.
	
	If you want to use your own bot, you can create it with the following instructions: https://core.telegram.org/bots.

2) Your chat_id

	This identifier is unique to each Telegram user and you can get it by talking by telegram to @get_id_bot (the one with the bow in the photo).

When you want to use a functionality that requires Telegram, such as _Alert attacks_, _ikabot_ will ask you for the bot's token and your chat_id. Once entered, they will be saved in a file and will not be asked again.

**If you are concerned about privacy, set up your own bot, so that nobody has the bot's token**

### Advanced

If there is an ikabot process that we identified with `ps aux | grep ikabot`, we can get a description of what it does with `kill -SIGUSR1 <pid>`. The description will arrive via Telegram.

### Windows

_Ikabot_ does not work in Windows, although in the future it might work in the Ubuntu bash of Windows 10.
