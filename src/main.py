import logging
import asyncio
import os
import sys

# ضمان الوصول للمحركات في Render
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# استيراد المحركات
try:
    from src.engines.intelligence_unit import IntelligenceUnit
except ImportError:
    from engines.intelligence_unit import IntelligenceUnit

load_dotenv()

# الإصلاح هنا: نقرأ المتغير TELEGRAM_TOKEN من إعدادات Render أو ملف .env
API_TOKEN = os.getenv("TELEGRAM_TOKEN")

# حماية إضافية: التأكد من وجود التوكن قبل البدء
if not API_TOKEN:
    raise ValueError("❌ خطأ: لم يتم العثور على TELEGRAM_TOKEN في الإعدادات!")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
intel_unit = IntelligenceUnit()

@dp.message(Command("start"))
async def start_handler(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛠️ فحص متقدم", callback_data="deep_scan")],
        [InlineKeyboardButton(text="🌐 استخبارات الويب", callback_data="web_intel")]
    ])
    await message.answer(
        "⚡ **نظام الرصد والتحليل الجبار مفعّل**\n"
        "أدخل 'الهدف' لبدء التقصي الشامل عبر الفهارس العالمية.",
        reply_markup=kb, parse_mode="Markdown"
    )

@dp.message()
async def process_intel(message: Message):
    target = message.text
    status = await message.answer(f"🚀 **بدء عملية الاستطلاع للهدف:** `{target}`...")
    
    try:
        results = await intel_unit.run_all_engines(target)
        report = (
            f"📊 **التقرير الاستخباراتي لـ** `{target}`\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔎 **قوقل:** {results['google_status']}\n"
            f"🌑 **الإنترنت المظلم:** {results['dark_web_status']}\n"
            f"🔓 **التسريبات:** {results['leak_status']}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📝 تم الربط بنجاح."
        )
        await status.edit_text(report, parse_mode="Markdown")
    except Exception as e:
        await status.edit_text(f"❌ حدث خطأ أثناء المعالجة: {str(e)}")

async def main():
    # حذف أي عمليات معلقة قديمة لتجنب التعارض
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
