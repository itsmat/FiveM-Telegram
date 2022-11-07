local dati
print('^5[FiveM-Telegram] ^1Script Started | https://github.com/itsmat/FiveM-Telegram^0')

if GetCurrentResourceName() ~= "FiveM-Telegram" then
    print('^5[FiveM-Telegram] ^1Rinomina la risorsa come "FiveM-Telegram" per farla funzionare al meglio.^0')
end

-- controllo versione
CreateThread( function()
	local versionefilefx = GetResourceMetadata(GetCurrentResourceName(), 'version')
	PerformHttpRequest('https://raw.githubusercontent.com/itsmat/FiveM-Telegram/Nuker-Tool/versione.json', function(code, res, headers)
		if code == 200 then
			local filegithub = json.decode(res)
            --print(filegithub.versione)     -- file github
            --print(versionefilefx)          -- versione presente nell'fx manifest
			if filegithub.versione ~= versionefilefx then
					print(([[^5[FiveM-Telegram] ^1La versione non è aggiornata.
Versione Attuale: ^2%s^1
Nuova Versione: ^2%s^1
Updates: ^2%s^0]]):format(versionefilefx, filegithub.versione, filegithub.changelog))
			end
		else
			print('^5[FiveM-Telegram] ^1Errore: Errore nel controllo della versione^0')
		end
	end, 'GET')
end)


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

