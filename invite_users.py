
import asyncio
from os import environ
from random import randrange
from dotenv import load_dotenv
from telethon.tl.functions.channels import InviteToChannelRequest
from authorize import authorize

load_dotenv()

file_name = 'blockDAGnetworkOfficial_usernames_pending'
file_path = f'tmp/{file_name}.txt'

with open(file_path) as f:
  users = f.read().split('\n')

api_id = int(environ.get("TG_API_ID"))
api_hash = environ.get("TG_API_HASH")
phone = environ.get("TG_PHONE")
channel = environ.get("CHANNEL")
total = len(users)

async def main ():
  client = await authorize(phone, api_id, api_hash)
  n = 0
  for id in users:

    # start inviting
    try:
      await client(InviteToChannelRequest(
        channel,
        [id]
      ))
      await asyncio.sleep(randrange(1, 5, 0.1))
      print(f'Invited {id}, Done {n}/{total}')

    # catch invalid users
    except Exception as e:
      msg = str(e)
      invalid_user = (
        id in msg or
        'The provided user is not a mutual contact' in msg
      )
      if invalid_user:
        print(f'Invalid user: {id}, removed!')
      else:
        raise e
      
    # remove user from pending state
    users.remove(id)
    with open(file_path, 'w') as f:
      f.write('\n'.join(users))

  print("Invite completed")

asyncio.run(main())