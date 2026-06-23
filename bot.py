from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, ContextTypes, filters, CommandHandler, CallbackQueryHandler
from datetime import datetime
import os
from weasyprint import HTML
from jinja2 import Template

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    try:
        with open("token.txt", "r", encoding="utf-8") as f:
            TOKEN = f.read().strip()
        print("✅ Токен загружен из файла token.txt")
    except FileNotFoundError:
        raise ValueError("❌ Токен не найден!")

CONTRACT_TYPES = {
    "exclusive": {
        "name": "Exclusive Rights",
        "description": "Эксклюзивные права на бит"
    },
    "rent": {
        "name": "Unlimited Lease",
        "description": "Аренда бита (Unlimited Lease)"
    }
}

# Шаблон договора в HTML (полностью стилизованный)
def get_contract_html(data, contract_type):
    publishing = int(data["publishing"])
    producer_publishing = 100 - publishing
    
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Contract</title>
        <style>
            body {
                font-family: 'Times New Roman', Times, serif;
                font-size: 12pt;
                margin: 40px;
                line-height: 1.5;
            }
            h1 {
                text-align: center;
                font-size: 16pt;
                text-transform: uppercase;
                text-decoration: underline;
                margin-bottom: 30px;
            }
            .header {
                text-align: center;
                margin-bottom: 25px;
            }
            .section-title {
                font-weight: bold;
                margin-top: 15px;
            }
            .signature {
                margin-top: 30px;
                width: 100%;
            }
            .signature-line {
                margin-top: 40px;
                border-top: 1px solid black;
                width: 200px;
                display: inline-block;
            }
            .publishing-section {
                margin-top: 20px;
                padding: 10px;
                border: 1px solid #ccc;
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        <h1>License Agreement For Beat "{{ BEAT }}"</h1>
        
        <p><strong>THIS LICENCE AGREEMENT</strong> is made on {{ DATE }} ("Effective Date") by and between <strong>{{ ARTIST }}</strong> (hereinafter referred to as the "Licensee") also, if applicable, professionally known as <strong>{{ NICK }}</strong>, whose principle address is <strong>{{ ADDRESS }}</strong>, and <strong>Dan White</strong> (hereinafter referred to as the "Licensor") also, if applicable, professionally known as Ayoswag, whose principle address is Vologda, Russia.</p>
        
        <p>Licensor warrants that it controls the mechanical rights in and to the copyrighted musical works entitled <strong>"{{ BEAT }}"</strong> ("Composition") as of and prior to the date first written above. The Composition, including the music thereof, was composed by White Dan ("Producer") managed under the Licensor.</p>
        
        <div class="section-title">Master Use.</div>
        <p>The Licensor hereby grants to Licensee an exclusive license (this "License") to record vocal synchronization to the Composition partly or in its entirety and substantially in its original form ("Master Recording").</p>
        
        <div class="section-title">Mechanical Rights.</div>
        <p>The Licensor hereby grants to Licensee an exclusive license to use Master Recording in the reproduction, duplication, manufacture, and distribution of phonograph records, cassette tapes, compact disk, digital downloads, other miscellaneous audio and digital recordings, and any lifts and versions thereof (collectively, the "Recordings", and individually, a "Recordings") worldwide for unlimited copies of such Recordings or any combination of such Recordings, condition upon the payment to the Licensor a sum of <strong>${{ PRICE }} USD</strong>, receipt of which is confirmed.</p>
        
        <div class="section-title">Performance Rights.</div>
        <p>The Licensor hereby grants to Licensee an exclusive license to use the Master Recording in unlimited for-profit performances, shows, or concerts.</p>
        
        <div class="section-title">Broadcast Rights.</div>
        <p>The Licensor hereby grants to Licensee an exclusive license to broadcast or air the Master Recording in unlimited amounts of radio stations.</p>
        
        <div class="section-title">Credit.</div>
        <p>Licensee shall acknowledge the original authorship of the Composition appropriately and reasonably in all media and performance formats under the name "Ayoswag" in writing where possible and vocally otherwise.</p>
        
        <div class="section-title">Consideration.</div>
        <p>In consideration for the rights granted under this agreement, Licensee shall pay to Licensor the sum of <strong>${{ PRICE }} USD</strong> and other good and valuable consideration, payable to "White Dan", receipt of which is hereby acknowledged.</p>
        
        <div class="section-title">Delivery.</div>
        <p>The Composition shall be delivered via email to an email address that Licensee provided when making their payment to Licensor.</p>
        
        <div class="section-title">Indemnification.</div>
        <p>Licensee agrees to indemnify and hold Licensor harmless from and against any and all claims, losses, damages, costs, expenses, including, without limitation, reasonable attorney's fees, arising of or resulting from a claimed breach of any of Licensee's representations, warranties or agreements hereunder.</p>
        
        <div class="section-title">Audio Samples.</div>
        <p>3rd party sample clearance is the responsibility of the Licensee.</p>
        
        <div class="section-title">Miscellaneous.</div>
        <p>This license is non-transferable and is limited to the Composition specified above, constitutes the entire agreement between the Licensor and the Licensee relating to the Composition, and shall be binding upon both the Licensor and the Licensee and their respective successors, assigns, and legal representatives.</p>
        
        <div class="section-title">Governing Law.</div>
        <p>This License is governed by and shall be construed under the law of Vologda, Russia, without regard to the conflicts of laws principles thereof.</p>
        
        <div class="publishing-section">
            <p><strong>Publishing.</strong></p>
            <p>{{ ARTIST }} owns <strong>{{ PUBLISHING }}%</strong> of publishing rights.</p>
            <p>Dan White owns <strong>{{ PRODUCER_PUBLISHING }}%</strong> of publishing rights.</p>
        </div>
        
        <p>Finished audio recording by Licensee of audio release can be distributed to music supervisors for synchronization licensing. This license includes synchronization rights for the TV, Film, and Video game industry. The Licensee is authorized to monetize and clear synchronization placements for these media under the terms of this agreement.</p>
        
        <div class="signature">
            <p><strong>THE PARTIES HAVE DULY EXECUTED THIS AGREEMENT on the date first written above.</strong></p>
            <br><br>
            <p><strong>Licensor:</strong></p>
            <div class="signature-line">Dan White - Producer</div>
            <br>
            <p>Date: {{ DATE }}</p>
            <br><br>
            <p><strong>Licensee:</strong></p>
            <div class="signature-line">{{ ARTIST }} - Artist</div>
            <br>
            <p>Date: {{ DATE }}</p>
        </div>
    </body>
    </html>
    """
    
    template = Template(html_template)
    return template.render({
        "BEAT": data["beat"],
        "ARTIST": data["artist"],
        "NICK": data["nick"],
        "ADDRESS": data["address"],
        "PRICE": data["price"],
        "PUBLISHING": publishing,
        "PRODUCER_PUBLISHING": producer_publishing,
        "DATE": data["date"] if data["date"] else datetime.now().strftime("%m.%d.%y")
    })

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📄 Exclusive Rights", callback_data="exclusive"),
            InlineKeyboardButton("📄 Unlimited Lease", callback_data="rent")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Привет! Я бот для создания договоров на биты.\n\n"
        "Выбери тип договора:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    contract_type = query.data
    context.user_data['contract_type'] = contract_type
    await query.edit_message_text(
        f"✅ Выбран: {CONTRACT_TYPES[contract_type]['name']}\n\n"
        "Теперь отправь данные в таком порядке (каждое с новой строки):\n\n"
        "1️⃣ Название бита\n"
        "2️⃣ Имя артиста\n"
        "3️⃣ Никнейм\n"
        "4️⃣ Адрес\n"
        "5️⃣ Цена (только цифры)\n"
        "6️⃣ Процент паблишинга (только цифры)\n"
        "7️⃣ Дата (в формате MM.DD.YY)\n\n"
        "📝 Пример:\n"
        "Follow Me\n"
        "Lil Pump\n"
        "@lilpump\n"
        "Miami, USA\n"
        "100\n"
        "50\n"
        "01.15.26"
    )

async def generate_contract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lines = text.split("\n")
    
    if 'contract_type' not in context.user_data:
        await update.message.reply_text("⚠️ Сначала выбери тип договора через /start")
        return
    
    if len(lines) < 7:
        await update.message.reply_text(
            f"❌ Нужно ввести ровно 7 строк!\n"
            f"Ты ввел {len(lines)} строк."
        )
        return
    
    data = {
        "beat": lines[0].strip(),
        "artist": lines[1].strip(),
        "nick": lines[2].strip(),
        "address": lines[3].strip(),
        "price": lines[4].strip(),
        "publishing": lines[5].strip(),
        "date": lines[6].strip()
    }
    
    try:
        int(data["price"])
        int(data["publishing"])
    except ValueError:
        await update.message.reply_text("❌ Цена и паблишинг должны быть числами!")
        return
    
    contract_type = context.user_data['contract_type']
    
    # Генерируем HTML-контент
    html_content = get_contract_html(data, contract_type)
    
    # Создаём PDF
    pdf_filename = f"{data['artist']}_{data['beat']}_{contract_type}.pdf"
    HTML(string=html_content).write_pdf(pdf_filename)
    
    # Отправляем PDF
    await update.message.reply_document(
        document=open(pdf_filename, "rb"),
        filename=pdf_filename
    )
    
    # Удаляем файл
    os.remove(pdf_filename)
    
    context.user_data['contract_type'] = None
    await update.message.reply_text(
        "✅ Готово! PDF договор отправлен.\n"
        "Чтобы создать новый - нажми /start"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_contract))
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
