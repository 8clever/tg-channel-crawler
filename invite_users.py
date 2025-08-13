
import asyncio
from os import environ
from dotenv import load_dotenv
from telethon.tl.functions.channels import InviteToChannelRequest
from authorize import authorize

load_dotenv()

file = 'tmp/blockDAGnetworkOfficial_usernames_valid.txt'

with open(file) as f:
  users = f.read().split('\n')

api_id = int(environ.get("TG_API_ID"))
api_hash = environ.get("TG_API_HASH")
phone = environ.get("TG_PHONE")
channel = environ.get("CHANNEL")

async def main ():
  client = await authorize(phone, api_id, api_hash)
  n = 0
  limit = 1000
  while True:
    start = n * limit
    end = start + limit
    chunk = users[start:end]
    await client(InviteToChannelRequest(
      channel,
      chunk
    ))
    print(f'Chunk completed {n}')
    if len(chunk) < limit:
      break
    n += 1

  print("Invite completed")

asyncio.run(main())