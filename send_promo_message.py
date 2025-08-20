
import asyncio
from os import environ
from dotenv import load_dotenv
from authorize import authorize

load_dotenv()

file_name = 'blockDAGnetworkOfficial_usernames'
file_pending = f'{file_name}_pending_invites'

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

messages = [
  '''🚀 Unlock the Future! 🔬 Join **Co.Ca. Lab** for exclusive insights, trending tech, and mind-blowing ideas! 💡
Subscribe now and stay ahead of the curve! 📱 @co_ca_lab'''
]

async def main ():
  client = await authorize(phone, api_id, api_hash)

  for id in users:
    try:
      for m in messages:
        await client.send_message(id, m, parse_mode='Markdown')
      print(f'Message sended to: {id}')
    except Exception as e:
      err = str(e)
      is_expected_error = (
        'No user' in err or
        'Nobody is using this username' in err or
        'PRIVACY_PREMIUM_REQUIRED' in err
      )
      if not is_expected_error:
        raise e
      print(f'{id} - {err}')

    # remove users from pending state
    users.remove(id)

    # store pending state
    save()

  print("Invite completed")

asyncio.run(main())