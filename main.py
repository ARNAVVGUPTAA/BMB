import os
import disnake
import pyrebase
import datetime
import random
import time
import asyncio

from disnake.ext import commands
# from disnake.ext import menus

firebase = pyrebase.initialize_app({
  "apiKey": "-",
  "authDomain": "bmbot-43d67.firebaseapp.com",
  "databaseURL": "https://bmbot-43d67-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "bmbot-43d67",
  "storageBucket": "bmbot-43d67.appspot.com",
  "messagingSenderId": "155496611438",
  "appId": "1:155496611438:web:16c67eccacd8ac46caf07f",
  "measurementId": "G-70ZS3JVECZ"
})

db = firebase.database()

intents = disnake.Intents().all()
client = commands.Bot(command_prefix='~',
                      case_insensitive=True, intents=intents)
client.remove_command("help")


@client.event
async def on_ready():
    one = 1
    onee = 1
    print("ALL HAIL THE GREAT LUCIFER!!!")
    while one == onee:
        status = random.choice([disnake.Status.online,disnake.Status.idle, disnake.Status.dnd])
        await client.change_presence(status= status, activity=disnake.Activity(type=random.choice([1,2,3,4,5]), name= f"{random.choice(['KACHA BADAM','PICHHE TOH DEKHO','BASSPAN KA PYAAR','PAGALPAN','SHITTY BUSINESS','ASSTG','EREN JAEGER','CHUTIYAPA','NIMBUDA','SHIN- HEHE'])} | ~help"))
        await asyncio.sleep(30)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        erem = disnake.Embed(
            title="Command Cooldown",
            description="You cant use this command now. Try after **%.0fs**" %
                        error.retry_after)
        await ctx.send(embed=erem)

    elif isinstance(error, commands.MissingRole):
        erem1 = disnake.Embed(
            title="Missing Role",
            description=f"You dont have role {error.missing_role} to run that command.")
        await ctx.send(embed=erem1)
    else:
        raise error

@client.command()
async def help(ctx):
    embed = disnake.Embed(title="HELP", description = "Here, you would get description and syntax of all the commands and how to use the bot for sending images and gifs", color=0x000000, timestamp=datetime.datetime.now())

    embed.set_thumbnail(url="https://media.discordapp.net/attachments/930692963472924674/936668521792954388/image_2.png")

    embed.set_footer(
    text=f"~help invoked by {ctx.author.display_name}",
    icon_url=ctx.author.avatar.url,
    )

    embed.add_field(name="addgif", value="Syntax: `~addgif (paste gif link or attach a gif)`", inline=False)
    embed.add_field(name="addimg", value="Syntax: `~addimg (paste image link or attach an image)`",inline=False)
    embed.add_field(name="giflist", value="Gives you all the usable gif names to send", inline=False)
    embed.add_field(name="imglist", value="Gives you all the usable image names to send", inline=True)
    embed.add_field(name="You can send a gif or an image with putting gif or image name in dots", value="An example would be `.bmb.`", inline=False)
    await ctx.reply(embed=embed)
@client.command()
async def test(ctx):
    await ctx.send("ASSTG <a:kesaribolbsdk:934821940697366558>")
    
@client.command()
async def giflist(ctx):
    gifarray = db.child("BMB").child("gifs").shallow().get().val()
    # allgifs = 
    sender= '\n'.join(map(str, gifarray))
    embed = disnake.Embed(title="Here is the list of all the gif aliases:", description= sender , color=0x000000, timestamp=datetime.datetime.now())
    embed.set_footer(
    text=f"~giflist invoked by {ctx.author.display_name}",
    icon_url=ctx.author.avatar.url,
    )
    await ctx.send(embed=embed)

@client.command()
async def imglist(ctx):
    imgarray = db.child("BMB").child("imgs").shallow().get().val()
    sender= '\n'.join(map(str, imgarray)) 
    embed = disnake.Embed(title="Here is the list of all the image aliases:", description= sender , color=0x000000, timestamp=datetime.datetime.now())
    embed.set_footer(
    text=f"~imglist invoked by {ctx.author.display_name}",
    icon_url=ctx.author.avatar.url,
    )
    await ctx.send(embed=embed)

@client.command()
async def add(ctx, type, key, url = None):
    if type.lower() == "g" or type.lower() == "gif":
        if url != None:
            if db.child("BMB").child("gifs").child(key).get().val() is None:
                db.child("BMB").child("gifs").child(key).set(url)
                await ctx.reply(f"alias {key} added with gif {url}")
            else:
                await ctx.reply(f"`{key}` already exists")
        else:
            if db.child("BMB").child("gifs").child(key).get().val() is None:
                db.child("BMB").child("gifs").child(key).set(ctx.message.attachments[0].url)
                await ctx.reply(f"alias {key} added with gif {ctx.message.attachments[0].url}")
    elif type.lower() == "i" or type.lower() == "img":
        if url != None:
            if db.child("BMB").child("imgs").child(key).get().val() is None:
                db.child("BMB").child("imgs").child(key).set(url)
                await ctx.reply(f"alias {key} added with image {url}")
            else:
                await ctx.reply(f"`{key}` already exists")
        else:
            if db.child("BMB").child("imgs").child(key).get().val() is None:
                db.child("BMB").child("imgs").child(key).set(ctx.message.attachments[0].url)
                await ctx.reply(f"alias {key} added with image {ctx.message.attachments[0].url}")
    else:
        await ctx.reply("Invalid Argument: the syntax is `~add` (`gif` or `image`) (`url` or attach an image or gif)")

@client.command()
async def addgif(ctx, gifname, giflink = None):
    if giflink != None:
        if db.child("BMB").child("gifs").child(gifname).get().val() is None:
            db.child("BMB").child("gifs").child(gifname).set(giflink)
            await ctx.send(f"alias {gifname} added with gif {giflink}")
        else:
            await ctx.send(f"{gifname} already exists")
    else:
        if db.child("BMB").child("gifs").child(gifname).get().val() is None:
            db.child("BMB").child("gifs").child(gifname).set(ctx.message.attachments[0].url)
            await ctx.send(f"alias {gifname} added with gif {ctx.message.attachments[0].url}")

@client.command()
async def addimg(ctx, imgname, imglink = None):
    if imglink != None:
        if db.child("BMB").child("imgs").child(gifname).get().val() is None:
            db.child("BMB").child("imgs").child(gifname).set(imglink)
            await ctx.send(f"alias {imgname} added with image {imglink}")
        else:
            await ctx.send(f"{imgname} already exists")
    else:
        if db.child("BMB").child("imgs").child(imgname).get().val() is None:
            db.child("BMB").child("imgs").child(imgname).set(ctx.message.attachments[0].url)
            await ctx.send(f"alias {imgname} added with image {ctx.message.attachments[0].url}")

@client.command()
@commands.has_role("Techie")
async def remove(ctx, name):
    if db.child("BMB").child("gifs").child(name).get().val() is not None:
        db.child("BMB").child("gifs").child(name).remove()
        await ctx.send(f"Removed gif {name}")
    elif db.child("BMB").child("imgs").child(name).get().val() is not None:
        db.child("BMB").child("imgs").child(name).remove()
        await ctx.send(f"Removed image {name}")
    else:
        await ctx.send(f"Couldn't remove {name}")


@client.command()
async def good(ctx):
    # If this message has a reference (meaning it's a reply)
    if ctx.message.reference:
        original = await ctx.fetch_message(ctx.message.reference.message_id)
        text = original.content
        await ctx.send(text)

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.content.startswith(".") and message.content.endswith("."):
        gifarray = db.child("BMB").child("gifs").shallow().get().val()
        imgarray = db.child("BMB").child("imgs").shallow().get().val()
        view = disnake.ui.View()
        item2 = disnake.ui.Button(style=disnake.ButtonStyle.grey  , label=f"as requested by {message.author.display_name}",disabled=True)
        item3 = disnake.ui.Button(style=disnake.ButtonStyle.blurple , label=f"{message.content}",disabled=True)
        view.add_item(item=item2)
        view.add_item(item=item3)
        for x in gifarray:
            if x == message.content.replace(".",""):
                if message.reference:
                    await message.delete()
                    item4 = disnake.ui.Button(emoji="🌐", label="Jump to the message",url=message.reference.resolved.jump_url, row=1)
                    embed = disnake.Embed(description=message.reference.resolved.content, color=0x000000)
                    embed.set_author(name=message.reference.resolved.author.display_name, icon_url=message.reference.resolved.author.avatar.url)
                    view.add_item(item=item4)
                    await message.channel.send(embed=embed)
                    await message.channel.send(content=f"{db.child('BMB').child('gifs').child(x).get().val()}", view=view)
                else:
                    await message.delete()
                    await message.channel.send(content=db.child("BMB").child("gifs").child(x).get().val(), view=view)

        for x in imgarray:
            if x == message.content.replace(".",""):
                if message.reference:
                    await message.delete()
                    item4 = disnake.ui.Button(emoji="🌐", label="Jump to the message", url=message.reference.resolved.jump_url, row=1)
                    embed = disnake.Embed(description=message.reference.resolved.content, color=0x000000)
                    embed.set_author(name=message.reference.resolved.author.display_name, icon_url=message.reference.resolved.author.avatar.url)
                    view.add_item(item=item4)
                    await message.channel.send(embed=embed)
                    await message.channel.send(content=f"{db.child('BMB').child('imgs').child(x).get().val()}", view=view)
                else:
                    await message.delete()
                    await message.channel.send(content=db.child("BMB").child("imgs").child(x).get().val(), view=view)

@client.slash_command()
async def ping(inter):
    await inter.response.send_message(f"Pong!\nLatency: {round(client.latency * 1000)}" + " ms" + " <a:therki:934818828066635776>")

Choice = commands.option_enum(["gifs", "imgs"])
@client.slash_command(guild_ids=[930692962688581673, 859871286296576031], description="To preview the GIF/Image you want to send")
async def preview(inter, choice: Choice, name):
    view = disnake.ui.View()
    btn = disnake.ui.Button(style=disnake.ButtonStyle.blurple , label=f".{name}.",disabled=True)
    # embed = disnake.Embed(title=name, image=db.child('BMB').child(choice).child(name).get().val(), color=0x000000)
    if db.child('BMB').child(choice).child(name).get().val() is not None:
        await inter.response.send_message(db.child('BMB').child(choice).child(name).get().val(), ephemeral=True, view=view)
        view.add_item(item=btn)
    else:
        await inter.response.send_message(f"couldn't preview the gif/image {name}. Are you sure it is a valid alias?", ephemeral=True, view=view)

client.run('OTMyODg5MDEwOTIwMTE2MjM0.YeZimA.etZDEuhNZ22O2Q7LUO6i5AwoymA')
