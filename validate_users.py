
import asyncio
from os import environ
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.types import Channel
from authorize import authorize
from telethon.hints import EntitiesLike

async def validate_user (client: TelegramClient, id: EntitiesLike):
  try:
    entity = await client.get_entity(id)
  except Exception as e:
    msg = str(e)
    invalid_user = (
      'Nobody is using this username' in msg or
      'No user' in msg
    )
    if invalid_user:
      return False
    raise e

  if isinstance(entity, (Channel)):
    return False
  
  is_invalid = (
    entity.deleted or
    entity.bot or 
    entity.mutual_contact
  )
  return not is_invalid

async def main ():
  load_dotenv()

  file_name = 'blockDAGnetworkOfficial_usernames'
  with open(f'tmp/{file_name}.txt') as f:
    users = f.read().split('\n')

  api_id = int(environ.get("TG_API_ID"))
  api_hash = environ.get("TG_API_HASH")
  phone = environ.get("TG_PHONE")
  client = await authorize(phone, api_id, api_hash)
  n = 0
  for id in users:
    if n > 10:
      break
      
    is_valid = await validate_user(client, id)
    print(f'{id}, valid: {is_valid}')
    n += 1
  
  print(f'Valid users: {len(users)}')
  with open(f'tmp/{file_name}_valid.txt', 'w') as f:
    f.write('\n'.join(users))

  print("Validation completed")

if __name__ == "__main__":
  asyncio.run(main())