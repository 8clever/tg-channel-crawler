
import asyncio
from os import environ
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
    print(f'Invite: {id}')
    try:
      await client(InviteToChannelRequest(
        channel,
        [id]
      ))
      await asyncio.sleep(1)
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
    users.remove(id)
    with open(file_path, 'w') as f:
      f.write('\n'.join(users))

    print(f'Done {n}/{total}')

  print("Invite completed")

asyncio.run(main())