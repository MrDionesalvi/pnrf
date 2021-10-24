-- CFG Program Files
 
local maxw, maxh = term.getSize()
local printer = peripheral.wrap("back")

os.pullEvent = os.pullEventRaw 
 
-- IMPLEMENTAZIONE DEL DRAWFILLEDBOX
local function drawPixelInternal(xPos, yPos)
    term.setCursorPos(xPos, yPos)
    term.write(" ")
end
 
Gplayer = ""
 
local tColourLookup = {}
for n = 1, 16 do
    tColourLookup[string.byte("0123456789abcdef", n, n)] = 2 ^ (n - 1)
end
 
function drawFilledBox(startX, startY, endX, endY, nColour)
    if type(startX) ~= "number" or type(startX) ~= "number" or type(endX) ~=
        "number" or type(endY) ~= "number" or
        (nColour ~= nil and type(nColour) ~= "number") then
        error("Expected startX, startY, endX, endY, colour", 2)
    end
 
    startX = math.floor(startX)
    startY = math.floor(startY)
    endX = math.floor(endX)
    endY = math.floor(endY)
 
    if nColour then term.setBackgroundColor(nColour) end
    if startX == endX and startY == endY then
        drawPixelInternal(startX, startY)
        return
    end
 
    local minX = math.min(startX, endX)
    if minX == startX then
        minY = startY
        maxX = endX
        maxY = endY
    else
        minY = endY
        maxX = startX
        maxY = startY
    end
 
    for x = minX, maxX do for y = minY, maxY do drawPixelInternal(x, y) end end
end
 
function colore(nome) term.setTextColor(nome) end
 
function sfondo(nome) term.setBackgroundColor(nome) end
 
function fineColore() term.setTextColour(colours.white) end
 
function fineSfondo() term.setBackgroundColour(colours.black) end
 
function titolo(testo)
    drawFilledBox(1, 1, maxw, 1, colors.gray)
    term.setCursorPos((maxw - #testo) / 2, 1)
    colore(colors.white)
    term.write(testo)
    term.setCursorPos(1, 2)
    sfondo(colors.white)
end
 
function clear()
    sfondo(colors.white)
    term.clear()
    term.setCursorPos(1, 1)
end
 
function errore(errore)
    sfondo(colors.red)
    colore(colors.white)
    term.clear()
    term.setCursorPos(1, 1)
    titolo("Errore irreversibile")
    term.setCursorPos(1, 3)
    sfondo(colors.red)
    colore(colors.white)
    term.write(errore)
    print("\n\n\nAttendere qualche secondo...")
    os.sleep(6)
    os.reboot()
end

function print_Page(message)

    if printer.getPaperLevel() == 0 then -- If there is no paper in the printer
      errore("La carta nella stampante è finita!")
    end
    
    if printer.getInkLevel() == 0 then -- If there is no ink in the printer
      error("L'inchiostro nella stampante è finita!")
    end
    
    -- There is paper and ink in the printer, we can now print a page
    
    if printer.newPage() then
      printer.write("Ricevuta PNRF")
      
      printer.setCursorPos(1, 3)
      printer.write("* Frequenza: "..message)

      
      printer.setCursorPos(1, 8)
      printer.write("Grazie per usare PNRF")

      printer.setPageTitle("PNRF - Ricevuta")
      printer.endPage()
    else
      errore("Stampante inceppata!")
    end 
end
 
function make_payment(player, amount)
    clear()
    titolo("PNFR HUB | Pagamento")
    colore(colors.black)
    term.setCursorPos(1,3)
    print("Inserisce le credenziali nPay\nper comprare il pagamento\nPrezzo da pagare: "..amount.." IC")
 
    term.setCursorPos(1,7)
    term.write("Nome utente:")
    term.setCursorPos(1,9)
    term.write("Password:")
 
    term.setCursorPos(14,7)
    username = read()
 
    term.setCursorPos(11,9)
    password = read("*")
 
    a = http.get("https://pnrf.rgbcraft.com/api/do/payments?player="..player.."&username="..username.."&password="..password.."&amount="..amount)
    if a ~= nil and a ~= "" then
        b = a.readAll()
        c = textutils.unserialize(b)
        a.close()
 
        if c['status'] == "OK" then
            clear()
            titolo("PNFR HUB | Pagamento completato")
            sfondo(colors.white)
            colore(colors.black)
            testo = "Frequenza assegnata: "..c['frequency']
            term.setCursorPos((maxw - #testo) / 2, 11)
            term.write(testo)
            print("\n         Stiamo stampando la ricevuta..")
            os.sleep(1)
            print_Page(c['frequency'])
            os.sleep(8)
            os.reboot()
        else
            errore(c['detail'])
        end
    else
        errore("Server non raggiungibile")
    end
    
    os.sleep(5)
 
 
end
 
function new_frequency(player)
    a = http.get("https://pnrf.rgbcraft.com/api/check/newfrequency?player="..player)
    if a ~= nil and a ~= "" then
        b = a.readAll()
        c = textutils.unserialize(b)
        a.close()
 
        if c['status'] == "OK" then
            clear()
            titolo("PNFR HUB | Nuova Frequenza")
            colore(colors.black)
            testo = "Clicca qualsiasi tasto per confermare"
            testo2 = "dovrai pagare: "..c['price']
            testo3 = "Al momento hai ".. c['frequency'].." frequenza/e"
            term.setCursorPos((maxw - #testo) / 2, 10)
            term.write(testo)
            term.setCursorPos((maxw - #testo2) / 2, 11)
            term.write(testo2)
            term.setCursorPos((maxw - #testo3) / 2, 13)
            term.write(testo3)
            os.pullEvent("key")
 
            make_payment(player, c['price'])
 
        elseif c['status'] == "TMF" then
            clear()
            titolo("PNFR HUB | Nuova Frequenza")
            colore(colors.black)
            testo = "Hai troppe frequenze!!, contatatta legoz"
            term.setCursorPos((maxw - #testo) / 2, 11)
            term.write(testo)
            os.sleep(5)
            os.reboot()
        else
            os.reboot()
        end
    else
        errore("Server non raggiungibile")
    end
end
 
function playerCheck(player)
    a = http.get("https://pnrf.rgbcraft.com/api/checkplayer?player="..player)
    if a ~= nil and a ~= "" then
        b = a.readAll()
        c = textutils.unserialize(b)
        a.close()
 
        Gplayer = player
        if c['status'] == "OK" then
            clear()
            titolo("PNFR HUB | Nuova Frequenza")
            colore(colors.black)
            testo = "Sei un nuovo utente!"
            term.setCursorPos((maxw - #testo) / 2, 11)
            term.write(testo)
            os.sleep(1)
            new_frequency(player)
        elseif c['status'] == "NP" then
            clear()
            titolo("PNFR HUB | Nuova Frequenza")
            colore(colors.black)
            testo = "Utente già registrato.. ASPETTA!"
            term.setCursorPos((maxw - #testo) / 2, 11)
            term.write(testo)
            os.sleep(1)
            new_frequency(player)
        else
            os.reboot()
        end
    else
        errore("Server non raggiungibile")
    end
end
 
function new_Frequence()
    clear()
    titolo("PNFR HUB | Nuova Frequenza")
    colore(colors.black)
    testo = "Clicca il sensore posto al lato/sotto"
    term.setCursorPos((maxw - #testo) / 2, 11)
    term.write(testo)
 
    os.startTimer(120)
    local event, player = os.pullEvent()
    if event == "player" then
        playerCheck(player)
    end
end
 
function faq()
    clear()
    titolo("PNFR HUB | F.A.Q")
    colore(colors.black)
    testo = "Work In progress"
    term.setCursorPos((maxw - #testo) / 2, 11)
    term.write(testo)
 
 
    drawFilledBox(43, 16, 48, 18, colors.red) -- FileBox (INFO)
 
    testo = "HOME"
    term.setCursorPos(44, 17)
    term.write(testo)
 
    os.startTimer(120)
    while true do
        local event, par1, par2, par3 = os.pullEventRaw()
        if par2 >= 43 and par2 <= 48 and par3 >= 16 and par3 <= 18 and event == "mouse_click" then -- Home
            os.reboot()
        end
    end
 
end
 
 
function update()
    if not fs.exists(".permaboot") then
        local file fs.open(".permaboot", "w")
        file.writeLine("Permaboooot")
        file.close()
        os.reboot()
    end    
    shell.run("rm startup")
    shell.run("pastebin get sg8epUiQ star")
    shell.run("star")
    shell.run("mv star startup")
 
end
 
update()
 
 
sfondo(colors.white)
term.clear()
 
 
 
titolo("PNRF HUB")
 
-- 51X 19Y
colore(colors.black)
sfondo(colors.white)
 
 
drawFilledBox(15, 11, 35, 13, colors.red) -- FileBox (Consegna Pacco)
 
testo = "Nuova Frequenza"
term.setCursorPos((maxw - #testo) / 2, 12)
term.write(testo)
 
--drawFilledBox(42, 16, 48, 18, colors.red) -- FileBox (FAQ)
 
--testo = "F.A.Q"
--term.setCursorPos(43, 17)
--term.write(testo)
 
colore(colors.black)
 
while true do
    colore(colors.black)
    local event, par1, par2, par3 = os.pullEventRaw()
    if par2 >= 15 and par2 <= 35 and par3 >= 11 and par3 <= 13 and event == "mouse_click" then -- New Return
        new_Frequence()
        os.sleep(3)
        os.reboot()
    --[[
    elseif par2 >= 42 and par2 <= 49 and par3 >= 16 and par3 <= 18 and event == "mouse_click"  then -- FAQ
        faq()
        os.reboot()
    --]]    
    end
end
 
os.sleep(45)
os.reboot()