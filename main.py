from pyrogram import Client 


ip = 'localhost:30120' #if localhost write localhost:port else ip:port
app = Client(
    './sessioni/sessione', 
    api_id = 123,                                                                          #my.telegram.org
    api_hash = "12ab3",                                                                    #my.telegram.org
    bot_token = "123:abc",					                           #@botfather
    plugins = dict(root="plugins")
)

if __name__ == "__main__":
    app.run(print('Telegram Bot Started || github.com/itsmat - Mat#3616'))



