from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackQueryHandler
from database.query import get_product
from filters.helpers import compute_rates
from dotenv.main import load_dotenv
import os
from database.manipulate import push_order
from database.query import get_user_name, get_user_room

load_dotenv()




def checkout(update, bot):
    query = update.callback_query
    # data = update.callback_query.data
    total = int(bot.user_data["cart_total"])
    rate = compute_rates(total)
    reply_keyboard = [
        [
            InlineKeyboardButton(text="Bank tranfer to Byte n Crunch", callback_data="pay_with_direct_transfer")
        ] ,
        [
            InlineKeyboardButton(text="Pay with FLutterwave", callback_data="pay_with_flutter_wave")
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text=f"You total comes down to # {total+rate} \n Subtotal: #{total} \n Shipping : #{rate}",
        reply_markup=markup,
    )

def direct_transfer(update, bot):
    query = update.callback_query
    total = int(bot.user_data["cart_total"])
    acc_name = os.environ["ACCOUNT_NAME"]
    acc_no =  os.environ["ACCOUNT_NUMBER"]
    bank =  os.environ["BANK"]
    text_to_send = f"Make a tranfer of #{total} to the account given below: \n Account Name = {acc_name} \n Account Number = {acc_no} \n Bank = {bank}"
    reply_keyboard = [
         [
            InlineKeyboardButton(text="I've made the Transfer!", callback_data="direct_payment_confirm")
        ],
         [
            InlineKeyboardButton(text="Back to home!", callback_data="start")
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text=text_to_send,
        reply_markup=markup,
    )

def confirm_direct_transfer(update, bot):
    query = update.callback_query
    # user_name = os.environ["byte_user_name"]
    total = int(bot.user_data["cart_total"])
    name = get_user_name(update.effective_user.id)
    room = get_user_room(update.effective_user.id)
    print(name)
    text_to_send = f"Thanks you for choosing us! \n Please send a copy of your transfer receipt to @david_ornstien or @mikeyruled to begin processing your order"
    push_order(bot.user_data["cart"],update.effective_user.id,name,int(bot.user_data["cart_total"]))
    my_text = f"Order for {name}, "
    print()
    for i in list(bot.user_data["cart"].items()):
        product = get_product(i[0])
        my_text += f"\n >> {i[1]} order(s) of {product[1]} at # {int(product[3]) * i[1]} \n Delivered to {room}"

    my_text += f" \n Total(plus shipping) = {total}"
    reply_keyboard = [
         [
            InlineKeyboardButton(text="Back to home!", callback_data="start")
        ]
    ]
    bot.bot.send_message(chat_id=-4050264876, text=my_text)
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text=text_to_send,
        reply_markup=markup,
    )
    bot.user_data["cart"] = {}
    bot.user_data["cart_total"] = 0



check_out_handler = CallbackQueryHandler(callback=checkout, pattern="checkout")
direct_transfer_handler = CallbackQueryHandler(callback=direct_transfer, pattern="pay_with_direct_transfer")
confirm_direct_transfer_handler =  CallbackQueryHandler(callback=confirm_direct_transfer, pattern="direct_payment_confirm")

