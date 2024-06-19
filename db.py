import mysql.connector
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler

# Database credentials
DB_HOST = http://sql12.freesqldatabase.com/
DB_NAME = sql12714230
DB_USER = sql12714230
DB_PASSWORD = sT5Ll7ZqBb

# Telegram bot token
BOT_TOKEN = 7023209368:AAETqTUkY-cGGB_wZ_P7unIC89Awen0Elqw

# Create Flask app
app = Flask(__name__)

# Initialize the bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# Connect to the database
def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Command handler for /start
def start(update: Update, context):
    chat_id = update.message.chat_id

    # Connect to the database
    db = connect_db()
    cursor = db.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE chat_id = %s", (chat_id,))
    user = cursor.fetchone()

    if user:
        update.message.reply_text("You are already subscribed.")
    else:
        cursor.execute("INSERT INTO users (chat_id) VALUES (%s)", (chat_id,))
        db.commit()
        update.message.reply_text("Thanks for subscribing me.")

    cursor.close()
    db.close()

# Add command handler to dispatcher
dispatcher.add_handler(CommandHandler("start", start))

# Set webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    # Set the webhook URL
    webhook_url = 'https://your_domain_or_ngrok_url/7023209368:AAETqTUkY-cGGB_wZ_P7unIC89Awen0Elqw'
    bot.set_webhook(webhook_url)
    
    # Run the Flask app
    app.run(port=8443)
