from keep_alive import keep_alive

# إبقاء البوت يعمل 24/7
keep_alive()

import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# إعداد السجلات
logging.basicConfig(level=logging.INFO)

# ضع هنا التوكن من BotFather
TELEGRAM_TOKEN = "8066239879:AAGURepbswUiGB210v931Zu95mBswhXfVVs"

# ضع هنا مفتاح OpenRouter الخاص بك
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

# رسالة ترحيب للمستخدم
WELCOME_MESSAGE = """
🤖 أهلاً بك!

أنا بوت ذكاء اصطناعي مبني باستخدام تقنية ChatGPT من OpenAI عبر OpenRouter.
🧠 أستطيع مساعدتك بالإجابة على أسئلتك أو مساعدتك في أي موضوع.

🛠️ تم التطوير بواسطة: عبدالرحمن جمال عبدالرب العطاس.
"""

# عند بدء المحادثة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

# عند إرسال صورة
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📷 ميزة تحليل الصور قيد التطوير، ترقبوا التحديثات القادمة!")

# عند إرسال نص
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.error(f"❌ خطأ في الاتصال بـ OpenRouter: {e}")
        reply = f"⚠️ حدث خطأ أثناء الاتصال بـ OpenRouter:\n{e}"

    await update.message.reply_text(reply)

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    print("🤖 البوت يعمل الآن...")
    app.run_polling()
