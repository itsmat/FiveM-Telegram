import json
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
import requests
from main import ip
versione = '1.0'

def fallo(cmd):
    print(cmd)
    requestadmins = []

    requestadmins.append(cmd)

    with open('richieste.json', 'w') as json_file:
        json.dump(requestadmins, json_file)

def controllobuild():
	r = requests.get('http://' + ip + '/info.json')
	data = r.json()
	json_data = data['vars']
	return(json_data["sv_enforceGameBuild"])

def listarisorse():
	r = requests.get('http://' + ip + '/info.json')
	data = r.json()
	return(data["resources"])

def controlloplayeronline():
	r = requests.get('http://' + ip + '/dynamic.json')
	data = r.json()
	return(data["clients"])

def controlloplayermassimi():
	r = requests.get('http://' + ip + '/dynamic.json')
	data = r.json()
	return(data["sv_maxclients"])

def hostname():
	r = requests.get('http://' + ip + '/dynamic.json')
	data = r.json()
	return(data["hostname"])

chatrisorse = []
@Client.on_message(filters.command("start") & filters.private)
async def cmdstart(client, message):
    if message.from_user.id in chatrisorse:
        chatrisorse.remove(message.from_user.id)

    mess = await message.reply('__🔄 Caricamento...__')
    await mess.edit(f'''**🛠 Gestione Server**
IP: {ip}

Players: <code>{controlloplayeronline()}/{controlloplayermassimi()}</code>
Server Build: <code>{controllobuild()}</code>''', reply_markup=InlineKeyboardMarkup( 
                    [   
                        [InlineKeyboardButton(text="👥 Gestione Players", callback_data='gestioneplayerhome')],
                        [InlineKeyboardButton(text="🛠 Gestione Risorse", callback_data='gestiscirisorsehome')],
                        [InlineKeyboardButton(text="🧑‍💻 Source Code 🧑‍💻", url='https://github.com/itsmat')],
                    ]
                ))

@Client.on_callback_query(filters.regex("startcb"))
async def startcb(client, query):
    if query.from_user.id in chatrisorse:
        chatrisorse.remove(query.from_user.id)

    mess = await query.message.edit('__🔄 Caricamento...__')
    await mess.edit(f'''**🛠 Gestione Server**
IP: {ip}
Versione Bot: <code>{versione}</code>

Players: <code>{controlloplayeronline()}/{controlloplayermassimi()}</code>
Server Build: <code>{controllobuild()}</code>''', reply_markup=InlineKeyboardMarkup( 
                    [   
                        [InlineKeyboardButton(text="👥 Gestione Players", callback_data='gestioneplayerhome')],
                        [InlineKeyboardButton(text="🛠 Gestione Risorse", callback_data='gestiscirisorsehome')],
                        [InlineKeyboardButton(text="🧑‍💻 Source Code 🧑‍💻", url='https://github.com/itsmat')],
                    ]
                ))

@Client.on_message(filters.command("kick") & filters.private)
async def espellicmd(client, message):
    utente, motivo = message.command[1:3]
    motivo = " ".join(message.command[2:])
    fallo(f"clientkick {utente} [FiveM-Telegram] Motivo: {motivo} Da: {message.from_user.first_name}")
    await message.reply(f'ID:{utente} kickato')

@Client.on_callback_query(filters.regex("gestiscirisorsehome"))
async def gestiscirisorsehome(client, query):
    await query.answer("🔄 Caricamento") 
    chatrisorse.append(query.from_user.id)
    try:
        await query.message.edit(f'''**✅ Invia il nome della risorsa da gestire.**
    
📄 Lista risorse: {listarisorse()}
''', reply_markup=InlineKeyboardMarkup( 
                    [   
                        [InlineKeyboardButton(text="🔄 Refresh 🔄", callback_data=f'refresh')],
                        [InlineKeyboardButton(text="🏡 Home 🏡", callback_data=f'startcb')],
                    ]
                ))
    except:
        pass

@Client.on_callback_query(filters.regex("gestioneplayerhome"))
async def gestioneplayerhome(client, query):
    await query.answer("🔄 Caricamento") 
    await query.message.edit(f'''**Orientati con i bottoni sottostanti**

👉 Per kickare un giocatore /kick id motivo
''', reply_markup=InlineKeyboardMarkup( 
                    [   
                        [InlineKeyboardButton(text="📄 Lista Player 📄", callback_data=f'listaplayers')],
                        [InlineKeyboardButton(text="🏡 Home 🏡", callback_data=f'startcb')],
                    ]
                )) #listaplayers

@Client.on_callback_query(filters.regex("listaplayers"))
async def listaplayers(client, query):
    await query.answer("🔄 Caricamento") 
    players =  requests.get(f'http://{ip}/players.json', timeout=5)
    getplayers = players.json()
    playerlist = ''
    for player in getplayers: #player['id'] #player['name'] #player['identifiers']
        playerlist = f'''[<code>{player['id']}</code>] {player['name']}\n'''
    await query.message.edit(f'''**📄 Lista Players 📄**

{playerlist}''', reply_markup=InlineKeyboardMarkup( 
                    [   
                        [InlineKeyboardButton(text="📄 Lista Con Identifiers 📄", callback_data=f'listaidentifiers')],
                        [InlineKeyboardButton(text="🔙 Indietro 🔙", callback_data=f'gestioneplayerhome')],
                    ]
                )) #listaplayers

@Client.on_callback_query(filters.regex("listaidentifiers"))
async def listaidentifiers(client, query):
    await query.answer("🔄 Caricamento") 
    players =  requests.get(f'http://{ip}/players.json', timeout=5)
    getplayers = players.json()
    playerlist = ''
    for player in getplayers: #player['id'] #player['name'] #player['identifiers']
        playerlist = f'''[<code>{player['id']}</code>] {player['name']} <code>{player['identifiers']}</code>\n'''
    await query.message.edit(f'''**📄 Lista Players 📄**

{playerlist}''', reply_markup=InlineKeyboardMarkup( 
                    [   
                        [InlineKeyboardButton(text="🔙 Indietro 🔙", callback_data=f'gestioneplayerhome')],
                    ]
                ))

@Client.on_message(filters.incoming & filters.text & filters.private)
async def ricevimess(client, message):
    if message.from_user.id in chatrisorse:
        risorsa = message.text
        await message.reply(f'**🛠 Stai gestendo la risorsa** <code>{risorsa}</code>', reply_markup=InlineKeyboardMarkup( 
                    [
                        [InlineKeyboardButton(text="✅ Avvia risorsa", callback_data=f'avvia_{risorsa}'), InlineKeyboardButton(text="Stoppa risorsa❌", callback_data=f'stoppa_{risorsa}')],
                        [InlineKeyboardButton(text="🔄 Riavvia risorsa", callback_data=f'riavvia_{risorsa}')],
                        [InlineKeyboardButton(text="🏡 Home 🏡", callback_data=f'startcb')],
                    ]
                ))

@Client.on_callback_query(filters.regex("stoppa"))
async def cbstop(client, query):
    resource = query.data.split('_')[1:2]
    await query.answer("🔄 Caricamento") 
    fallo(f"stop {resource[0]}")
    await query.message.edit(f'**❌ Risorsa **<code>{resource[0]}</code> **stoppata**')

@Client.on_callback_query(filters.regex("refresh"))
async def cbrefresh(client, query):
    resource = query.data.split('_')[1:2]
    await query.message.edit("🔄 Caricamento") 
    fallo(f"refresh")
    await gestiscirisorsehome(client, query)

@Client.on_callback_query(filters.regex("riavvia"))
async def cbrestart(client, query):
    resource = query.data.split('_')[1:2]
    await query.answer("🔄 Caricamento") 
    fallo(f"restart {resource[0]}")
    await query.message.edit(f'**🔄 Risorsa **<code>{resource[0]}</code> **restartata**')

@Client.on_callback_query(filters.regex("avvia"))
async def cbavvia(client, query):
    resource = query.data.split('_')[1:2]
    await query.answer("🔄 Caricamento") 
    fallo(f"start {resource[0]}")
    await query.message.edit(f'**✅ Risorsa **<code>{resource[0]}</code> **startata**')


@Client.on_message(filters.command("avviarisorsa") & filters.private)
async def cmdavviarisorsa(client, message):
    resource = message.command[1] 
    fallo(f"start {resource}")
    await message.reply(f'Risorsa {resource} avviata')

@Client.on_message(filters.command("stoprisorsa") & filters.private)
async def cmdrisorsastop(client, message):
    resource = message.command[1] 
    fallo(f"stop {resource}")
    await message.reply(f'Risorsa {resource} stoppata')