#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║        FX SNIPER BOT — Reminder Analisis Forex Otomatis         ║
║        Kirim notifikasi ke Telegram setiap sesi trading          ║
╚══════════════════════════════════════════════════════════════════╝

SETUP (jalankan sekali):
  pip install python-telegram-bot schedule pytz

CARA PAKAI:
  1. Buat bot Telegram: chat ke @BotFather → /newbot
  2. Isi BOT_TOKEN di bawah
  3. Isi CHAT_ID (dapatkan dari @userinfobot)
  4. python fx_sniper_bot.py
"""

import os
import schedule
import time
import logging
from datetime import datetime
import pytz

# ──────────────────────────────────────────
#  KONFIGURASI — ISI DI SINI
# ──────────────────────────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")   # diisi via Railway Environment Variables
CHAT_ID   = os.environ.get("CHAT_ID", "")      # diisi via Railway Environment Variables

WIB = pytz.timezone("Asia/Jakarta")

# ──────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
log = logging.getLogger("FXSniperBot")

# ──────────────────────────────────────────
#  PAIRS PER SESSION
# ──────────────────────────────────────────
PAIRS = {
    "asian":  ["XAUUSD", "USDJPY", "AUDJPY", "CADJPY", "NZDUSD", "NZDCAD", "NZDCHF", "AUDCHF"],
    "london": ["XAUUSD", "EURUSD", "GBPUSD", "GBPAUD", "EURAUD", "EURGBP", "GBPJPY", "EURCAD"],
    "ny":     ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "USDCAD", "CADJPY", "NZDUSD", "USDCHF"],
}

# ──────────────────────────────────────────
#  FORMAT PESAN
# ──────────────────────────────────────────
def format_pairs(pairs: list) -> str:
    return "\n".join(f"  ├ `{p}`" for p in pairs[:-1]) + f"\n  └ `{pairs[-1]}`"

def msg_asian() -> str:
    now = datetime.now(WIB)
    pairs_str = format_pairs(PAIRS["asian"])
    return f"""🌏 *ASIAN SESSION DIBUKA*
━━━━━━━━━━━━━━━━━━━━━━
🕕 Waktu: *{now.strftime('%H:%M WIB')}* | {now.strftime('%d %b %Y')}
⏰ Sesi: 06:00 – 14:00 WIB

📋 *PAIRS YANG PERLU DIANALISIS:*
{pairs_str}

*📊 LANGKAH ANALISIS (Price Action MTF):*
1️⃣ *H4* — Identifikasi trend & S/R mayor
2️⃣ *H1* — Cari BoS (Break of Structure)
3️⃣ *M30* — Entry presisi + konfirmasi candle

⚖️ *Target R:R = 1:3*
  • SL di bawah/atas level S/R
  • TP3 = 3× jarak SL dari entry

🎯 *BIAS CHECKLIST SEBELUM ENTRY:*
  ☐ H4 trend konfirmasi
  ☐ H1 pullback ke S/R
  ☐ M30 pin bar / engulfing
  ☐ R:R ≥ 1:3 ✅

⚡ _Disiplin adalah edge terbesar trader!_
"""

def msg_london() -> str:
    now = datetime.now(WIB)
    pairs_str = format_pairs(PAIRS["london"])
    return f"""🇬🇧 *LONDON SESSION DIBUKA*
━━━━━━━━━━━━━━━━━━━━━━
🕕 Waktu: *{now.strftime('%H:%M WIB')}* | {now.strftime('%d %b %Y')}
⏰ Sesi: 14:00 – 21:00 WIB

📋 *PAIRS YANG PERLU DIANALISIS:*
{pairs_str}

*📊 POLA UTAMA LONDON SESSION:*
  • *London Breakout* — break dari range Asian
  • *Fakeout/Liquidity Sweep* — di atas/bawah high/low Asian
  • *Reversal* — setelah sweep, cari konfirmasi di H1-M30

⚖️ *Target R:R = 1:3*
  • Perhatikan liquidity grab sebelum entry!
  • Hindari entry saat news EUR/GBP High Impact

🔴 *WASPADAI:* London session = volatilitas tinggi
Tunggu konfirmasi, jangan FOMO!

⚡ _Sabar menunggu setup = profit konsisten_
"""

def msg_ny() -> str:
    now = datetime.now(WIB)
    pairs_str = format_pairs(PAIRS["ny"])
    return f"""🗽 *NEW YORK SESSION DIBUKA*
━━━━━━━━━━━━━━━━━━━━━━
🕕 Waktu: *{now.strftime('%H:%M WIB')}* | {now.strftime('%d %b %Y')}
⏰ Sesi: 19:00 – 22:00 WIB

📋 *PAIRS YANG PERLU DIANALISIS:*
{pairs_str}

*📊 POLA UTAMA NY SESSION:*
  • *NY Continuation* — lanjutan arah London
  • *NY Reversal* — jika London sudah extended
  • *Overlap 19:00-21:00* — volatilitas tertinggi hari ini!

⚖️ *Target R:R = 1:3*
  • Ini sesi terakhir — jangan overtrade!
  • Cek apakah ada setup yang belum kena TP

⚠️ *PENUTUPAN POSISI:*
  Pertimbangkan close posisi sebelum 22:00 WIB
  untuk hindari overnight risk

⚡ _Quality over quantity — 1 trade bagus > 5 trade sembarangan_
"""

def msg_end_of_day() -> str:
    now = datetime.now(WIB)
    return f"""🌙 *SESI TRADING BERAKHIR*
━━━━━━━━━━━━━━━━━━━━━━
🕕 {now.strftime('%H:%M WIB')} | {now.strftime('%d %b %Y')}

*📝 REVIEW HARIAN — isi jurnal trading Anda:*

  ✅ Berapa trade yang diambil hari ini?
  📊 Win/Loss ratio hari ini?
  💡 Apa yang bisa diperbaiki?
  🧠 Apakah emosi trading terkontrol?
  🎯 Setup terbaik hari ini di pair apa?

*⚠️ REMINDER:*
  • Close semua posisi yang tidak diperlukan
  • Catat semua trade di jurnal
  • Istirahat — trading besok dengan fresh mind

_"The goal of a successful trader is to make the best trades. Money is secondary."_ — Alexander Elder

🌙 _Selamat beristirahat!_
"""

def msg_weekly_prep() -> str:
    now = datetime.now(WIB)
    return f"""📅 *PERSIAPAN MINGGU BARU*
━━━━━━━━━━━━━━━━━━━━━━
🕕 {now.strftime('%H:%M WIB')} | {now.strftime('%d %b %Y')}

*🗓 TRADING WEEK DIMULAI BESOK (SENIN)*

*📌 CHECKLIST PERSIAPAN:*
  ☐ Cek kalender ekonomi minggu ini
  ☐ Review jurnal minggu lalu
  ☐ Identifikasi key level S/R di chart
  ☐ Set alert harga di platform trading
  ☐ Tentukan max loss mingguan
  ☐ Update plan trading minggu ini

*🌐 CARI BERITA HIGH IMPACT:*
  → USD, EUR, GBP, JPY, AUD, NZD, CAD

*💪 MINDSET MINGGU INI:*
  • Follow the plan
  • Risk management first
  • Konsisten > Profit cepat

_Ready to trade smart this week!_ 🚀
"""

# ──────────────────────────────────────────
#  KIRIM PESAN
# ──────────────────────────────────────────
def send_message(text: str):
    """Kirim pesan ke Telegram"""
    try:
        import urllib.request
        import urllib.parse
        import json

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id":    CHAT_ID,
            "text":       text,
            "parse_mode": "Markdown"
        }).encode()

        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get("ok"):
                log.info(f"✅ Pesan terkirim: {text[:40]}...")
            else:
                log.error(f"❌ Gagal: {result}")
    except Exception as e:
        log.error(f"❌ Error kirim pesan: {e}")

# ──────────────────────────────────────────
#  SCHEDULE JOBS
# ──────────────────────────────────────────
def setup_schedule():
    # ── SENIN – JUMAT ──
    # Asian Session (06:00 WIB)
    schedule.every().monday.at("06:00").do(send_message, msg_asian())
    schedule.every().tuesday.at("06:00").do(send_message, msg_asian())
    schedule.every().wednesday.at("06:00").do(send_message, msg_asian())
    schedule.every().thursday.at("06:00").do(send_message, msg_asian())
    schedule.every().friday.at("06:00").do(send_message, msg_asian())

    # London Session (14:00 WIB)
    schedule.every().monday.at("14:00").do(send_message, msg_london())
    schedule.every().tuesday.at("14:00").do(send_message, msg_london())
    schedule.every().wednesday.at("14:00").do(send_message, msg_london())
    schedule.every().thursday.at("14:00").do(send_message, msg_london())
    schedule.every().friday.at("14:00").do(send_message, msg_london())

    # New York Session (19:00 WIB)
    schedule.every().monday.at("19:00").do(send_message, msg_ny())
    schedule.every().tuesday.at("19:00").do(send_message, msg_ny())
    schedule.every().wednesday.at("19:00").do(send_message, msg_ny())
    schedule.every().thursday.at("19:00").do(send_message, msg_ny())
    schedule.every().friday.at("19:00").do(send_message, msg_ny())

    # End of Day (22:00 WIB)
    schedule.every().monday.at("22:00").do(send_message, msg_end_of_day())
    schedule.every().tuesday.at("22:00").do(send_message, msg_end_of_day())
    schedule.every().wednesday.at("22:00").do(send_message, msg_end_of_day())
    schedule.every().thursday.at("22:00").do(send_message, msg_end_of_day())
    schedule.every().friday.at("22:00").do(send_message, msg_end_of_day())

    # Weekly Prep (Minggu 20:00 WIB)
    schedule.every().sunday.at("20:00").do(send_message, msg_weekly_prep())

    log.info("✅ Schedule berhasil diatur!")
    log.info("📋 Jadwal aktif:")
    log.info("  • Senin-Jumat 06:00 → Asian Session Alert")
    log.info("  • Senin-Jumat 14:00 → London Session Alert")
    log.info("  • Senin-Jumat 19:00 → New York Session Alert")
    log.info("  • Senin-Jumat 22:00 → End of Day Review")
    log.info("  • Minggu 20:00     → Weekly Prep")

# ──────────────────────────────────────────
#  TEST MODE
# ──────────────────────────────────────────
def test_bot():
    """Test kirim pesan - jalankan sebelum setup schedule"""
    log.info("🧪 Testing bot...")
    send_message("🤖 *FX Sniper Bot AKTIF!*\n\nBot trading reminder Anda sudah berjalan.\nAnda akan menerima notifikasi di:\n• 06:00 WIB — Asian Session\n• 14:00 WIB — London Session\n• 19:00 WIB — New York Session\n• 22:00 WIB — End of Day Review\n\n_Selamat trading! 🚀_")

# ──────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════╗
║        FX SNIPER BOT — v1.0             ║
╚══════════════════════════════════════════╝
    """)

    if BOT_TOKEN == "XXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX":
        print("⚠️  PERINGATAN: Isi BOT_TOKEN dan CHAT_ID terlebih dahulu!")
        print("   1. Chat @BotFather di Telegram → /newbot")
        print("   2. Salin token ke BOT_TOKEN di atas")
        print("   3. Chat @userinfobot → salin id ke CHAT_ID")
        exit(1)

    # Test dulu
    test_bot()

    # Setup jadwal
    setup_schedule()

    # Jalankan loop
    log.info("🚀 Bot berjalan... (Ctrl+C untuk berhenti)")
    while True:
        schedule.run_pending()
        time.sleep(30)
