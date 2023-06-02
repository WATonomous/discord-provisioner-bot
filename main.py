import aiohttp
import discord
import logging
import os
from aiohttp import web
from discord.ext import tasks

logger = logging.getLogger('discord.wato-provisioner')

intents = discord.Intents.none()
intents.members = True

client = discord.Client(intents=intents)

# TODO: sentry integration for logging:
# https://docs.sentry.io/platforms/python/guides/logging/

@client.event
async def on_member_join(member):
    logger.info(f'{member} has joined the server.')

    # Trigger the provisioner
    logger.info("Triggering the provisioner")
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'https://api.github.com/repos/WATonomous/infra-config/dispatches',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.environ["GITHUB_TOKEN"]}',
                'Accept': 'application/vnd.github+json',
                'X-GitHub-Api-Version': "2022-11-28",
            },
            json={'event_type': 'provision-discord'},
        ) as resp:
            if resp.status == 204:
                logger.info('Successfully triggered the Discord provisioner.')
            else:
                logger.error(f'Failed to trigger the Discord provisioner. {resp.status=}')

@client.event
async def on_ready():
    logger.info(f'{client.user} has connected to Discord. Now setting up healthchecks')

    health_endpoint_app = web.Application()
    health_endpoint_app.add_routes([web.get('/health', health_endpoint)])
    health_endpoint_runner = web.AppRunner(health_endpoint_app)
    await health_endpoint_runner.setup()
    healthcheck_site = web.TCPSite(health_endpoint_runner, '0.0.0.0', 8000)
    await healthcheck_site.start()

    healthcheck_loop.start()

    logger.info("ready")

async def health_endpoint(_request):
    if client.is_closed():
        return web.Response(text='Client is closed!', status=500)
    else:
        return web.Response(text='OK')

@tasks.loop(seconds=60)
async def healthcheck_loop():
    logger.info(f'Healthcheck loop running. {client.is_closed()=}')
    # TODO: ping a dead man's switch

client.run(os.environ['DISCORD_TOKEN'])
