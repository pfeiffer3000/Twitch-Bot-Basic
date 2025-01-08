# This is the main bot guts.
# It handles signing in to twitch, getting ready, sending messages, and redirecting commands to the cogs.
# cog_commands.py ==> handles general chatbot commands, like !help, !shoutout, etc.
# cog_pubsub.py ==> deals with subscriptions, channel points, and stuff like that

from twitchio.ext import commands, routines, eventsub
from random import choices
import asyncio

# you need the following Twitch API Scopes (https://dev.twitch.tv/docs/authentication/scopes/)
# bits:read
# channel:read:redemptions
# channel:manage:redemptions
ACCESS_TOKEN = "" 

prefix_char = "!"  # the prefix for commands

botnick = "Your Bot Name Here"
initial_channels = ['<your_channel_name>']


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=ACCESS_TOKEN, prefix=prefix_char, initial_channels=initial_channels)
        self.esclient = eventsub.EventSubWSClient(self)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is   | {self.user_id}')
        self.RT_info_reminder.start()
        print(f"Ready!")
        print()

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot.
        if message.echo:
            print(f"    {botnick}: {message.content}")
            return

        # Print the contents of our message to console...
        print(f"{message.author.name}: {message.content}")

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands.
        await self.handle_commands(message)

    async def send_multiple(self, temp_list, sleep_time=2):  # code to send multiple messages from a list
        channel = self.bot.get_channel(self.channel)
        for t in temp_list:
            await channel.send(t)
            await asyncio.sleep(sleep_time)
    
    async def send_message(self, MESSAGE):  # code to send multiple messages from a list
        channel = self.bot.get_channel(self.channel)
        await channel.send(MESSAGE)

    # This error replaces the one in ext.commands.bot.event_command_errors()
    # Comment it out for the real error to show up
    async def event_command_error(self, context: commands.Context, error: Exception):
        pass

    # ========== put COMMANDS here ========================================

    

    # ========== routines are below ========================================

    @routines.routine(minutes=14)
    async def junk_reminder(self):  # sends random 1s and 0s to the first channel in the list
        zero_ones = ["0", "1"]
        random_junk = ''.join(choices(zero_ones, k=3))
        channel = self.get_channel(initial_channels[0])
        await channel.send(f"Try {prefix_char}info. #.{random_junk}") # The random junk helps Twitch not think it's a duplicate message

    @RT_info_reminder.before_routine
    async def junk_reminder_before(self): # sends a welcome message before launching into the junk_reminder routine above
        channel = self.get_channel(initial_channels[0])
        await channel.send(f"Remember, there will be junk!")


    # ============================

    
bot = Bot()
initial_extensions = ["cog_commands", "cog_pubsub"] # the cogs handle stuff like commands, bits, subscriptions, etc. 
for extension in initial_extensions:
    bot.load_module(extension)

bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.