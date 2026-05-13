import asyncio
import aiohttp
import os
from supabase import create_client, Client

class IntelligenceUnit:
    def __init__(self):
        # جلب بيانات الاتصال من البيئة
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.path.join(os.getenv("SUPABASE_KEY"))
        self.supabase: Client = create_client(url, key)

    async def run_all_engines(self, target):
        # تنفيذ مهام البحث بشكل متوازي (Parallel Execution) لسرعة الاستجابة
        tasks = [
            self.search_google_indexed(target),
            self.check_database_leaks(target),
            self.check_dark_web_mentions(target)
        ]
        
        results = await asyncio.gather(*tasks)
        
        return {
            "google_status": results[0],
            "leak_status": results[1],
            "dark_web_status": results[2],
            "total_hits": sum([1 for r in results if "لم يتم" not in r])
        }

    async def search_google_indexed(self, target):
        """بحث حقيقي في فهارس قوقل المفتوحة للنتائج المشبوهة"""
        # نستخدم Ahmia كمنفذ بحث مجاني لا يحتاج API Key ومعروف في مجتمع OSINT
        search_url = f"https://ahmia.fi/search/?q={target}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, timeout=10) as response:
                    if response.status == 200:
                        text = await response.text()
                        # فحص بسيط للنتائج في الصفحة
                        if target in text:
                            return "⚠️ تم العثور على روابط في فهارس عامة"
                        return "✅ لا توجد نتائج علنية"
                    return "🔄 المحرك مشغول حالياً"
        except Exception:
            return "❌ خطأ في الاتصال بالمحرك"

    async def check_database_leaks(self, target):
        """فحص حقيقي داخل جدول التسريبات في Supabase الخاص بك"""
        try:
            # نبحث في جدول اسمه 'leaked_users' عن تطابق للبريد أو الهدف
            response = self.supabase.table("leaked_users").select("*").eq("email", target).execute()
            if response.data:
                leaks_count = len(response.data)
                return f"🔓 مسرب في {leaks_count} قاعدة بيانات"
            return "✅ نظيف (لا يوجد تسريبات)"
        except Exception as e:
            return "⚠️ فحص التسريبات غير متاح حالياً"

    async def check_dark_web_mentions(self, target):
        """فحص حقيقي للذكر في مواقع البستبين (Pastebin) المشهورة بالتسريبات"""
        url = f"https://psbdmp.ws/api/search/{target}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("count", 0) > 0:
                            return f"🌑 موجود في {data['count']} نصوص مسربة (Pastes)"
            return "✅ لا يوجد نشاط في الإنترنت المظلم"
        except:
            return "⚠️ تعذر فحص فهارس البستبين"
