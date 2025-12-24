from telethon import TelegramClient
import asyncio

api_id = 11111111
api_hash = 'HASH'
phone_number = '+38096********'

client = TelegramClient('my_session', api_id, api_hash)


async def main():
    target_group = 'python'

    try:
        participants = await client.get_participants(target_group, limit=5)
        for user in participants:
            print(f"ID: {user.id} | Name: {user.first_name} {user.last_name or ''} | User: @{user.username}")

    except Exception as e:
        print(e)

    await client.send_message('me', 'Test message from Telethon script')


if __name__ == '__main__':
    client.start(phone=phone_number)

    with client:
        client.loop.run_until_complete(main())