-- CFG Program Files

local maxw, maxh = term.getSize()
--os.pullEvent = os.pullEventRaw 
 
-- IMPLEMENTAZIONE DEL DRAWFILLEDBOX
local function drawPixelInternal(xPos, yPos)
    term.setCursorPos(xPos, yPos)
    term.write(" ")
end
 
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

function playerCheck(player)
    a = http.get("https://pnrf.rgbcraft.com/api/checkplayer?player="..player)
    b = a.readAll()

    ret
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
        check = playerCheck(player)
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
    end    
    shell.run("rm star2")
    shell.run("pastebin get sg8epUiQ star2")
    shell.run("rm startup")

end
 

sfondo(colors.white)
term.clear()
 

 
titolo("PNRF HUB")
 
-- 51X 19Y
colore(colors.black)
sfondo(colors.white)
 
 
drawFilledBox(15, 11, 35, 13, colors.red) -- FileBox (Consegna Pacco)
 
testo = "Nuove Frequenza"
term.setCursorPos((maxw - #testo) / 2, 12)
term.write(testo)
 
drawFilledBox(42, 16, 48, 18, colors.red) -- FileBox (FAQ)
 
testo = "F.A.Q"
term.setCursorPos(43, 17)
term.write(testo)
 
colore(colors.black)
 
while true do
    colore(colors.black)
    local event, par1, par2, par3 = os.pullEventRaw()
    if par2 >= 15 and par2 <= 35 and par3 >= 11 and par3 <= 13 and event == "mouse_click" then -- New Return
        new_Frequence()
        os.sleep(3)
        os.reboot()
 
    elseif par2 >= 42 and par2 <= 49 and par3 >= 16 and par3 <= 18 and event == "mouse_click"  then -- FAQ
        faq()
        os.reboot()
    end
    print("\n\n ".. event)
end
 
os.sleep(45)
os.reboot()