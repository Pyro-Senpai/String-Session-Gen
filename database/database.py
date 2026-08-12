# (©)Pyro-Senpai

import motor.motor_asyncio
import config

dbclient = motor.motor_asyncio.AsyncIOMotorClient(config.DATABASE_URI)
database = dbclient[config.DATABASE_NAME]
user_data = database['users']

async def present_user(user_id: int):
    found = await user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(client, message):
    user = message.from_user
    if not user:
        return
    
    if not await present_user(user.id):
        user_dict = {
            '_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        try:
            await user_data.insert_one(user_dict)
        except Exception as e:
            print(f"Error adding user to database: {e}")
