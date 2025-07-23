import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# إعداد السجلات
logging.basicConfig(level=logging.INFO)

# مفاتيح API مباشرة (غير آمن ولكن حسب طلبك)
TELEGRAM_TOKEN = "8066239879:AAGURepbswUiGB210v931Zu95mBswhXfVVs"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# رسالة ترحيبية
WELCOME_MESSAGE = """
🤖 مرحباً بك!

أنا بوت ذكاء اصطناعي مبني باستخدام تقنية ChatGPT من شركة OpenAI.
أستطيع مساعدتك في الإجابة على أسئلتك وطلبك للمساعدة.

🛠️ تم تطوير هذا البوت بواسطة: عبدالرحمن جمال عبدالرب العطاس.
"""

# عند بدء المحادثة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

# الرد على الصور
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📷 ميزة تحليل الصور قيد التطوير بواسطة عبدالرحمن العطاس، ترقبوا التحديثات القادمة.")

# الرد على النصوص باستخدام GPT
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = "حدث خطأ أثناء الاتصال بـ OpenAI."

    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    print("🤖 البوت يعمل الآن...")
    app.run_polling()
