
import asyncio
from os import environ
from dotenv import load_dotenv
from telethon.tl.functions.channels import InviteToChannelRequest
from authorize import authorize

load_dotenv()

file = 'tmp/blockDAGnetworkOfficial_usernames.txt'

with open(file) as f:
  users = f.read().split('\n')

api_id = int(environ.get("TG_API_ID"))
api_hash = environ.get("TG_API_HASH")
phone = environ.get("TG_PHONE")
channel = environ.get("CHANNEL")

async def main ():
  client = await authorize(phone, api_id, api_hash)

  await client(InviteToChannelRequest(
    channel,
    users
  ))

  print("Invite completed")

asyncio.run(main())