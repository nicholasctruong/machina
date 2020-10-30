import os
import random
from dotenv import load_dotenv    #comment out for heroku deployment
import discord
from discord.ext import commands
import statements
intents = discord.Intents.default()
intents.members = True

load_dotenv()             #comment out for heroku deployment
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.', intents = intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

async def get_user(ctx, target=''):
    '''helper function to return member based on a string search'''
    if target.strip() == '':
        raise commands.errors.MemberNotFound(ctx)
    target_members = await ctx.guild.query_members(target)
    if len(target_members) == 0:
        raise commands.errors.MemberNotFound(ctx)
    target_member = target_members[0]
    return target_member

@bot.command(name='compliment', help='Compliments the user that you tag, add "aloud" to compliment in tts')
async def compliment(ctx, target='', tts=None):
    target_member = await get_user(ctx, target)
    if target_member == bot.user:
        target_member = ctx.author
        await ctx.send('awe thanks!')
    compliments = statements.compliments
    response = random.choice(compliments)
    if tts == 'aloud':
        await ctx.send(f'<@{target_member.id}>, {response}', tts=True)
    else:
        await ctx.send(f'<@{target_member.id}>, {response}')

@bot.command(name='insult', help='Insults the user that you tag, add "aloud" to insult in tts')
async def insult(ctx, target='', tts=None):
    target_member = await get_user(ctx, target)
    if target_member == bot.user:
        target_member = ctx.author
        await ctx.send('damn you really tried and failed')
    insults = statements.insults
    response = random.choice(insults)
    if tts == 'aloud':
        await ctx.send(f'<@{target_member.id}>, {response}', tts=True)
    else:
        await ctx.send(f'<@{target_member.id}>, {response}')

@bot.command(name='pic', help='Generates a random emoji from the server\'s custom emoji list')
async def pic(ctx):
    emojis = bot.emojis
    if len(emojis) == 0:
        await ctx.send(f'Sorry, no custom emojis found on this server!')
    else:
        emoji = random.choice(emojis)
        await ctx.send(f'{emoji}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MemberNotFound):
        await ctx.send(f'Sorry! user not found, please try again')

bot.run(TOKEN)