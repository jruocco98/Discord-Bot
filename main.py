import discord
from discord.ext import commands
from googleapiclient.discovery import build

TOKEN = 'OTg3NDU0NzQzNDAyMTQzODE1.GLjfqC.8HUR0ZxfIJtiFiuP7HyU2D4L5KQU1xL8FTeoTU'
api_key = 'AIzaSyBdUACxdjRAljBNGLg3pbEtloDqUp26PZM'
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello, ' + str(ctx.author).split('#')[0])


@client.command(name='google')
async def showImage(ctx,*, search):
    
    def check(reaction, user): 
        return str(reaction) == "➡️" or str(reaction) == '⬅️'
    
    async def searchList(resource, result):
        counter = 0
        for x in range(20):
            reaction = await client.wait_for("reaction_add", check=check)
            
            if(str(reaction[0]) == '➡️'  and counter < 9):
                counter += 1
                embed1.set_image(url=result['items'][counter]['link'])
                
                await msg.edit(embed=embed1)
                
            if(str(reaction[0]) == '⬅️' and counter > 0):
                counter -= 1
                embed1.set_image(url=result['items'][counter]['link'])
                
                await msg.edit(embed=embed1)    

    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(q=f'{search}', cx='75d9adc92598d4edf', searchType='image').execute()
    url1 = result['items'][0]['link']

    embed1 = discord.Embed(title=f'Images Result: {search.title()}')
    embed1.set_image(url=url1)
    msg = await ctx.send(embed=embed1)

    await msg.add_reaction("⬅️")
    await msg.add_reaction("➡️")

    await searchList(resource, result)
client.run(TOKEN)