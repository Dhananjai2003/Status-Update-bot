import discord
import datetime
from prettytable import PrettyTable
from sqlScript import *

intents = discord.Intents().all()
intents.messages=True
client = discord.Client(intents = intents)

category_list=get_categories()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global category_list
    if message.author == client.user:
        return

    if message.content.startswith('!newCategory'): #to add new categories
        message_list=message.content.split(' ')
        if len(message_list)==2:
            if add_categories(message_list[-1]):
                category_list = get_categories()
                await message.channel.send(f'{message_list[-1]} is added')
            else:
                await message.channel.send(f'{message_list[-1]} is already exists')
        
        else:
            message.channel.send('```Wrong Format \nFormat = !newCategory <category_name>```')
    
    if message.content.startswith('!hello'): # says hello back
        await message.channel.send(f'Hello {message.author}')

    if message.content.startswith('!add'): #tested
        message_list=message.content.split(' ')
        if len(message_list)==3 and message_list[-2]=='me' and message_list[-1] in category_list:
            if add_members(message.author,message_list[-1]):
                await message.channel.send(f'{message.author} Already Exist in this list')
            else:
                await message.channel.send(f'Welcome {message.author} from {message_list[-1]}')

        elif len(message_list) >= 3 and message_list[-1] in category_list :
            name_new_user=''
            for i in range(1,len(message_list)-1):
                name_new_user+=message_list[i]+' '
            
            add_members(name_new_user,message_list[-1])
            await message.channel.send(f'Welcome {name_new_user} from {message_list[-1]}')
        else:
            await message.channel.send(f"```Wrong Format = !add me <category>\ncategory in {category_list}```")
        # add the backend


    if message.content.startswith("!startStatusUpdate"): #tested
        x = datetime.datetime.now()
        #here a new tuple should be created
        if check_round_active() == False:#only if no rounds are running
            start_round(message.author)
            await message.channel.send(f'{message.author} has started status updates for {x.strftime("%x")}')
        else:
            await message.channel.send('!! A ROUND IS ALREADY ACTIVE !!')

    if message.content.startswith("!stop"):
        if check_round_active() == False:#checks for the previous round
            await message.channel.send(" No Status update round is active")
        elif check_round_author(message.author):#here there should be a validation (user started the status update == user terminating status update)
            stop_round()
            await message.channel.send(f'{message.author} has terminated status update')
        else:
            await message.channel.send("!! ONLY THOSE WHO STARTED THIS ROUND CAN TERMINATE THIS ROUND !!")
    

    if message.content.startswith("!showStatus"): #tested

        myTable = PrettyTable(["Name","Status"])
        return_message=show_status()
        for i in range(len(return_message)):
            myTable.add_row([return_message[i][0],return_message[i][1]])
        
        await message.channel.send("```"+str(myTable)+'```')


    if message.content.startswith("!showPending"): # tested
        message_list=message.content.split(" ")
        
        if len(message_list)!=2:
            await message.channel.send("```Worng Fromat \nFormat = !showPending <minimum days pending>```")

        else:

            name_list=show_pending(message_list[-1])
            myTable = PrettyTable(["Name","Category","Status"])

            for i in name_list:
                myTable.add_row([i[0],i[1],i[-1]])

            await message.channel.send("```"+str(myTable)+"```")


    if message.content.startswith('!remove'): #tested
        message_list=message.content.split(' ')

        if len(message_list)<3:
            await message.channel.send(f"```Worng Format = !remove <discordName#id> <category> \ncategory in {category_list}```")

        elif message_list[-1] not in category_list:
            await message.channel.send(f"```Worng Format = !remove <discordName#id> <category> \ncategory in {category_list}```")
            

        else:
            name_user=message_list[-2]
            user_cat=message_list[-1]
            remove_members(name_user,user_cat)
            await message.channel.send(f'removed {name_user} from status updates')

    if message.content.startswith('!update'):
        message_list=message.content.split('```')
        if check_round_active():
            if len(message_list)!=3:
                await message.channel.send(f'Wrong Format')

            else:
                update(message.author)
                await message.channel.send(f'{message.author} has commpleted status update!')
        else:
            await message.channel.send(f"There is now round active now you can't post updates")

   

    if message.content.startswith('!help'):
        await message.channel.send(f""" ```!update <post update in code blocks> | To post updates
!startStatusUpdate | Will start a new round for status update
!stop | To stop current round
!showStatus | To show pending/non-pending status updates for a round
!showPending <minimum days pending> | To show members with certain amount of days pending
!add me <category> | To add yourself to the Status update list category in {category_list}
!add <discord id> <category> | To add someone to the Status update list 
!remove <discord id> | To remove members for status update list
!newCategory <category name> | To add new categories into the bot
!hello | Will say back hello```""")



        


client.run("insert token here")
