
import asyncio
from os import environ
from dotenv import load_dotenv
from telethon.tl.functions.channels import InviteToChannelRequest
from authorize import authorize
from validate_users import validate_user

load_dotenv()

file_name = 'blockDAGnetworkOfficial_usernames'
file_pending = f'{file_name}_pending'

def file_name_to_path (name: str):
  return f'tmp/{name}.txt'

def save ():
  with open(file_name_to_path(file_pending), 'w') as f:
    f.write('\n'.join(users))

users: list[str] = []

try:
  with open(file_name_to_path(file_pending)) as f:
    users = f.read().split('\n')
except:
  with open(file_name_to_path(file_name)) as f:
    users = f.read().split('\n')
  save()

api_id = int(environ.get("TG_API_ID"))
api_hash = environ.get("TG_API_HASH")
phone = environ.get("TG_PHONE")
channel = environ.get("CHANNEL")
total = len(users)
limit_per_invite = 50
validate = True

async def main ():
  client = await authorize(phone, api_id, api_hash)
  invite_list = []

  for id in users:
    # validate user
    if validate:
      is_valid_user = await validate_user(client, id)
      print(f'{id}, valid: {is_valid_user}, {len(invite_list)}/{limit_per_invite}')
      
      if not is_valid_user:
        users.remove(id)
        save()
        continue
    
    # add user to batch request
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

    # clean batch list
    invite_list = []
    
    # stop processing, try to one batch per account
    break

  print("Invite completed")

asyncio.run(main())