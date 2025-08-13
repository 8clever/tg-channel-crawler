
import asyncio
from os import environ
from dotenv import load_dotenv
from telethon.tl.functions.channels import InviteToChannelRequest
from authorize import authorize

load_dotenv()

file_name = 'blockDAGnetworkOfficial_usernames'

with open(f'tmp/{file_name}.txt') as f:
  users = f.read().split('\n')

api_id = int(environ.get("TG_API_ID"))
api_hash = environ.get("TG_API_HASH")
phone = environ.get("TG_PHONE")
channel = environ.get("CHANNEL")
total = len(users)

print(f'Loaded: {total}')

async def main ():
  client = await authorize(phone, api_id, api_hash)
  n = 0
  for id in users:
    try:
      user = await client.get_entity(id)
      if user.bot or user.deleted:
        users.remove(id)
    except:
      users.remove(id)

    print(f'Done {n}/{total}')
    n += 1
  
  print(f'Valid users: {len(users)}')
  with open(f'tmp/{file_name}_valid.txt', 'w') as f:
    f.write('\n'.join(users))

  print("Validation completed")

asyncio.run(main())