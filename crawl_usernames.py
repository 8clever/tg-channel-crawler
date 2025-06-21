import asyncio
from datetime import datetime
from authorize import authorize
from dotenv import load_dotenv
from os import environ

load_dotenv()

api_id = int(environ.get("TG_API_ID"))

api_hash = environ.get("TG_API_HASH")

phone = environ.get("TG_PHONE")

channel = environ.get("CHANNEL")

def save (data: dict):
  with open(f'tmp/{channel}_usernames.txt', 'w') as fp:
    txt = "\n".join(data.values())
    fp.write(txt)
    print("File saved!")

async def main ():
  client = await authorize(phone, api_id, api_hash)

  usernames = dict()

  checked = dict()

  msgs = await client.get_messages(channel, 0)

  total = msgs.total

  completed = 0
  
  now = datetime.now().timestamp()

  async for m in client.iter_messages(channel):
    completed += 1

    if getattr(m, 'sender', None) and getattr(m.sender, 'bot', None):
      continue

    id = getattr(m.from_id, 'user_id', None)
    if checked.get(id):
      continue

    sender = await m.get_sender()
    checked[id] = 1
    if sender and sender.username:
      usernames[id] = sender.username
      print(f'Done {completed}/{total} {m.date}')

    delta = datetime.now().timestamp() - now
    if delta < 60:
      continue

    now = datetime.now().timestamp()
    save(usernames)

  save(usernames)
  print(f'{channel} crawled successfully!')


asyncio.run(main())