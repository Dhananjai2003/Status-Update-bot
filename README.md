# Status-Update-bot

## Description
Discord bot to check for status updates for CTF teams


### Libraries Used:
+ datetime
+ prettytable (To create tables)
+ sqlite3
+ discord.py 

## Content
+ Package installation
+ How to Use
+ Credits

## Guide to Install and Run
+ install datetime `pip install datetime`
+ install prettytable `pip install prettytable`
+ install discord.py `pip install discord.py`

## How to use the BOT in your server

### Set -up
+ Install the nessary packages
+ Make a discord app in discord developer portal (https://discord.com/developers/applications)
+ Then make a bot and generate a bot and a token.
+ Clone this directory and in `bot.py` in the last line insert you token in side `client.run('insert your token')`
+ Invite the bot to your server with the nessary permissons
+ Then run the script in you server 

### Bot commands
+ `!add me <category>` Adds the user who used this command
+ `!add <ID> <category>` Adds the person mentioned
+ `!remove <ID>` Removes person mentioned 
+ `!startStatusUpdate` Starts Status update
+ `!stop` Stops status update
+ `!showStatus` Shows status of all the members
+ `!showPending <number>` Shows list of members with number of pending updates greater that specified number
+ `!update ```<update content>``` ` Registers Updates by user.
+ `!help` Shows the list of commands

## Credits 
+ Dhananjai Murali - python,sqlite3 implimentation.
