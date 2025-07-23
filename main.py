from keep_alive import keep_alive

# إبقاء البوت يعمل
keep_alive()

import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# إعداد السجلات
logging.basicConfig(level=logging.INFO)

# مفاتيح API
TELEGRAM_TOKEN = "8066239879:AAGURepbswUiGB210v931Zu95mBswhXfVVs"
OPENROUTER_API_KEY = "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"
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"  # <-- تغيير المسار الأساسي

# رسالة ترحيبية
WELCOME_MESSAGE = """
🤖 مرحباً بك!

أنا بوت ذكاء اصطناعي مبني باستخدام تقنية ChatGPT من شركة OpenAI عبر OpenRouter.
أستطيع مساعدتك في الإجابة على أسئلتك وطلبك للمساعدة.

🛠️ تم تطوير هذا البوت بواسطة: عبدالرحمن جمال عبدالرب العطاس.
"""

# عند بدء المحادثة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

# الرد على الصور
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📷 ميزة تحليل الصور قيد التطوير بواسطة عبدالرحمن العطاس، ترقبوا التحديثات القادمة.")

# الرد على النصوص باستخدام OpenRouter GPT
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",  # <-- صيغة OpenRouter
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"❌ خطأ في الاتصال بـ OpenRouter: {e}")
        reply = f"حدث خطأ أثناء الاتصال بـ OpenRouter:\n{e}"

    await update.message.reply_text(reply)

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    print("🤖 البوت يعمل الآن...")
    app.run_polling()
