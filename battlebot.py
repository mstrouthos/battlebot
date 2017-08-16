# BattleBot project is a Discord Bot that enables users to retrieve stats for
# any Player Unknown's Battelgrounds player.
# BattleBot was developed by Mr_Sparrow (Michalis Strouthos)

import discord
import asyncio
import json
import os
from pypubg import core

api = core.PUBGAPI(os.environ['PUBG_KEY'])

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!battlebot'):
        reply = 'Hello @everyone, I am **' + client.user.name + '**, I can inform you about PUBG stats for any player!\n\n'
        reply += 'Here are the things you can ask me to do:'
        reply += '\n'
        reply += '**!battlebot**: I introduce myself to everyone and inform them about how I can help.\n'
        reply += '**!stats** {pubg_username}: Retrieves the stats for the provided username for all regions and modes.\n'
        reply += '**!stats** {region} {pubg_username}: Retrieves the stats for the provided player for all modes for the region specified.\n'
        reply += '**!chicken** {pubg_username}: Shows how many chicken dinners the player specified has in total. :poultry_leg: \n'
        reply += '\n'
        reply += 'BattleBot reporting for duty!\n'
        await client.send_message(message.channel, reply)
    elif message.content.startswith('!stats'):
        split_input = message.content.split()
        if(len(split_input) == 2):
            region_filter = 'agg'
            player_name = split_input[1]
        elif(len(split_input) == 3):
            region_filter = split_input[1]
            player_name = split_input[2]

        tmp = await client.send_message(message.channel, 'Retrieving player stats for ' + player_name)

        player_stats = api.player(player_name)

        if('error' in player_stats):
            await client.send_message(message.channel, 'There was an error retrieving stats for ' + player_name +'. Please try again later.')
        else:
            stats = player_stats['Stats']
            stats_filter = ['KillDeathRatio', 'RoundsPlayed', 'WinRatio', 'Wins', 'Top10s', 'Kills', 'Rating']
            stats_string = ""
            for stat in stats:
                region_stats = stat
                if(region_stats['Region'] == region_filter.lower()):
                    stats_string += '**' + region_stats['Match'].capitalize() + '** : '

                    for region_stat in region_stats['Stats']:
                        if region_stat['field'] in stats_filter:
                                stats_string += region_stat['label'] + ': ' + region_stat['value'] + ' | '
                    stats_string+= '\n'
            if(region_filter == 'agg'):
                region = 'all regions'
            else:
                region = region_filter.upper()

            if(stats_string == ''):
                await client.edit_message(tmp, 'No stats available for ' + player_name + ' for ' + region + '\n')
            else:
                await client.edit_message(tmp, 'Stats for ' + player_name + ' for ' + region + ': \n' + stats_string)
            # await client.edit_message(tmp, 'No stats found for this player!')

    elif message.content.startswith('!chicken'):
        split_input = message.content.split()
        player_name = split_input[1];

        tmp = await client.send_message(message.channel, 'Cooking some chicken for ' + player_name)

        player_stats = api.player(player_name)
        if('error' in player_stats):
            await client.send_message(message.channel, 'There was an error retrieving stats for ' + player_name +'. Please try again later.')
        else:
            stats = player_stats['Stats']
            stats_filter = ['Wins']
            reply = ""
            for stat in stats:
                region_stats = stat
                if(region_stats['Region'] == 'agg'):
                    for region_stat in region_stats['Stats']:
                        if region_stat['field'] in stats_filter:
                                for dinners in range(0, int(region_stat['value'])):
                                    reply += ' :poultry_leg: '

            await client.edit_message(tmp, reply)

    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run(os.environ['BOT_TOKEN'])
