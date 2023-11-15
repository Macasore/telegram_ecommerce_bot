from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackQueryHandler
from database.query import get_all_vendors


# *add funtion to fetch product data before sending to browse product handler
# *integrate with ibiang's api

def browse_shops_init(update, bot):
    vendors = get_all_vendors()
    print(vendors)
    bot.user_data["vendors"] = vendors
    browse_state = 5
    bot.user_data["browse_state"] = browse_state
    my_vendors = vendors[0:browse_state]
    buttons = []
    for vendor in my_vendors:
        buttons.append(
            [InlineKeyboardButton(text=vendor[1], callback_data=f"browse_shop_{vendor[0]}")]
        )
    reply_keyboard = buttons + [
        
            [InlineKeyboardButton(text="Next", callback_data="browse_vendors_next"),
            InlineKeyboardButton(text="Previous", callback_data="browse_vendors_previous")]
        
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    bot.bot.send_message(
        chat_id=update.effective_chat.id,
        text="What do you feel like getting today?",
        reply_markup=markup,
    )

def browse_vendors(update,bot):
    query = update.callback_query
    match update.callback_query.data:
        case "browse_vendors_next":
            state = bot.user_data["browse_state"]
            my_vendors = bot.user_data["vendors"][state:state+5]
            bot.user_data["browse_state"] = state + 5
            buttons = []
            for vendor in my_vendors:
                buttons.append(
                    [InlineKeyboardButton(text=vendor[1], callback_data=f"browse_shop_{vendor[0]}")]
                )
            reply_keyboard =buttons+ [
                
                [
                    [InlineKeyboardButton(text="Next", callback_data="browse_vendors_next")],
                    [InlineKeyboardButton(text="Previous", callback_data="browse_vendors_previous")]
                ]
            ]
            
            
        case "browse_vendors_previous":
            state = bot.user_data["browse_state"]
            if state > 5:
                state = bot.user_data["browse_state"]
                my_vendors = bot.user_data["vendors"][state-5:state]
                bot.user_data["browse_state"] = state - 5
                buttons = []
                for vendor in my_vendors:
                    buttons.append(
                        [InlineKeyboardButton(text=vendor[1], callback_data=f"browse_shop_{vendor[0]}")]
                    )
                reply_keyboard = [
                    buttons,
                    [
                        [InlineKeyboardButton(text="Next", callback_data="browse_vendors_next")],
                        [InlineKeyboardButton(text="Previous", callback_data="browse_vendors_previous")]
                    ]
                ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text="What do you feel like getting today?",
        reply_markup=markup,
    )



browse_vendor_handler = CallbackQueryHandler(callback=browse_shops_init, pattern="make_order", run_async=True)
browse_vendor_ext_handler = CallbackQueryHandler(callback=browse_vendors, pattern="browse_vendors_", run_async=True)