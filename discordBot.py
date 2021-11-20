import os,sqlite3,discord
from discord.ext import commands
from model import model
model.load() 

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='?',intents=intents)

global maxWarnings
global punishment
maxWarnings = 5
punishment = "kick"




#events
@bot.event 
async def on_ready():
  print("Bot is ready")

@bot.event
async def on_guild_join(guild):
  print (f"Bot deployed to server:{guild} ")
  conn = sqlite3.connect(guild.name+"-database.db")
  cursor = conn.cursor()
  cursor.execute("CREATE TABLE IF NOT EXISTS warnings (name TEXT, amount_of_warnings INTEGER)")



  params = [(member.name+"#"+member.discriminator, 0) for member in guild.members]
  cursor.executemany("INSERT INTO warnings VALUES(?,?)", params)
  conn.commit()
  conn.close()


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  
  await bot.process_commands(message)

  global maxWarnings
  global punishment


  if model.predict(message):
    author = str(message.author)
    await message.delete()
    await message.channel.send("Be nice "+message.author.mention)

    # database update stuff
    conn = sqlite3.connect(message.guild.name+"-database.db")
    cursor = conn.cursor()
    warnings = cursor.execute("SELECT amount_of_warnings FROM warnings WHERE name = ?",(author,)).fetchall()[0][0]
    if warnings >= maxWarnings-1:

      if punishment =="ban":
        await message.author.ban(reason="Be nice, if you think this is a mistake, contact the moderator team")
        cursor.execute("UPDATE warnings SET amount_of_warnings = 0 WHERE name = ?",(author,))
      
      else:
        await message.author.kick()
        cursor.execute("UPDATE warnings SET amount_of_warnings = 0 WHERE name = ?",(author,))
      

    else:
      cursor.execute("UPDATE warnings SET amount_of_warnings = ? WHERE name = ?",(warnings+1, author))
      await message.channel.send(message.author.mention+", you've been warned. Amount of warnings:"+str(warnings+1))
    conn.commit() 
    conn.close()

#commands
@bot.command()
async def viewWarnings(ctx):
  print(f"User {ctx.author} has requested to view warnings.")

  conn = sqlite3.connect(ctx.guild.name+"-database.db")
  cursor = conn.cursor()
  amountOfWarnings = cursor.execute("SELECT amount_of_warnings FROM warnings WHERE name = ?",(str(ctx.author),)).fetchall()[0][0]

  print(f"User {ctx.author} request to view warnings was fulfilled.")

  await ctx.channel.send(ctx.author.mention+", Your amount of warnings is: "+str(amountOfWarnings))

  conn.close()

@bot.command()
async def toggle(ctx, newMaxWarnings=5, newPunishment="kick"):
  global maxWarnings
  global punishment
  
  if type(newMaxWarnings)!=int:
    await ctx.channel.send(ctx.author.mention+", You cannot set the max warnings to anything other than an integer!")
    return
  
  if newPunishment!="kick" and newPunishment!="ban":
    await ctx.channel.send(ctx.author.mention+", You cannot set the punishment to anything other than ban or kick!")
    return
  
  maxWarnings = newMaxWarnings
  punishment = newPunishment

  await ctx.channel.send(ctx.author.mention+", Your changes were made.")









bot.run(os.environ['DISCORD TOKEN'])