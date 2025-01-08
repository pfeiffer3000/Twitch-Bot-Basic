from twitchio.ext import commands
import asyncio

prefix_char = "!"  # the prefix for commands


class ChatMethodCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_name = "your_channel_name"  # the channel id
       

    # ============= put commands below here ======================

    # === send single message =============================================================

    @commands.command()
    async def test(self, ctx: commands.Context):
        '''
        Test the system
        '''
        await ctx.send(f'Testing of the Mugtion Testing system complete @{ctx.author.name}!')

    @commands.command(name="commands", aliases=["help", "imlost"])
    async def commands_command(self, ctx: commands.Context):
        '''
        List all the commands available
        '''
        commands_list = []
        for k in self._commands:
            commands_list.append(k)
        commands_str = ', '.join(commands_list)
        await ctx.send(commands_str)
 

    # === send multiple messages ========================================================================

    # general function that sends multiple messages, useful for lists of messages
    async def send_multiple(self, temp_list, sleep_time=2):
        channel = self.bot.get_channel(self.channel_name)
        for t in temp_list:
            await channel.send(t)
            await asyncio.sleep(sleep_time)

    @commands.command()
    async def info(self, ctx: commands.Context):
        '''
        An example of sending multiple messages
        '''
        temp_list = ["Line one of test message", "This is another line of the test message"]
        task = asyncio.create_task(self.send_multiple(temp_list))
    
 
    # =========================================

def prepare(bot):
    bot.add_cog(ChatMethodCog(bot))