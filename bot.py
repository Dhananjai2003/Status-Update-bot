import discord
import datetime
import os
from prettytable import PrettyTable
from sqlScript import add_members,remove_members,check_round_active,check_round_author, show_pending, start_round, stop_round, show_status,update

intents = discord.Intents().all()
intents.messages=True
client = discord.Client(intents = intents)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!hello'): 
        await message.channel.send(f'Hello {message.author}')

    if message.content.startswith('!add'): #tested
        message_list=message.content.split(' ')
        if len(message_list)==3 and message_list[-2]=='me' and message_list[-1] in ['crypto','reversing','forencis','pwn','web','pentest']:
            if add_members(message.author,message_list[-1]):
                await message.channel.send(f'{message.author} Already Exist in this list')
            else:
                await message.channel.send(f'Welcome {message.author} from {message_list[-1]}')

        elif len(message_list) >= 3 and message_list[-1] in ['crypto','reversing','forencis','pwn','web','pentest'] :
            name_new_user=''
            for i in range(1,len(message_list)-1):
                name_new_user+=message_list[i]+' '
            
            add_members(name_new_user,message_list[-1])
            await message.channel.send(f'Welcome {name_new_user} from {message_list[-1]}')
        else:
            await message.channel.send("```Wrong Format = !add me <cat>\ncat = 'crypto','reversing','forencis','pwn','web','pentest' ```")
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
            myTable = PrettyTable(["Name","Cat","Status"])

            for i in name_list:
                myTable.add_row([i[0],i[1],i[-1]])

            await message.channel.send("```"+str(myTable)+"```")


    if message.content.startswith('!remove'): #tested
        message_list=message.content.split(' ')

        if len(message_list)<3:
            await message.channel.send("```Worng Format = !remove <discordName#id> <cat> \ncat = 'crypto','reversing','forencis','pwn','web','pentest'```")

        elif message_list[-1] not in ['crypto','reversing','forencis','pwn','web','pentest']:
            await message.channel.send("```Worng Format = !remove <discordName#id> <cat> \ncat = 'crypto','reversing','forencis','pwn','web','pentest'```")
            

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
        await message.channel.send(""" ```!update <post update in code blocks> | To post updates
!startStatusUpdate | Will start a new round for status update
!stop | To stop current round
!add me <div> | To add yourself to the Status update list cat = ('crypto','reversing','forencis','pwn','web','pentest')
!add <discord id> <div> | To add someone to the Status update list 
!remove <discord id> | To remove members for status update list
!hello | Will say back hello```""")



        


client.run("retrived")
