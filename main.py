import os
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("❌ Переменная окружения DISCORD_TOKEN не установлена!")

intents = discord.Intents.default()
intents.message_content = True  # для текстовых команд
intents.guilds = True           # для slash-команд

bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------- МОДАЛЬНАЯ ФОРМА --------------------
class ContractModal(discord.ui.Modal, title="Заполнение контракта"):
    def __init__(self):
        super().__init__()

        # Ссылка на скриншот
        self.add_item(discord.ui.TextInput(
            label="Ссылка на скриншот",
            placeholder="Вставьте ссылку на скриншот",
            required=True
        ))

        # Галочка "Активировал контракт?" через Select
        self.add_item(discord.ui.Select(
            placeholder="Активировал контракт?",
            options=[
                discord.SelectOption(label="Да", value="Активировал"),
                discord.SelectOption(label="Нет", value="Не активировал")
            ],
            min_values=1,
            max_values=1
        ))

        # Тип контракта
        self.add_item(discord.ui.Select(
            placeholder="Выберите тип контракта",
            options=[
                discord.SelectOption(label="Дары моря", value="Дары моря"),
                discord.SelectOption(label="Металлургия", value="Металлургия"),
                discord.SelectOption(label="Товары", value="Товары"),
                discord.SelectOption(label="Ателье", value="Ателье")
            ],
            min_values=1,
            max_values=1
        ))

    async def on_submit(self, interaction: discord.Interaction):
        screenshot = self.children[0].value
        activated = self.children[1].values[0]
        contract_type = self.children[2].values[0]

        # Словарь каналов по типу контракта
        channels_map = {
            'Дары моря': 1427776962390261801,
            'Металлургия': 1427776981432406117,
            'Товары': 1427777104879288550,
            'Ателье': 1427777125519458384
        }

        channel_id = channels_map.get(contract_type)
        channel = bot.get_channel(channel_id)

        if channel:
            await channel.send(
                f"**{interaction.user.mention}**\n"
                f"Тип контракта: {contract_type}\n"
                f"Скриншот: {screenshot}\n"
                f"{activated} контракт"
            )

        await interaction.response.send_message("Форма отправлена!", ephemeral=True)

# -------------------- СОБЫТИЯ --------------------
@bot.event
async def on_ready():
    print(f"✅ Бот запущен как {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Синхронизировано {len(synced)} команд.")
    except Exception as e:
        print(f"Ошибка синхронизации команд: {e}")

# -------------------- ТЕСТОВАЯ КОМАНДА --------------------
@bot.tree.command(name="ping", description="Проверить отклик бота")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

# -------------------- КОМАНДА /CONTRACTS --------------------
@bot.tree.command(name="contracts", description="Заполнить форму контракта")
async def contracts(interaction: discord.Interaction):
    modal = ContractModal()
    await interaction.response.send_modal(modal)

# -------------------- ЗАПУСК --------------------
bot.run(TOKEN)
