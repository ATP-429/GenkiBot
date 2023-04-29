from discord import app_commands
import discord
import pickle
import os


class Scoreboard:
	def __init__(self):
		score_file = open("score.txt", "rb")
		self.scores = pickle.load(score_file)
		print("Loaded")

	async def loadData(self):
		score_file = open("score.txt", "rb")
		self.scores = pickle.load(score_file)
		print("Loaded")

	async def saveData(self):
		score_file = open("score.txt", "wb")
		pickle.dump(self.scores, score_file)

	async def register(self, user_id):
		self.scores[user_id] = 0
		await self.saveData()

	async def add(self, user_id):
		if user_id not in self.scores:
			self.scores[user_id] = 0
		self.scores[user_id] += 1
		await self.saveData()
	
	async def sub(self, user_id):
		if user_id not in self.scores:
			self.scores[user_id] = 0
		self.scores[user_id] -= 1
		await self.saveData()

	async def printLeaderboard(self):
		embed=discord.Embed(title="SCOREBOARD", color=discord.Color.blue())
		print(self.scores)
		user_str, score_str = "", ""
		for user_id, score in self.scores.items():
			user_str += bot.get_user(user_id).name + "\n"
			score_str += str(score)+"\n"
		embed.add_field(name="Name", value=user_str, inline=True)
		embed.add_field(name="Lessons", value=score_str, inline=True)
		return embed

f = open("token.txt")
DISCORD_TOKEN = f.read()

scoreboard = Scoreboard()
scoreboard.loadData()



# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)

# async def confirm(message):
# 	await message.add_reaction('👍')

@tree.command(name="add", description="Call this command after you complete a Genki Chapter")
async def slash_command(interaction: discord.Interaction):
	global scoreboard
	await scoreboard.add(interaction.user.id)
	await interaction.response.send_message("Congrats! "+(await scoreboard.printLeaderboard()))

@tree.command(name="sub", description="Call this command if you want to erase your doing of a Genki Chapter")
async def slash_command(interaction: discord.Interaction):
	global scoreboard
	await scoreboard.sub(interaction.user.id)
	await interaction.response.send_message("Chapter record deleted. "+(await scoreboard.printLeaderboard()))

@tree.command(name="register", description="Call this command if you want to register yourself on the scoreboard")
async def slash_command(interaction: discord.Interaction):
	global scoreboard
	await scoreboard.register(interaction.user.id)
	await interaction.response.send_message("Registered!")

@tree.command(name="show", description="Call this command if you want to display the scoreboard")
async def slash_command(interaction: discord.Interaction):
	global scoreboard
	await interaction.response.send_message(embed=await scoreboard.printLeaderboard())

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
	await tree.sync()
	print("Ready!")

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)