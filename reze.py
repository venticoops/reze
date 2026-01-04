
# This file is made by REI otherwise known as KeiNeroKami in Github
# ====================<REIME>====================
# This are snippets for making a bot/App in Discord
# ===============================================

import json, nextcord, random, os
from nextcord.ext import commands
from nextcord import ButtonStyle, Embed, SelectOption, SlashOption
from nextcord.ui import Button, View, Select
from dotenv import load_dotenv

# --------------------------------------

# NOTES: 

# --------------------------------------

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="+", intents=intents)

# Bonus tip for making slash commands
# ---------- Auto-sync Slash Commands ----------

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(
        status=nextcord.Status.idle, # Options: online, idle, dnd, invisible
        activity=nextcord.Activity(
            name="✨ i love you",
            type=nextcord.ActivityType.playing, # Options: playing, streaming, listening, watching, competing
        )
    )
    print("Presence set!")
    await bot.sync_all_application_commands()
    print("synced!")

#------------------------------------

# ===============================
# JSON HELPERS
# ===============================

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --------------------------------

ocs = json.load(open(r"C:\Users\Usuario\Desktop\all\reze\data\ocs.json"))

oc_list = ocs["oc_list"]
frai_oc = ocs["frai_oc"]
kei_oc = ocs["kei_oc"]

@bot.command()
async def randomoc(ctx, amount: int, whose: str = None):
    
    if whose == "kei":
        list = random.choices(kei_oc, k=amount)
        chosen = ", ".join(list)
    elif whose == "frai":
        list = random.choices(frai_oc, k=amount)
        chosen = ", ".join(list)
    elif whose == None:
        list = random.choices(oc_list, k=amount)
        chosen = ", ".join(list)

    await ctx.send(f"chosen oc(s) were: '{chosen}'")

@bot.slash_command(name="randomoc", description="gives random oc")
async def randomoc_slash(interaction: nextcord.Interaction, amount: int, whose: str = nextcord.SlashOption(required=False, choices={"Frai": "frai", "Kei": "kei"})):

    if whose is None:
        list = random.choices(oc_list, k=amount)
        chosen =  ", ".join(list)
    elif whose == "frai":
        list = random.choices(frai_oc, k=amount)
        chosen = ", ".join(list)
    elif whose == "kei":
        list = random.choices(kei_oc, k=amount)
        chosen = ", ".join(list)
    
    await interaction.response.send_message(f"chosen oc(s) were: '{chosen}'")

# --------------------------------

MOVIES_FILE = r"C:\Users\Usuario\Desktop\all\reze\data\movies.json"
movies = load_json(MOVIES_FILE, [])

@bot.group(invoke_without_command=True)
async def movielist(ctx):
    if not movies:
        await ctx.send("🎬 La lista está vacía")
    else:
        await ctx.send("🎬 Lista actual:\n" + "\n".join(movies))

@movielist.command()
async def add(ctx, *, movie: str):
    movies.append(movie)
    save_json(MOVIES_FILE, movies)
    await ctx.send(f"✅ Agregada: **{movie}**\n🎬 Lista:\n" + "\n".join(movies))

@movielist.command()
async def remove(ctx, *, movie: str):
    if movie not in movies:
        await ctx.send("❌ Esa película no está en la lista")
        return
    movies.remove(movie)
    save_json(MOVIES_FILE, movies)
    await ctx.send(f"🗑️ Eliminada: **{movie}**\n🎬 Lista:\n" + "\n".join(movies))

@bot.slash_command(name="movielist", description="Manage the movie list")
async def movielist(
    interaction: nextcord.Interaction,

    action: str = SlashOption(
        name="action",
        description="What do you want to do?",
        choices={
            "Show list": "show",
            "Add movie": "add",
            "Remove movie": "remove"
        }
    ),

    movie: str = SlashOption(
        name="movie",
        description="Movie name (required for add/remove)",
        required=False
    )
):
    # SHOW
    if action == "show":
        if not movies:
            await interaction.response.send_message("🎬 La lista está vacía")
        else:
            await interaction.response.send_message(
                "🎬 Lista actual:\n" + "\n".join(movies)
            )

    # ADD
    elif action == "add":
        if not movie:
            await interaction.response.send_message(
                "❌ Debes indicar una película para agregar",
                ephemeral=True
            )
            return

        movies.append(movie)
        save_json(MOVIES_FILE, movies)

        await interaction.response.send_message(
            f"✅ Agregada: **{movie}**\n🎬 Lista:\n" + "\n".join(movies)
        )

    # REMOVE
    elif action == "remove":
        if not movie:
            await interaction.response.send_message(
                "❌ Debes indicar una película para eliminar",
                ephemeral=True
            )
            return

        if movie not in movies:
            await interaction.response.send_message(
                "❌ Esa película no está en la lista",
                ephemeral=True
            )
            return

        movies.remove(movie)
        save_json(MOVIES_FILE, movies)

        await interaction.response.send_message(
            f"🗑️ Eliminada: **{movie}**\n🎬 Lista:\n" + "\n".join(movies)
        )

# -----------------------------

TEST_GUIDE_FILE= r"C:\Users\Usuario\Desktop\all\reze\data\test.json"
test = load_json(TEST_GUIDE_FILE, [])

async def createTestEmbed(pageNum=0, inline=False):
    pageNum = pageNum % len(list(test))
    pageTitle = list(test)[pageNum]
    embed=Embed(title=pageTitle)
    for key, val in test[pageTitle].items():
        embed.add_field(name=key, value=val, inline=inline)
        embed.set_footer(text=f"Page {pageNum+1} of {len(list(test))}")
    return embed

@bot.command()
async def testing(ctx):
    currentPage=0

    async def next_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage += 1
        await sent_msg.edit(embed= await createTestEmbed(pageNum=currentPage), view=myview)

    async def previous_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage -= 1
        await sent_msg.edit(embed= await createTestEmbed(pageNum=currentPage), view=myview)


    nextButton = Button(label=">", style=ButtonStyle.secondary)
    nextButton.callback = next_callback
    previousButton = Button(label="<", style=ButtonStyle.secondary)
    previousButton.callback = previous_callback

    myview = View(timeout=180)
    myview.add_item(previousButton)
    myview.add_item(nextButton)
    sent_msg = await ctx.send(embed=await createTestEmbed(), view=myview)

# --------------------------------

#@bot.command()
#async def testTwo(ctx):
#    option1= SelectOption(label="one", value="first", description="one, first", emoji="1️⃣")
#    option2= SelectOption(label="two", value="second", description="two, second", emoji="2️⃣")
#    option3= SelectOption(label="three", value="third", description="three, third", emoji="3️⃣")
#    dropdown = Select(placeholder="choose!", options=[option1, option2, option3], max_values=3)
#    await ctx.send("Hi!!")

# --------------------------------

bot.run(TOKEN)

