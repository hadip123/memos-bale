from bale import Bot, Update, Message, SuccessfulPayment, LabeledPrice
import requests
import os
from dotenv import load_dotenv

load_dotenv()
memos_token = os.getenv("MEMOS_TOKEN")
memos_host = os.getenv("MEMOS_HOST")
client = Bot(token=os.getenv("BALE_TOKEN"))


@client.event
async def on_ready():
    print(client.user, "is Ready!")


@client.event
async def on_message(message: Message):
    if (str(message.author.id) != os.getenv("BALE_USER_ID")):
        await message.reply("متأسفم. شما اجازه بهره برداری از این بازو را ندارید.")
        return
    print(message.content, ' saving to memos')
    response = save_in_memos(message.content)

    if (response.status_code != 200):
        await message.reply("نتونستم ذخیرش کنم. شرمنده\n{}".format(response.json()))
        return

    await message.reply("ذخیره شد!")


@client.event
async def on_successful_payment(successful_payment: SuccessfulPayment):
    print("We Receive an payment From {}".format(successful_payment.payload))


def save_in_memos(content: str):
    url = "{}/api/v1/memos".format(memos_host)
    payload = {
        "content": content,
        "visibility": "PUBLIC",
        "resources": [
        ],
        "relations": [
        ]
    }
    headers = {
        "Authorization": "Bearer {}".format(memos_token)
    }
    response = requests.post(url, json=payload, headers=headers)

    return response


client.run()
