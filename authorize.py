from telethon import TelegramClient

async def authorize (phone: str, api_id: int, api_hash: str):
  client = TelegramClient('authorized/' + phone, api_id, api_hash)

  await client.connect()

  if not await client.is_user_authorized():
      await client.send_code_request(phone)
      print(f'Code sended to phone: {phone}. Please fill code below')
      code = input('Enter the Telegram code: ')
      try:
          await client.sign_in(phone, code)
      except:
        exit()

  return client