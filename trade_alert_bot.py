import os
import time
import schedule
from nsepython import nse_eq
from telegram import Bot

# Telegram setup
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=BOT_TOKEN)

# Stocks to monitor
stocks = ["BHEL", "CESC", "IRFC", "RVNL", "NHPC", "PNB", "SJVN", "MGL", "JPPOWER", "RECLTD"]

# Store previous high prices for breakout logic
prev_highs = {}

def check_for_breakouts():
    messages = []
    for symbol in stocks:
        try:
            data = nse_eq(symbol)
            ltp = float(data["priceInfo"]["lastPrice"])
            high = float(data["priceInfo"]["intraDayHighLow"]["max"])
            low = float(data["priceInfo"]["intraDayHighLow"]["min"])
            vol = int(data["securityWiseDP"]["quantityTraded"])
            
            # Check for breakout
            if symbol in prev_highs:
                if ltp > prev_highs[symbol] * 1.005 and vol > 500000:
                    messages.append(f"📈 Breakout Alert: {symbol}\nLTP: ₹{ltp} > Prev High: ₹{prev_highs[symbol]}\nVolume: {vol}")
            prev_highs[symbol] = max(prev_highs.get(symbol, 0), high)
        except Exception as e:
            print(f"Error checking {symbol}: {e}")

    # Send alerts
    for msg in messages:
        bot.send_message(chat_id=CHAT_ID, text=msg)

# Schedule check every 2 minutes
schedule.every(2).minutes.do(check_for_breakouts)

print("Bot started...")
while True:
    schedule.run_pending()
    time.sleep(1)
