import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# استيراد المحركات المتقدمة
from engines.intelligence_unit import IntelligenceUnit

load_dotenv()
API_TOKEN = os.getenv("8713533131:AAEHsLROo10xBo_oG7C-6BbtDDvN3x94u7A")

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
        "أدخل 'الهدف' (بريد، يوزر، نطاق، أو اسم) لبدء التقصي الشامل عبر الفهارس العالمية.",
        reply_markup=kb, parse_mode="Markdown"
    )

@dp.message()
async def process_intel(message: Message):
    target = message.text
    status = await message.answer(f"🚀 **بدء عملية الاختراق المعلوماتي للهدف:** `{target}`...")
    
    # تنفيذ البحث المتوازي في قوقل، أغميا (Dark Web)، وقواعد البيانات المسربة
    results = await intel_unit.run_all_engines(target)
    
    report = (
        f"📊 **التقرير الاستخباراتي النهائي لـ** `{target}`\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🔎 **نتائج قوقل المتقدمة:** {results['google_status']}\n"
        f"🌑 **فهرس الإنترنت المظلم:** {results['dark_web_status']}\n"
        f"🔓 **تسريبات قواعد البيانات:** {results['leak_status']}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📝 **الملخص:** تم العثور على {results['total_hits']} نقطة ترابط."
    )
    
    await status.edit_text(report, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
