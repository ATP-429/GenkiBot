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
		s = "\nSCOREBOARD\n"
		print(self.scores)
		for user_id, score in sorted(self.scores.items(), key=lambda x: x[1], reverse=True):
			s += f"{(await bot.fetch_user(user_id)).name} : {score} lessons completed!\n"
		return s

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
	await interaction.response.send_message(await scoreboard.printLeaderboard())

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
	await tree.sync()
	print("Ready!")

# #EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
# @bot.event
# async def on_message(message):
# 	global scoreboard
# 	if message.channel.name == "scoreboard":
# 		if message.content == "!show":
# 			await message.channel.send(await scoreboard.printLeaderboard())
# 			await confirm(message)
# 		if message.content == "!register":
# 			await scoreboard.register(message.author.id)
# 			await confirm(message)
# 		if message.content == "!add":
# 			await scoreboard.add(message.author.id)
# 			await confirm(message)
# 		if message.content == "!sub":
# 			await scoreboard.sub(message.author.id)
# 			await confirm(message)
		

# @bot.event
# async def on_reaction_add(reaction, user):
#     message = reaction.message # our embed
#     channel = discord.utils.get(message.guild.channels, name="welcome") #our channel
#     if message.channel.id == channel.id: # checking if it's the same channel
#         if message.author == bot.user: #checking if it's sent by the bot
#             if reaction.emoji.name == "👋🏽": #checking the emoji
#                 # enter code here, user is person that reacted

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)