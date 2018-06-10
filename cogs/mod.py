import discord
from discord.ext import commands
import random, asyncio, aiohttp

class mod():
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, user):
        x = await self.bot.db.welcome.find_one({"id": str(user.guild.id)})
        if not x:
            return
        channel = int(x['channel'])
        send_channel = self.bot.get_channel(channel)
        if not send_channel:
            return
        await send_channel.send(f"Welcome {user.mention} to the guild!")

    @commands.command()
    async def welcome(self, ctx):
        await ctx.send("Please mention the channel to set welcome messages in.")
        try:
            x = await self.bot.wait_for("message", check=lambda x: x.channel == ctx.channel and x.author == ctx.author, timeout=60.0)
        except asyncio.TimeoutError:
            return await ctx.send("Request timed out. Please try again.")
        if not x.content.startswith("<#") and not x.content.endswith(">"):
            return await ctx.send("Please properly mention the channel.")
        channel = x.content.strip("<#").strip(">")
        try:
            channel = int(channel)
        except ValueError:
            return await ctx.send("Did you properly mention a channel? Probably not.")
        await self.bot.db.welcome.update_one({"id": str(ctx.guild.id)}, {"$set": {"channel": channel} }, upsert=True )
        await ctx.send("I have set the welcome channel!")

def setup(bot):
    bot.add_cog(mod(bot))
