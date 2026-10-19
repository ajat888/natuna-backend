from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import json

# Inisialisasi aplikasi FastAPI
app = FastAPI(title="Natuna POS AI Backend")

# Inisialisasi Groq Client
# ⚠️ GANTI DENGAN API KEY GROQ KAMU
API_KEY = "gsk_ISI_API_KEY_KAMU_DISINI"
client = Groq(api_key=API_KEY)

# ==========================================
# 1. Format data dari Flutter
# ==========================================
class PenjualanData(BaseModel):
    tanggal: str
    omzet: int
    pengeluaran: int
    menu_terlaris: str

# ==========================================
# 2. Endpoint AI
# ==========================================
@app.post("/api/laporan-ai")
def buat_laporan(data: PenjualanData):
    kas_bersih = data.omzet - data.pengeluaran
    
    # Menyusun Prompt untuk AI
    prompt = f"""
    Kamu adalah konsultan bisnis kafe. Buatkan laporan evaluasi harian yang santai tapi tajam untuk owner kafe.
    Data hari ini:
    - Tanggal: {data.tanggal}
    - Omzet: Rp {data.omzet:,}
    - Pengeluaran: Rp {data.pengeluaran:,}
    - Kas Bersih: Rp {kas_bersih:,}
    - Menu Terlaris: {data.menu_terlaris}
    
    Berikan 1 paragraf kesimpulan dan 1 saran aksi konkret untuk besok. Jangan pakai bahasa yang terlalu formal.
    """

    try:
        # Memanggil Groq API (Model LLaMA 3)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Kamu adalah asisten AI untuk aplikasi kasir NATUNA POS."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192", # Model gratis & cepat dari Groq
            temperature=0.7,
            max_tokens=300,
        )
        
        hasil_ai = chat_completion.choices[0].message.content
        
        return {
            "status": "success",
            "data": {
                "kas_bersih": kas_bersih,
                "laporan_ai": hasil_ai
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
