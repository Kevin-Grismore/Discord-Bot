import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

d2_headers = {'X-API-KEY': os.getenv('D2KEY')}

def get_d2_player(platform, name):
  url = "https://www.bungie.net/Platform/Destiny2/SearchDestinyPlayer/{0}/{1}".format(platform, name)
  r = requests.get(url, headers=d2_headers)
  json_data = json.loads(r.text)
  response_text = json_data['Response']
  member_id = response_text[0]['membershipId']
  return member_id

def get_d2_player_name(platform, name):
  url = "https://www.bungie.net/Platform/Destiny2/SearchDestinyPlayer/{0}/{1}".format(platform, name)
  r = requests.get(url, headers=d2_headers)
  json_data = json.loads(r.text)
  names = []
  for i in range(len(json_data['Response'])):
    names.append(json_data['Response'][i]['displayName'])
  return names

def get_d2_characters(platform, name):
  member_id = get_d2_player(platform, name)
  url = "https://www.bungie.net/Platform/Destiny2/{0}/Profile/{1}/?components=100".format(platform, member_id)
  r = requests.get(url, headers=d2_headers)
  json_data = json.loads(r.text)
  character_ids = json_data['Response']['profile']['data']['characterIds']
  return character_ids

def get_d2_power(platform, name):
  member_id = get_d2_player(platform, name)
  character_ids = get_d2_characters(platform, name)
  powers = []
  for id in character_ids:
    url = "https://www.bungie.net/Platform/Destiny2/{0}/Profile/{1}/Character/{2}/?components=200".format(platform, member_id, id)
    r = requests.get(url, headers=d2_headers)
    json_data = json.loads(r.text)
    powers.append(json_data['Response']['character']['data']['light'])
  return powers

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  #The real Destiny 2 begins here
  if msg.startswith('!d2characters'):
    player_name = msg.split('!d2characters ', 1)[1]
    membership_id = get_d2_characters(3, player_name)
    await message.channel.send(membership_id)

  if msg.startswith('!d2power'):
    player_name = msg.split('!d2power ', 1)[1]
    d2_power = get_d2_power(3, player_name)
    await message.channel.send(d2_power)

  if msg.startswith('!d2player'):
    player_name = msg.split('!d2player ', 1)[1]
    d2_player_name = get_d2_player_name(3, player_name)
    await message.channel.send(d2_player_name)

keep_alive()
client.run(os.getenv('TOKEN'))