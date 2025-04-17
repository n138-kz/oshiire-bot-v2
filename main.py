import json
import os
import sys
import math
import discord
import datetime
import time
import logging
import zlib
import hashlib

from logging import getLogger, config as logger_config
config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s"
        }
    },
    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "fileHandler": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": "log/logging.log"
        }
    },
    "loggers": {
        "__main__": {
            "level": "DEBUG",
            "handlers": ["consoleHandler", "fileHandler"],
            "propagate": False
        },
        "same_hierarchy": {
            "level": "DEBUG",
            "handlers": ["consoleHandler", "fileHandler"],
            "propagate": False
        },
        "lower.sub": {
            "level": "DEBUG",
            "handlers": ["consoleHandler", "fileHandler"],
            "propagate": False
        }
    },
    "root": {
        "level": "INFO"
    }
}
config['formatters']['simple']['format']="%(asctime)s %(name)s:%(lineno)s [%(levelname)s]: %(message)s"
logger_config.dictConfig(config)
logger = getLogger(__name__)

# ファイルパス
GLOBAL_FILE = {
    'config': '.secret/config.json', # 設定
    'help': 'lib/command_help.json', # ヘルプファイル
    'notice_log': 'log/notice_%(time).json',
    'except_log': 'log/except_%(time).log',
    'result_log': 'log/result_%(time).log',
    'detail_log': 'log/detail_%(time).log',
    'async_log': 'log/async_%(time).log',
    'console_log': 'log/console_%(time).log',
}

# メッセージ定義
GLOBAL_TEXT = {
    'err': {
        'en':{
            'incomplete_command': '% Incomplete command',
            'your_not_admin': 'Your NOT Administrators',
            'require_args': 'Required the args',
            'invalid_args': 'Invalid the args',
            'dir_not_found': 'No such directory',
            'file_not_found': 'No such file or directory',
        },
        'ja':{
            'incomplete_command': 'コマンドが不完全です。',
            'your_not_admin': 'あなたは管理者ロールが付与されていません。',
            'require_args': '引数が必要です。',
            'invalid_args': '引数が無効です。',
            'dir_not_found': 'No such directory.',
            'file_not_found': 'No such file or directory.',
        }
    },
    'msg': {
        'en':{
            'init_mesg': 'INIT',
            'display_help':'Display the command help',
            'display_version':'Display the version',
            'calculate_ping':'Displays the latency of the bot',
            'pingpong':'The bot\'s ping value is %(ping)ms.',
            'display_help_resync':'Slash command resync',
            'require_admin_role':'*Require the admin-role',
        },
        'ja':{
            'init_mesg': 'INIT',
            'display_help':'コマンドヘルプを表示します。',
            'display_version':'Botのバージョンを表示します。',
            'calculate_ping':'Botのレイテンシを表示します。',
            'pingpong':'BotのPing値は%(ping)msです。',
            'display_help_resync':'Slash command resync',
            'require_admin_role':'※要管理者権限',
        }
    },
    'color': {
        'ok': 0x00ff00,
        'err': 0xff0000,
        'caution': 0xffa500,
    },
    'url': {
        'github': { 'repository': 'https://github.com/n138-kz/oshiire-bot-v2' },
        'discord': {
            'avatar':'',
        }
    }
}

# 言語
LOCALE = 'en'

logger.info(GLOBAL_TEXT['msg'][LOCALE]['init_mesg'])

def default_config():
    # Default settings
    logger.info('Load the default setting.')
    config = {
        "external": {
            "discord": {
                "token": ""
            }
        },
        "internal": {
            "discord": {
                "author": {
                    "url": "https://discord.com/",
                    "name": "Discord Bot",
                    "icon": "https://cdn.discordapp.com/embed/avatars/0.png"
                },
                "color": "ffffff",
                "title": "Hello World",
                "description": "",
                "image": {
                    "image": {
                        "url": ""
                    },
                    "thumbnail": {
                        "url": ""
                    }
                },
                "footer": {
                    "text": "Powered by n138-kz",
                    "icon": "https://github.com/n138-kz.png"
                }
            }
        }
    }
    return config

def commit_config(config=default_config(),file=GLOBAL_FILE['config']):
    config['internal']['meta'] = {}
    config['internal']['meta']['written_at'] = math.trunc(time.time())
    with open(file, mode='w',encoding='UTF-8') as f:
        json.dump(config, f, indent=4)
    logger.info('Config commit at: {0}'.format(config['internal']['meta']['written_at']))

def load_config(config_file=GLOBAL_FILE['config']):
    # Default settings
    config = default_config()

    # Check directory exist
    if not(os.path.isdir(os.path.dirname(config_file))):
        os.mkdir(os.path.dirname(config_file))
        logger.error(GLOBAL_TEXT['err']['en']['dir_not_found'])
        sys.exit(1)

    # Check file exist
    if not(os.path.isfile(config_file)):
        commit_config(config=config,file=config_file)
        logger.error(GLOBAL_TEXT['err']['en']['file_not_found'])
        sys.exit(1)

    with open(config_file,encoding='UTF-8') as f:
        config = json.load(f)

    # config = json.dumps(config,indent=4) # Debug
    logger.info('Config loaded at: {0}'.format(math.trunc(time.time())))
    return config

def getEnv(mode='help'):

    text=''

    if False:
        pass

    elif mode=='help':
        file=GLOBAL_FILE['help']
        if not(os.path.isfile(file)):
            text='{0}\n{1}'.format(
                '`'+COMMAND_PREFIX+' help`',
                GLOBAL_TEXT['msg'][LOCALE]['display_help'],
            )
            logger.warning('{0}: {1}'.format(GLOBAL_TEXT['err']['en']['file_not_found'], file))
        else:
            with open(file, encoding='UTF-8') as f:
                helps=json.load(f)
                for index,help in helps['command'].items():
                    text += ''
                    text += '`{0} {1}`\n{2}\n'.format(
                        helps['prefix'],
                        index,
                        help['description'],
                    )
                    if help['admin']:
                        text += GLOBAL_TEXT['msg'][LOCALE]['require_admin_role']+'\n'

        #text += text.replace(COMMAND_PREFIX+' ','/')
        return text
    elif mode=='version':
        # Version
        text = '{0}.{1}'.format(
            datetime.datetime.fromtimestamp(os.stat(__file__).st_mtime).strftime('%Y%m%d'),
            datetime.datetime.fromtimestamp(os.stat(__file__).st_mtime).strftime('%H%M%S'),
        )
        text = '{0}.{1}'.format(
            text,
            hashlib.md5(str(zlib.crc32(str(os.stat(__file__).st_mtime).encode('utf-8'))).encode()).hexdigest()[0:8],
        )
        return text
    elif mode=='ping':
        raw_ping = client.latency
        text = GLOBAL_TEXT['msg'][LOCALE]['pingpong'].replace(
            '%(ping)',
            '{0}'.format(round(raw_ping * 1000))
        )
        return text

config = load_config()

# 言語
LOCALE = 'ja'

# Discord APIトークン
DISCORD_API_TOKEN = config['external']['discord']['token']
logger.info('Discord Bot token has initiated.')

# ！コマンド接頭辞
COMMAND_PREFIX = '!oshiire'

# Discord Bot Setup
intents=discord.Intents.default()
intents.message_content = True
intents.reactions = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_message(message):
    # 変数初期化
    title=None
    descr=None
    color=0x000000
    text=None
    logfname_async=None
    logfname_detail=None

    # 送信者がbotである場合は弾く
    if message.author.bot:
        logger.warning('Call by Bot')
        return
    
    # テキストチャンネルのみ処理
    if message.channel.type != discord.ChannelType.text:
        logger.warning('Call on not text channel')
        return
    
    title='Result'
    descr=''
    
    if message.content.startswith(COMMAND_PREFIX):
        logger.info('on_message: {0}'.format(message.content))

        if False:
            pass

        elif message.content.startswith(COMMAND_PREFIX+' help'):
            logger.info('do_action: {0}'.format(message.content))
            logger.info('do_author: {0}'.format(message.author.name))
            title='Result'
            descr=''
            color=GLOBAL_TEXT['color']['ok']

            try:
                await message.channel.id.typing()
            except Exception as e:
                logging.error('Error has occured: {}'.format(e.reason))
            embed = discord.Embed(
                title=title,description=descr,color=color,
                url=GLOBAL_TEXT['url']['github']['repository'],
                timestamp=datetime.datetime.now(datetime.timezone.utc),
            )
            embed.set_thumbnail(url=GLOBAL_TEXT['url']['discord']['avatar'])
            embed.add_field(
                name='Result',
                value=getEnv(mode='help'),
                inline=False
            )
            embed.set_footer(icon_url=config['internal']['discord']['footer']['icon'],text=config['internal']['discord']['footer']['text'])
            embed.set_author(icon_url=config['internal']['discord']['author']['icon'],name=config['internal']['discord']['author']['name'],url=config['internal']['discord']['author']['url'])
            async_log = await message.reply(embed=embed)
            with open(file=os.getcwd()+'/'+GLOBAL_FILE['async_log'].replace('%(time)', str(math.trunc(time.time()))),encoding='utf-8',mode='w') as f:
                f.write('{0}'.format(async_log))

        elif message.content.startswith(COMMAND_PREFIX+' version'):
            logger.info('do_action: {0}'.format(message.content))
            logger.info('do_author: {0}'.format(message.author.name))
            title='Result'
            descr=''
            color=GLOBAL_TEXT['color']['ok']

            try:
                await message.channel.id.typing()
            except Exception as e:
                logging.error('Error has occured: {}'.format(e.reason))
            embed = discord.Embed(
                title=title,description=descr,color=color,
                url=GLOBAL_TEXT['url']['github']['repository'],
                timestamp=datetime.datetime.now(datetime.timezone.utc),
            )
            embed.set_thumbnail(url=GLOBAL_TEXT['url']['discord']['avatar'])
            embed.add_field(
                name='Result',
                value=getEnv(mode='version'),
                inline=False
            )
            embed.set_footer(icon_url=config['internal']['discord']['footer']['icon'],text=config['internal']['discord']['footer']['text'])
            embed.set_author(icon_url=config['internal']['discord']['author']['icon'],name=config['internal']['discord']['author']['name'],url=config['internal']['discord']['author']['url'])
            async_log = await message.reply(embed=embed,avatar_url=config['internal']['discord']['author']['icon'])
            with open(file=os.getcwd()+'/'+GLOBAL_FILE['async_log'].replace('%(time)', str(math.trunc(time.time()))),encoding='utf-8',mode='w') as f:
                f.write('{0}'.format(async_log))

        elif message.content.startswith(COMMAND_PREFIX+' ping'):
            logger.info('do_action: {0}'.format(message.content))
            logger.info('do_author: {0}'.format(message.author.name))
            title='Result'
            descr=''
            color=GLOBAL_TEXT['color']['ok']

            try:
                await message.channel.id.typing()
            except Exception as e:
                logging.error('Error has occured: {}'.format(e.reason))
            embed = discord.Embed(
                title=title,description=descr,color=color,
                url=GLOBAL_TEXT['url']['github']['repository'],
                timestamp=datetime.datetime.now(datetime.timezone.utc),
            )
            embed.set_thumbnail(url=GLOBAL_TEXT['url']['discord']['avatar'])
            embed.add_field(
                name='Pong',
                value=getEnv(mode='ping'),
                inline=False
            )
            embed.set_footer(icon_url=config['internal']['discord']['footer']['icon'],text=config['internal']['discord']['footer']['text'])
            embed.set_author(icon_url=config['internal']['discord']['author']['icon'],name=config['internal']['discord']['author']['name'],url=config['internal']['discord']['author']['url'])
            async_log = await message.reply(embed=embed,avatar_url=config['internal']['discord']['author']['icon'])
            with open(file=os.getcwd()+'/'+GLOBAL_FILE['async_log'].replace('%(time)', str(math.trunc(time.time()))),encoding='utf-8',mode='w') as f:
                f.write('{0}'.format(async_log))

@tree.command(name="help",description=GLOBAL_TEXT['msg'][LOCALE]['display_help'])
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(getEnv(mode='help'), ephemeral=True)#ephemeral=True→「これらはあなただけに表示されています」

@tree.command(name="help_resync",description=GLOBAL_TEXT['msg'][LOCALE]['display_help_resync'])
async def help_resync(interaction: discord.Interaction):
    await tree.sync()
    await interaction.response.send_message(getEnv(mode='help'), ephemeral=True)#ephemeral=True→「これらはあなただけに表示されています」

@tree.command(name="version",description=GLOBAL_TEXT['msg'][LOCALE]['display_version'])
async def version(interaction: discord.Interaction):
    await interaction.response.send_message(getEnv(mode='version'), ephemeral=True)#ephemeral=True→「これらはあなただけに表示されています」

@tree.command(name="ping",description=GLOBAL_TEXT['msg'][LOCALE]['calculate_ping'])
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(getEnv(mode='ping'), ephemeral=True)#ephemeral=True→「これらはあなただけに表示されています」

@client.event
async def on_ready():
    logger.info('--設定情報--')

    # スラッシュコマンドを同期
    logger.info('スラッシュコマンドを同期中')
    await tree.sync()
    logger.info('... [ OK ]')

    # アクティビティステータスを設定
    # https://qiita.com/ryo_001339/items/d20777035c0f67911454
    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=COMMAND_PREFIX+' help'))

    # Botアイコン設定
    GLOBAL_TEXT['url']['discord']['avatar']=config['internal']['discord']['author']['icon']

# Botを起動
def main():
    try:
        handler = logging.FileHandler(filename=GLOBAL_FILE['console_log'].replace('%(time)', str(math.trunc(time.time()))), encoding='utf-8', mode='w')
        client.run(DISCORD_API_TOKEN, log_handler=handler, log_level=logging.DEBUG, root_logger=True)
    except Exception as e:
        logging.error('Error has occured: {}'.format(e.reason))

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error('Error has occured: {}'.format(e.reason))
