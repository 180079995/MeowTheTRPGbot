from src.init import *
import random
import src.funcs
import re
#import variables
#import combat

authed=["947763268154449980","7135999400264335571"]
lasers=[]

with open ("files\\Critical.txt","r",encoding='UTF-8') as f:
    Critical = f.read().splitlines()
with open ("files\\Fumble.txt","r",encoding='UTF-8') as f:  
    Fumble = f.read().splitlines()


@interactions.slash_command(
    name="roll",
    description="Roll dice.",
)
@interactions.slash_option(
            name="amount",
            description="In 'xDn+k' format, no spaces allowed. Description at the end.",
            opt_type=interactions.OptionType.STRING,
            required=True,
)
async def roll(ctx: interactions.SlashContext, amount: str):
    try:
        dice = amount.split(" ",1)+['']
        dice,description = dice[0],dice[1]
        if '<' in dice or '>' in dice:
            larger = '>' in dice
            equal = '=' in dice
            dice,limit = re.split("<|>",dice)
        else:
            limit = None
        dice = dice.split("+")
        nums = []
        for i in dice:
            k=re.split("d|D",i)
            if len(k)>1:
                nums.append(funcs.rolldice(int(k[0]),int(k[1])))
            else:
                nums.append([int(k[0])])
        sums = [sum(i) for i in nums]
        string = ''
        for i in range(len(sums)):
            string+=f" + {str(sums[i])} [{'+'.join(str(j) for j in nums[i])}]"
        total = sum(sums)
        if (limit):
            evalstr = f"{total}{'>' if larger else '<'}{limit}"
            if larger and equal:
                limit = "≧ "+limit[1:]
            elif equal:
                limit = "≦ "+limit[1:]
            await ctx.send(f"<@{ctx.user.id}> \n{amount}\n{string[3:]} = {total} {'' if equal else '>' if larger else '<'}{limit} -> {'成功'if eval(evalstr) else '失敗'} {description}")
        else:
            await ctx.send(f"<@{ctx.user.id}> \n{amount}\n{string[3:]} = {total} {description}")
    except:
        await ctx.send(":x:Syntax Error",ephemeral=True)

@interactions.slash_command(
    name="cc",
    description="Skill Check",
    )
@interactions.slash_option(
    name="value",
    description="An integer, and a description if you want.",
    opt_type=interactions.OptionType.STRING,
    required=True,
)
@interactions.slash_option(
    name="amount",
    description="An integer, how many dice you need?",
    opt_type=interactions.OptionType.INTEGER,
    required=False,
)
async def cc(ctx: interactions.SlashContext, value: str,amount = 1):
    try:
        value = value.split(" ",1)+['']
        value,description = int(value[0]),value[1]
        response = f'<@{ctx.user.id}> \n'
        for i in range(amount):
            dice = sum(funcs.rolldice(1,100))
            if dice<=5:
                status = Critical[random.randint(0,len(Critical)-1)]
            elif dice >=96:
                status = Fumble[random.randint(0,len(Fumble)-1)]
            elif dice <= value/5:
                status = "極限成功"
            elif dice <= value/2:
                status = "困難成功"
            elif dice <= value:
                status = "通常成功"
            else:
                status = "失敗"
            if amount == 1:
                response+=f"1D100 = {dice} ≦ {value} -> {status} {description}\n"
            else:
                response+=f"#{i+1}: 1D100 = {dice} ≦ {value} -> {status} {description}\n"
        await ctx.send(response)
    except:
        await ctx.send(":x:Syntax Error",ephemeral=True)

@interactions.slash_command(
    name="drcc",
    description="Skill Check",
)
@interactions.slash_option(
    name="value",
    description="An integer, and a description if you want.",
    opt_type=interactions.OptionType.STRING,
    required=True,
)
@interactions.slash_option(
    name="kp",
    description="The one who would recieve the result.",
    opt_type=interactions.OptionType.USER,
    required=True,
)
@interactions.slash_option(
    name="amount",
    description="An integer, how many dice you need?",
    opt_type=interactions.OptionType.INTEGER,
    required=False,
)

async def drcc(ctx: interactions.SlashContext, value: str, kp:interactions.models.discord.user.User, amount = 1):
    try:
        value = value.split(" ",1)+['']
        value,description = int(value[0]),value[1]
        response = f'來自<@{ctx.user.id}> \n'
        for i in range(amount):
            dice = sum(funcs.rolldice(1,100))
            if dice<=5:
                status = Critical[random.randint(0,len(Critical)-1)]
            elif dice >=96:
                status = Fumble[random.randint(0,len(Fumble)-1)]
            elif dice <= value/5:
                status = "極限成功"
            elif dice <= value/2:
                status = "困難成功"
            elif dice <= value:
                status = "通常成功"
            else:
                status = "失敗"
            if amount == 1:
                response+=f"1D100 = {dice} ≦ {value} -> {status} {description}\n"
            else:
                response+=f"#{i+1}: 1D100 = {dice} ≦ {value} -> {status} {description}\n"
        await ctx.send(f"暗骰給<@{kp.id}> {description}")
        await kp.send(response)
    except:
        await ctx.send(":x:Syntax Error",ephemeral=True)

@interactions.slash_command(
    name="secret",
    description="No one will know...",
)
@interactions.slash_option(
    name="text",
    description="Your text",
    opt_type=interactions.OptionType.STRING,
    required=True,
)


async def secret(ctx: interactions.SlashContext, text: str):
    await ctx.send("Secret sended.",ephemeral=True)
    await ctx.channel.send(text)


@interactions.slash_command(
    name="flag",
    description="Let's get a flag!",
)
async def flag(ctx: interactions.SlashContext ):
    with open (r"files\Flags.txt","r",encoding='UTF-8') as f:
        content = f.read().splitlines()
    flag = content[random.randint(1,len(content))-1]
    await ctx.send(f"<@{ctx.user.id}>\n{flag}")

@interactions.slash_command(
    name="laserbeam",
    description="Shoot Laserbeam!",
)
async def laserbeam(ctx: interactions.SlashContext ):
    length = random.randint(10,50)
    lasers.append(await ctx.send("```                                @@@@@@@@@@%*                \n         /%@@@@@@%.         @@@@@@@@@@@@@@@@@@@@@@@@@@*     \n  @@@@@@@@@@@@@@@@@@@@@@@@@@@@                     #@@@     \n  @@@                   @@@,                       @@@%     \n  @@@%                              (@@@@@@(       @@@      \n  @@@%                               @@@@  @       @@@      \n @@@@                                @@@@& @       @@@,     \n @@@                                               @@@@     \n@@@@                           @@@@@@              #@@@     \n @@@                             @@@@@@             @@@.    \n  @@@&                            @@@@@              @@@@/  \n  @@@&                         ,@@@@@      ((          @@@# \n  @@@                                 @@@@@  @       @@@@@  \n  @@@@*                               @@@@@@@@@  @@@@@@     \n    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@      @@@@  @@@@@@@        \n                               @@@@@@@@@@@@@@@@@            ```"))
    for i in range(5):
        lasers.append(await ctx.channel.send("```                                ||           ||\n```"*(length//5)))
    lasers.append(await ctx.channel.send("```                                ||           || \n                               ||             ||\n                              ||               ||\n                             ||                 ||\n                              ||               ||\n                               |||           |||\n                                 |||||||||||||\n\n```"))
    #send Dead.png
    lasers.append( await ctx.channel.send(file=interactions.File(r"files\Dead.png", file_name="Dead.png")))

@interactions.slash_command(
    name="deletelaser",
    description="Delete all Laserbeam!",
)
async def deletelaser(ctx: interactions.SlashContext ):
    await ctx.defer()
    while lasers:
        await lasers.pop().delete()
    await ctx.send("Clear!",ephemeral=True)
    await ctx.channel.send(file=interactions.File(r"files\Tomb.png", file_name="Tomb.png"))
