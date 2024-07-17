import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import random
import pymongo
from threading import Thread
from datetime import datetime, timedelta
import re

TOKEN = '7360511985:AAEPPooNjhzY6KKuaMA_QloZcX9yn6bx5Ms'
MONGO_URI = "mongodb+srv://omnikingzeno2000:PrinceJindal@cluster0.a35bmwi.mongodb.net"

client = pymongo.MongoClient(MONGO_URI)
db = client["BikesDB"]
users_collection = db["users"]
bikes_collection = db["bikes"]

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

OWNER_ID = 7387719195

bikes = {
    "Hayabusa": {
        "price": 20000,
        "image": "https://www.suzukicycles.com/-/media/project/suzuki-cycles/images/on-road/2023/hayabusa/gallery/2023-hayabusa-abs-gallery-image.jpg",
        "details": "The Suzuki Hayabusa is a sport motorcycle known for its speed and power. Engine: 1340cc. Top speed: 312 km/h."
    },
    "Yamaha R1": {
        "price": 17000,
        "image": "https://www.yamahamotorsports.com/assets/img/2019/mc/c2019/YZF-R1c3_014a6.jpg",
        "details": "The Yamaha R1 is a sport bike known for its performance and agility on the track. Engine: 998cc. Top speed: 299 km/h."
    },
    "Kawasaki Ninja H2": {
        "price": 30000,
        "image": "https://www.motorbeam.com/wp-content/uploads/2015-Kawasaki-Ninja-H2R-Wallpaper.jpg",
        "details": "The Kawasaki Ninja H2 is a 'supercharged supersport' class motorcycle. Engine: 998cc. Top speed: 400 km/h."
    },
    "Ducati Panigale V4": {
        "price": 25000,
        "image": "https://www.ducati.com/ww/en/bikes/panigale/panigale-v4",
        "details": "The Ducati Panigale V4 is an Italian sports bike known for its speed and design. Engine: 1103cc. Top speed: 306 km/h."
    },
    "BMW S1000RR": {
        "price": 18000,
        "image": "https://www.bmw-motorrad.co.uk/content/dam/bmwmotorradnsc/marketGB/bikes/sport-bikes/s1000rr/2022/06-2021/gallery/S-1000-RR-Gallery-1.jpg",
        "details": "The BMW S1000RR is a powerful sports bike with advanced technology and performance. Engine: 999cc. Top speed: 299 km/h."
    },
    "Suzuki GSX-R1000": {
        "price": 16000,
        "image": "https://www.suzukicycles.com/-/media/project/suzuki-cycles/images/on-road/2023/gsx-r1000/gallery/2023-gsx-r1000-gallery-image.jpg",
        "details": "The Suzuki GSX-R1000 is a top-performing sports bike with a reputation for speed. Engine: 999cc. Top speed: 299 km/h."
    },
    "Honda CBR1000RR": {
        "price": 19000,
        "image": "https://powersports.honda.com/street/supersport/cbr1000rr/gallery/2021/gallery-01.jpg",
        "details": "The Honda CBR1000RR is a high-performance sports bike known for its agility and speed. Engine: 999cc. Top speed: 299 km/h."
    },
    "Aprilia RSV4": {
        "price": 22000,
        "image": "https://www.aprilia.com/on-the-road/road/RSV4/RSV4-1100/",
        "details": "The Aprilia RSV4 is an Italian sports bike known for its performance and handling. Engine: 1099cc. Top speed: 300 km/h."
    },
    "MV Agusta F4": {
        "price": 26000,
        "image": "https://www.mvagusta.com/media/73382/f4-my2017_gallery-08.jpg",
        "details": "The MV Agusta F4 is an Italian sports bike with a combination of speed and design. Engine: 998cc. Top speed: 305 km/h."
    },
    "KTM 1290 Super Duke R": {
        "price": 19000,
        "image": "https://www.ktm.com/globalassets/motorcycles/naked/1290-super-duke-r/gallery/2023/ktm-1290-super-duke-r-2023.jpg",
        "details": "The KTM 1290 Super Duke R is a powerful and aggressive naked bike. Engine: 1301cc. Top speed: 289 km/h."
    }
}

last_work_time = {} 

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type != "private":
        bot.reply_to(message, "<b>Use This Command In Bot PM</b>")
        return
    user_id = message.from_user.id
    user = users_collection.find_one({"_id": user_id})
    if user is None:
        users_collection.insert_one({"_id": user_id, "balance": 100000, "bikes": [], "last_work_time": None})
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("📢 Updates Channel", url="https://t.me/BikeXUpdates"),
        InlineKeyboardButton("📞 Contact Owner", url="https://t.me/JustGarv"),
        InlineKeyboardButton("➕ Add me to Group", url="t.me/BikeXCatcherRobot?startgroup=new")
    )
    bot.send_photo(
        message.chat.id,
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSG9gG0c6DjygqcuZ37eiCLzgg0tZpIOL-deA&s',
        caption="🌟 <b>Welcome to BikeBot!</b> 🌟 🚴‍♂️\n\nI'm here to assist you with various commands and features.\n\nFeel free to explore the bot and use the inline buttons below to navigate.",
        reply_markup=keyboard
    )

@bot.message_handler(commands=['wallet'])
def wallet(message):
    user_id = message.from_user.id
    user = users_collection.find_one({"_id": user_id})
    if user is not None:
        if user_id == OWNER_ID:
            bot.send_message(message.chat.id, "💰 You have <b>INFINITE</b> money! 🤑")
        else:
            bot.send_message(message.chat.id, f"💰 <b>Your Money:</b> ${user['balance']:,}")
    else:
        bot.send_message(message.chat.id, "🚫 You are not registered. Please use /start to start.")

@bot.message_handler(commands=['mybikes'])
def mybikes(message):
    user_id = message.from_user.id
    user = users_collection.find_one({"_id": user_id})
    if user:
        if user_id == OWNER_ID:
            bike_list = list(bikes.keys())
            response = "🏍 <b>All Bikes in the Store:</b>\n" + "\n".join([f"• {bike}" for bike in bike_list])
        elif 'bikes' in user:
            bike_list = user['bikes']
            if bike_list:
                response = "🏍 <b>Your Bikes:</b>\n" + "\n".join([f"• {bike}" for bike in bike_list])
            else:
                response = "🚫 <b>You don't have any bikes yet.</b>"
        else:
            response = "🚫 <b>You are not registered. Please use /start to start.</b>"
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "<b>🚫 You are not registered. Please use /start to start.</b>")

@bot.message_handler(commands=['show'])
def show_bike(message):
    bike_name = message.text.split(maxsplit=1)[1]
    bike = bikes.get(bike_name)
    if bike:
        bot.send_photo(
            message.chat.id,
            bike['image'],
            caption=f"🏍 <b>{bike_name}</b>\n\n{bike['details']}"
        )
    else:
        bot.send_message(message.chat.id, "🚫 <b>You don't have this bike.</b>")

@bot.message_handler(commands=['store'])
def store(message):
    bot.send_photo(
        message.chat.id,
        "https://t4.ftcdn.net/jpg/05/67/03/25/360_F_567032519_HWWeha72w4FlDHtpJCDOP82gCMjubrN0.jpg",
        caption=''''<b>Welcome to the Bike Store!🏍️\n\nHere you can purchase top-of-the-line bikes.
        
        1.<code>Yamaha R1</code>
        2.<code>Hayabusa</code>
        3.<code>Kawasaki Ninja H2</code>
        4.<code>Ducati Panigale V4</code>
        5.<code>BMW S1000RR</code>
        6.<code>Suzuki GSX-R1000</code>
        7.<code>Honda CBR1000RR</code>
        8.<code>Aprilia RSV4</code>
        9.<code>MV Agusta F4</code>
        1o,<code>KTM 1290 Super Duke R</code>

    You Can Buy These Bikes by /buy (bike Name)</b>''',
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def buy_bike(call):
    user_id = call.from_user.id
    bike_name = call.data.split("_")[1]
    bike = bikes.get(bike_name)

    if bike:
        user = users_collection.find_one({"_id": user_id})
        if user:
            if user['balance'] >= bike["price"]:
                users_collection.update_one({"_id": user_id}, {"$inc": {"balance": -bike["price"]}, "$push": {"bikes": bike_name}})
                bot.edit_message_text(
                    call.message.chat.id,
                    call.message.message_id,
                    text=f"<b>🎉 <b>Congratulations!</b> You have purchased the <b>{bike_name}</b>!\n\n</b>"
                         f"<b>💰 Your remaining balance: ${user['balance'] - bike['price']:,}\n\n</b>"
                         f"<b>You can view your bikes using <code>/mybikes</code></b>",
                    parse_mode="HTML"
                )
            else:
                bot.edit_message_text(
                    call.message.chat.id,
                    call.message.message_id,
                    text=f"<b>🚫 Insufficient funds! You need ${bike['price']:,} to buy this bike.\n\n</b>"
                         f"<b>Work hard to earn more money using <code>/work</code> command.</b>"
                )
        else:
            bot.edit_message_text(
                call.message.chat.id,
                call.message.message_id,
                text="<b>🚫 You are not registered. Please use /start to start.</b>"
            )
    else:
        bot.edit_message_text(
            call.message.chat.id,
            call.message.message_id,
            text="<b>🚫 Invalid bike selection.</b>"
        )

@bot.message_handler(commands=['buy'])
def buy_bike_command(message):
    user_id = message.from_user.id
    bike_name = message.text.split(maxsplit=1)[1]
    bike = bikes.get(bike_name)

    if bike:
        if user_id == OWNER_ID:
            bot.reply_to(message, "<b>👑 Owner OP! You Have All Bikes!</b>", parse_mode="HTML")
            return
        user = users_collection.find_one({"_id": user_id})
        if user:
            if user['balance'] >= bike["price"]:
                users_collection.update_one({"_id": user_id}, {"$inc": {"balance": -bike["price"]}, "$push": {"bikes": bike_name}})
                bot.reply_to(
                    message,
                    f"<b>🎉 Congratulations! You have purchased the {bike_name}!\n\n</b>"
                    f"<b>💰 Your remaining balance: ${user['balance'] - bike['price']:,}\n\n</b>"
                    f"<b>You can view your bikes using <code>/mybikes</code></b>",
                    parse_mode="HTML"
                )
            else:
                bot.reply_to(
                    message,
                    f"<b>🚫 Insufficient funds! You need ${bike['price']:,} to buy this bike.\n\n</b>"
                    f"<b>Work hard to earn more money using <code>/work</code> command.</b>",
                )
        else:
            bot.reply_to(message, "<b>🚫 You are not registered. Please use /start to start.</b>")
    else:
        bot.reply_to(message, "<b>🚫 Invalid bike selection.</b>")

@bot.message_handler(commands=['work'])
def work(message):
    user_id = message.from_user.id
    user = users_collection.find_one({"_id": user_id})
    if user:
        last_work_time = user.get("last_work_time")
        if last_work_time:
            last_work_time = datetime.fromisoformat(last_work_time)
            if (datetime.now() - last_work_time).total_seconds() < 86400:
                bot.reply_to(message, "<b>You've already worked today! Come back tomorrow.</b>")
                return

        if user_id == OWNER_ID:
            bot.reply_to(message, "<b>👑 You are the owner! 👑</b>")
            return

        users_collection.update_one({"_id": user_id}, {"$set": {"last_work_time": datetime.now().isoformat()}})
        users_collection.update_one({"_id": user_id}, {"$inc": {"balance": 1000}})
        bot.reply_to(message, f"<b>💪 You worked hard and earned $1,000! 💪\n💰 Your new balance: ${user['balance'] + 1000:,}</b>", parse_mode="HTML")
        
        last_work_time[user_id] = datetime.now()

    else:
        bot.reply_to(message, "<b>🚫 You are not registered. Please use /start to start.</b>")

@bot.message_handler(commands=['event'])
def event(message):
    try:
        user_id = message.from_user.id
        user = users_collection.find_one({"_id": user_id})
        if not user:
            bot.reply_to(message, "<b>🚫 You are not registered. Please use /start to start.</b>")
            return

        if user.get('event_claimed'):
            bot.reply_to(message, "<b>🚫 You have already claimed the event reward.</b>")
            return

        users_collection.update_one({"_id": user_id}, {"$inc": {"balance": 100000}, "$set": {"event_claimed": True}})
        bot.reply_to(message, "<b>🎉 You have claimed $100,000 from the event! 🎉</b>")
    except Exception as e:
        bot.reply_to(message, f"<b>🚫 An error occurred: {e}</b>")
        print(f"Error in /event command: {e}")

@bot.message_handler(commands=['race'])
def race(message):
    try:
        user_id = message.from_user.id
        user = users_collection.find_one({"_id": user_id})
        if not user:
            bot.reply_to(message, "<b>🚫 You are not registered. Please use /start to start.</b>")
            return

        if not user.get('bikes'):
            bot.reply_to(message, "<b>🚫 You don't have any bikes to race with.</b>")
            return

        last_race_time = user.get('last_race_time')
        if last_race_time:
            last_race_time = datetime.fromisoformat(last_race_time)
            if (datetime.now() - last_race_time).total_seconds() < 86400:
                bot.reply_to(message, "<b>🚫 You have already raced today. Come back tomorrow.</b>")
                return

        keyboard = InlineKeyboardMarkup()
        for bike in user['bikes']:
            keyboard.add(InlineKeyboardButton(bike, callback_data=f'race_{bike}'))

        bot.send_message(message.chat.id, "<b>🏁 Choose your bike for the race:</b>", reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(message, f"<b>🚫 An error occurred: {e}</b>")
        print(f"<b>Error in /race command: {e}</b>")

@bot.callback_query_handler(func=lambda call: call.data.startswith('race_'))
def handle_race(call):
    try:
        user_id = call.from_user.id
        bike_name = call.data.split("_")[1]

        bike = bikes.get(bike_name)
        if not bike:
            bot.answer_callback_query(call.id, "<b>🚫 Invalid bike selection.</b>")
            return

        chances = {
            "Hayabusa": 0.5,
            "Yamaha R1": 0.3,
            "Kawasaki Ninja H2": 0.7
        }

        result = random.random() < chances.get(bike_name, 0)
        if result:
            users_collection.update_one({"_id": user_id}, {"$inc": {"balance": 10000}})
            result_message = "<b>🎉 You won the race and earned $10,000! 🎉</b>"
        else:
            result_message = "<b>😢 You lost the race. Better luck next time.</b>"

        users_collection.update_one({"_id": user_id}, {"$set": {"last_race_time": datetime.now().isoformat()}})
        bot.edit_message_text(result_message, call.message.chat.id, call.message.message_id)
    except Exception as e:
        bot.reply_to(call.message, f"<b>🚫 An error occurred: {e}</b>")
        print(f"Error in handle_race callback: {e}")


@bot.message_handler(commands=['give'])
def handle_give_command(message):
    try:
        # Extract recipient_id and amount using regular expressions
        match = re.match(r'/give (\d+) (\d+)', message.text) 
        if not match:
            bot.reply_to(message, "Invalid command format. Use /give <recipient_id> <amount>.")
            return

        recipient_id = int(match.group(1))
        amount = int(match.group(2))

        user_id = message.from_user.id
        user = users_collection.find_one({"_id": user_id})
        if not user:
            bot.reply_to(message, "You are not registered. Please use /start to start.")
            return

        recipient = users_collection.find_one({"_id": recipient_id})
        if not recipient:
            bot.reply_to(message, "Recipient not found.")
            return

        if user_id != OWNER_ID and amount > user['balance']:
            bot.reply_to(message, "You don't have enough money.")
            return

        if user_id != OWNER_ID:
            users_collection.update_one({"_id": user_id}, {"$inc": {"balance": -amount}})
        users_collection.update_one({"_id": recipient_id}, {"$inc": {"balance": amount}})

        bot.reply_to(message, f"<b>You have given ${amount} to {recipient_id}!")
        bot.send_message(recipient_id, f"{message.from_user.username} has given you ${amount}!")

    except ValueError:
        bot.reply_to(message, "Invalid amount. Please enter a valid number.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")
        print(f"Error in /give command: {e}")

bot.polling()
