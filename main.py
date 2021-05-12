import discord
from discord.ext import commands, tasks
import re
import time as Time
from event import Event

client = commands.Bot(command_prefix='~')

events = []


@client.event
async def on_ready():
    print('ready')
    check_list.start()
    await client.change_presence(
        status=discord.Status.online)


@client.command()
async def schedule(ctx, time, *, title):
    '''
    Enter a time and title with the format hh:mm title. Ex for 9pm: 21:00 title
    :param title:
    :param ctx:
    :param time:
    :return:
    '''
    if not re.match('([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', time):
        await ctx.channel.send('Invalid time')
        return

    for event in events:
        if event.title == title:
            await ctx.channel.send(f'There is already a schedule set for {event.title} at {event.time}')
            return

    await ctx.channel.send(f'Scheduled an event for {title} at {time}')
    events.append(Event(ctx.message.author, time, title))


@client.command()
async def unschedule(ctx, *, title: str):
    '''
    Remove a scheduled event
    :param ctx:
    :param title:
    :return:
    '''
    title = title.lower()
    for event in events:
        if title == event.title:
            if ctx.message.author == event.scheduler:
                events.remove(event)
                await ctx.channel.send(f'Unscheduled {event.title}')
                return
            else:
                await ctx.channel.send('Only the scheduler can remove this schedule')
                return

    ctx.message.send(f'There is no schedule for {title}')


@client.command()
async def subscribe(ctx, *, title):
    '''
    Subscribe to an event
    :param ctx:
    :param title:
    :return:
    '''
    for event in events:
        if event.title == title:
            event.add_subscriber(ctx.message.author)
            await ctx.channel.send(f'You have subscribed to {event.title}')
            return
    await ctx.channel.send(f'There is no schedule for {title}')


@client.command()
async def unsubscribe(ctx, title):
    '''
    Unsubscribe from an event
    :param ctx:
    :param title:
    :return:
    '''
    for event in events:
        if event.title == title:
            event.remove_subscriber(ctx.message.author)
            await ctx.channel.send(f'You have unsubscribed from {event.title}')
            return
    await ctx.channel.send(f'There is no schedule for {title}')


@tasks.loop(seconds=10)
async def check_list():
    current = ':'.join(Time.ctime().split(' ')[3].split(':')[:2])
    f = Time.strptime(current, '%H:%M')
    time_from = f.tm_hour * 60 + f.tm_min
    for event in events:
        t = Time.strptime(event.time, '%H:%M')
        event_time = t.tm_hour * 60 + t.tm_min
        if time_from == event_time:
            for subscriber in event.subscribers:
                receiver = await subscriber.create_dm()
                await receiver.send(f'{event.title} is starting')

            events.remove(event)


token = '' #bot token here
client.run(token)
