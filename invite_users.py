
import asyncio
from os import environ
from random import randrange
from dotenv import load_dotenv
from telethon.tl.functions.channels import InviteToChannelRequest
from authorize import authorize
from validate_users import validate_user

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

def save ():
  with open(file_path, 'w') as f:
    f.write('\n'.join(users))

async def main ():
  client = await authorize(phone, api_id, api_hash)
  limit_per_invite = 20
  invite_list = []
  
  for id in users:
    # add users to batch request
    is_valid_user = await validate_user(client, id)
    if not is_valid_user:
      users.remove(id)
      save()
      continue

    invite_list.append(id)
    if len(invite_list) < limit_per_invite:
      continue

    # start inviting
    await client(InviteToChannelRequest(channel, invite_list))
    print(f'Invited {", ".join(invite_list)}')

    # remove users from pending state
    for i in invite_list:
      users.remove(i)

    # store pending state
    save()

  print("Invite completed")

asyncio.run(main())