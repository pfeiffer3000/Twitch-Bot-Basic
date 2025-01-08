from twitchio.ext import pubsub, commands
from random import choice
import asyncio

USERS_OAUTH_TOKEN = ""
USERS_CHANNEL_ID = ""

prefix_char = "!"

class PubSubCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.pubsub = pubsub.PubSubPool(bot)
        
        self.channel = "YOUR CHANNEL NAME"
        
    @commands.Cog.event()
    async def event_ready(self):
        topics = [
            pubsub.channel_points(USERS_OAUTH_TOKEN)[USERS_CHANNEL_ID],
            pubsub.bits(USERS_OAUTH_TOKEN)[USERS_CHANNEL_ID],]
        await self.bot.pubsub.subscribe_topics(topics)

    async def send_multiple(self, temp_list, sleep_time=2):  # code to send multiple messages from a list
        channel = self.bot.get_channel(self.channel)
        for t in temp_list:
            await channel.send(t)
            await asyncio.sleep(sleep_time)
    
    async def send_message(self, MESSAGE):  # code to send a single messsage
        channel = self.bot.get_channel(self.channel)
        await channel.send(MESSAGE)
    

    # ==== CHANNEL POINTS =============
    @commands.Cog.event()
    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        await self.event_pubsub_channel_points2(event)

    async def event_pubsub_channel_points2(self, event: pubsub.PubSubChannelPointsMessage):
        # You could do this direct in the event if you wanted to
        MESSAGE = f"{event.user.name} used '{event.reward.title}' for {str(event.reward.cost)} Channel Points."
        print(MESSAGE)

        # =========== put channel points reward logic below here ==================
        if event.reward.title == "Get a new DJ name":
            dj1 = ["DJ", "Captain", "Flippin"]
            dj2 = ["Twinkie", "Dingus", "MadDog"]
            
            dj_name_1 = choice(dj1)
            dj_name_2 = choice(dj2)
            dj_name = f"{dj_name_1} {dj_name_2}"
            MESSAGE = f"{event.user.name} new DJ Name is: {dj_name}"
        
            await self.send_message(MESSAGE)
   


    # === BITS ====================

    @commands.Cog.event()
    async def event_pubsub_bits(self, event: pubsub.PubSubBitsMessage):
        # do stuff on bit redemptions
        print(f"{event.message.content = }")
        print(f"{event.user.name} redeemed {event.bits_used} bits")
        MESSAGE = f"Thanks @{event.user.name} for the bits! You're real swell!"
        
        self.send_message(MESSAGE)

    # === SUBSCRIPTIONS ==================

    @commands.Cog.event()
    async def event_pubsub_subscription(self, event: pubsub.channel_subscriptions):
        print(f"{event.user.name} subscribed!")

def prepare(bot):
    bot.add_cog(PubSubCog(bot))