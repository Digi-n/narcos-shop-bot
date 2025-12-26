from flask import Flask
import threading
import discord
from discord.ext import commands
from discord import app_commands
import os
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()
# ======================
# CONFIG
# ======================
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN is missing! Add it in Render environment variables.")

GUILD_ID = 1451761878089990257
SYNDICATE_ROLE = "Syndicate Member"

# ======================
# BOT SETUP
# ======================
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ======================
# SHOP ITEMS
# ======================
PRODUCTS = {
    "Advanced Lockpick": 200000,
    "Weed OG Seed": 10000,
    "Pestle & Mortar": 20000,
    "Chemical Beaker": 15000,
    "Portable Meth Lab": 25000,
    "Meth Test Kit": 5000,
    "Egg Timer": 10000,
    "Hydrochloric Acid": 20000,
    "Red Phosphorus": 25000,
    "Lithium": 22000,
    "Pseudoephedrine": 23000,
    "Acetone": 10000,
    "5.56×45 Ammo": 500,
    "Liquid Fertilizer": 8000,
    "Watering Can": 4000,
    "Fertilizer": 1200,
    "Advanced Fertilizer": 6000
}

# ======================
# SHOP MODAL
# ======================
class ShopModal(discord.ui.Modal, title="🕷️ Black Market Order"):
    def __init__(self):
        super().__init__()

        self.inputs = {}
        for item in list(PRODUCTS.keys())[:5]:  # Discord limit
            field = discord.ui.TextInput(
                label=item,
                placeholder="Enter quantity (leave empty if none)",
                required=False
            )
            self.add_item(field)
            self.inputs[item] = field

    async def on_submit(self, interaction: discord.Interaction):
        total = 0
        summary = ""

        for name, field in self.inputs.items():
            if field.value:
                qty = int(field.value)
                price = PRODUCTS[name]
                cost = qty * price
                total += cost
                summary += f"• **{name}** × {qty} = **${cost:,}**\n"

        if not summary:
            await interaction.response.send_message(
                "❌ No items selected.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="🧾 BLACK MARKET PURCHASE",
            description=summary,
            color=0x8B0000
        )

        embed.add_field(name="💰 Total", value=f"${total:,}", inline=False)
        embed.add_field(name="👤 Buyer", value=interaction.user.mention, inline=False)

        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("✅ Order submitted.", ephemeral=True)


# ======================
# SHOP COMMAND
# ======================
@bot.tree.command(name="shop", description="Open the black market shop")
async def shop(interaction: discord.Interaction):

    if not any(role.name == SYNDICATE_ROLE for role in interaction.user.roles):
        await interaction.response.send_message(
            "❌ Only Syndicate Members can use this.",
            ephemeral=True
        )
        return

    await interaction.response.send_modal(ShopModal())


# ======================
# READY
# ======================
@bot.event
async def on_ready():
    guild = discord.Object(id=1451761878089990257)

    # Clear old commands
    bot.tree.clear_commands(guild=guild)

    # Sync fresh commands
    await bot.tree.sync(guild=guild)

    print(f"✅ Bot is online as {bot.user}")


# ======================
# RUN
# ======================
bot.run(TOKEN)



