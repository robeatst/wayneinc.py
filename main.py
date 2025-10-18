import os
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("❌ Переменная окружения DISCORD_TOKEN не установлена!")

intents = discord.Intents.default()
intents.message_content = True  # для текстовых команд
intents.guilds = True            # для slash-команд

bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------- МОДАЛЬНАЯ ФОРМА --------------------
class ContractModal(discord.ui.Modal, title="Заполнение контракта"):
    def __init__(self, channel_id: int):
        super().__init__()
        self.channel_id = channel_id

        # Ссылка на скриншот
        self.add_item(discord.ui.InputText(
            label="Ссылка на скриншот",
            placeholder="Вставьте ссылку на скриншот",
            required=True
        ))

        # Галочка "Активировал контракт?" через Select (1 вариант)
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
                discord.SelectOption(label="Товары со склада", value="Товары со склада")
            ],
            min_values=1,
            max_values=1
        ))

    async def on_submit(self, interaction: discord.Interaction):
        screenshot = self.children[0].value
        activated = self.children[1].values[0]
        contract_type = self.children[2].values[0]

        channel = bot.get_channel(self.channel_id)
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

# -------------------- КОМАНДА /КОНТРАКТ --------------------
@bot.tree.command(name="контракт", description="Заполнить форму контракта")
async def contract(interaction: discord.Interaction):
    channel_id = 1427776903552438447  # ID текстового канала для отправки сообщений
    modal = ContractModal(channel_id)
    await interaction.response.send_modal(modal)

# -------------------- ЗАПУСК --------------------
bot.run(TOKEN)
