from random import randint
import interactions
with open(r'files\token.txt') as f:
    token = f.read()
client = interactions.Client(token = token)

@interactions.listen()
async def on_ready():
    print('Bot start!')

