import asyncio, os, csv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from services.wheel_selector import get_wheel_data, format_wheel_answer

BOT_TOKEN = os.getenv("BOT_TOKEN")
CSV_PATH = "data/car_models_global.csv"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# CSV helpers
def get_brands():
    brands = set()
    with open(CSV_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            brands.add(row["brand"])
    return sorted(brands)

def get_models(brand):
    models = set()
    with open(CSV_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["brand"] == brand:
                models.add(row["model"])
    return sorted(models)

def get_years(brand, model):
    years = set()
    with open(CSV_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["brand"] == brand and row["model"] == model:
                for y in range(int(row["year_start"]), int(row["year_end"])+1):
                    years.add(y)
    return sorted(years)

# Handlers
@dp.message(Command("start"))
async def start(msg: Message):
    brands = get_brands()[:12]
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=b, callback_data=f"brand:{b}")] for b in brands])
    await msg.answer("🚗 Выберите марку автомобиля:", reply_markup=kb)

@dp.callback_query(F.data.startswith("brand:"))
async def choose_model(cb: CallbackQuery):
    brand = cb.data.split(":")[1]
    models = get_models(brand)[:12]
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=m, callback_data=f"model:{brand}:{m}")] for m in models])
    await cb.message.edit_text(f"Марка: {brand}\nВыберите модель:", reply_markup=kb)

@dp.callback_query(F.data.startswith("model:"))
async def choose_year(cb: CallbackQuery):
    _, brand, model = cb.data.split(":")
    years = get_years(brand, model)[-10:]
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(y), callback_data=f"year:{brand}:{model}:{y}")] for y in years])
    await cb.message.edit_text(f"{brand} {model}\nВыберите год:", reply_markup=kb)

@dp.callback_query(F.data.startswith("year:"))
async def finish(cb: CallbackQuery):
    _, brand, model, year = cb.data.split(":")
    wheel_data = get_wheel_data(brand, model, year)
    answer = format_wheel_answer(wheel_data)
    await cb.message.edit_text(f"✅ Автомобиль выбран:\n{brand} {model} {year}\n\n{answer}\n👇 Дальше можно: подбор шин, рассчитать цену")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
