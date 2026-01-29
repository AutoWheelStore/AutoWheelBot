from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import pandas as pd

ORG_NAME = "AutoWheel Store"
ADDRESS = "Москва, ул. Южнопортовая, 46"
WORK_TIME = "10:00–19:00"
FOUNDATION_YEAR = 2014

df = pd.read_csv("applicability.csv")

def find_applicability(pcd, dia):
    result = df[(df["pcd"] == pcd) & (df["dia"] <= float(dia))]
    return "\n".join(f"- {r.brand} {r.model}" for r in result.itertuples())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Введите параметры:\n"
        "/build R WIDTH PCD ET DIA\n"
        "Пример:\n/build 22 10 5x130 0 84.1"
    )

async def build(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r, w, pcd, et, dia = context.args
        cars = find_applicability(pcd, dia)

        text = f"""
Кованые диски R{r}
PCD: {pcd} | DIA: {dia}

Подходят для:
{cars}

{ORG_NAME}
{ADDRESS}
{WORK_TIME}
Основаны в {FOUNDATION_YEAR}
"""
        await update.message.reply_text(text)
    except:
        await update.message.reply_text("Ошибка формата. Используйте /build")

app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("build", build))
app.run_polling()
