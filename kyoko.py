import os
import random
# from dotenv import load_dotenv    #comment out for heroku deployment
import discord
from discord.ext import commands
import statements

# load_dotenv()             #comment out for heroku deployment
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='compliment', help='Compliments the user that you tag, add "aloud" to compliment in tts')
async def compliment(ctx, target: discord.Member, tts=None):
    if target == bot.user:
        target = ctx.author
        await ctx.send('awe thanks!')
    compliments = statements.compliments
    response = random.choice(compliments)
    if tts == 'aloud':
        await ctx.send(f'{target.nick}, {response}', tts=True)
    else:
        await ctx.send(f'{target.nick}, {response}')

@bot.command(name='insult', help='Insults the user that you tag, add "aloud" to insult in tts')
async def insult(ctx, target: discord.Member, tts=None):
    if target == bot.user:
        target = ctx.author
        await ctx.send('damn you really tried and failed')
    insults = statements.insults
    response = random.choice(insults)
    if tts == 'aloud':
        await ctx.send(f'{target.nick}, {response}', tts=True)
    else:
        await ctx.send(f'{target.nick}, {response}')




@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MemberNotFound):
        await ctx.send(f'Sorry! user not found, please try again')

bot.run(TOKEN)