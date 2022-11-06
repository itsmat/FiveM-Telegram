local dati
print('^5[FiveM-Telegram] ^1Script Started | https://github.com/itsmat/FiveM-Telegram^0')

CreateThread(function()
    while true do
        Wait(1000*3)
        dati = LoadResourceFile(GetCurrentResourceName(), "./richieste.json") 
        if dati then
            dati = json.decode(dati)
        end
        if type(dati) == 'table' then
            SaveResourceFile(GetCurrentResourceName(), 'richieste.json', '')
            for _,i in pairs(dati) do
                ExecuteCommand(i)
            end
        end
    end
end)

