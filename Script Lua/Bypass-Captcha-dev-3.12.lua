local sampev = require 'lib.samp.events'
local memory = require "memory"
script_properties("work-in-pause")

function main()
    while not isSampAvailable() do wait(0) end
    if not isSampLoaded() or not isSampfuncsLoaded() then return end

    sampRegisterChatCommand('bc', ativacao)
    sampRegisterChatCommand('infobc', infobc)

    while true do wait(0)
        if status then
            verificarCaptcha()
        end
    end
end

function infobc()
    if(infobc) then
        sampShowDialog(2004, "ÍNDICE DE INFORMAÇÕES", [[
    {01A9DB}INFORMAÇÕES:
    {FFFFFF} - Digite no chat {01DF01}'/bc'{FFFFFF} Para ativar/desativar o Bypass Captcha!

    {ff9900}RECOMENDAÇÕES:
    {FFFFFF} - Utilize com moderação para não levantar suspeitas.

    {FFFFFF} - Não abandone o jogo.

    {FFFFFF} - Se movimente eventualmente, se mostre presente, deste modo não é
    necessário se preocupar em receber alguma punição.

    {ff0000}ATENÇÃO:
    {FFFFFF} - Tenha ciência que essa não é uma versão completa, é a versão de lançamento
    aberta ao público por tempo indeterminado, podendo ser prolongada posteriormente. Foi 
    adicionado alguns recursos essenciais para tornar a utilização mais segura,
    entretanto como mencionado anteriormente, não é uma versão finalizada.

    {FFFFFF} - Terminantemente proibido adulterar o nome do script.

    Tem alguma dúvida ou sugestão? Utilize os contatos abaixo:
    {01DF01}Discord: {ffffff}MarzipanFX01#8254
    {01DF01}E-Mail: {ffffff}marzipanfx01@hotmail.com.br
    {01DF01}Canal do YouTube: {ffffff}MarzipanFX01
    
    {01DF01}Versão: {FFFFFF}Standard Edition 3.12
    {01DF01}Vencimento: {FFFFFF}N/A
    {01DF01}Licença p/: {FFFFFF}N/A

    Desenvolvido por {01DF01}MarzipanFX01{FFFFFF}
    Todos os direitos reservados.
    ]], "{FFFFFF}Fechar", "", 0)
    end
end

function verificarCaptcha()
    result = sampTextdrawIsExists(2135)
    if result == true then
        wait(1000)
        normalizarTextdraws()
        salvarCoordenadas()

            sampAddChatMessage("{eb4000}| AVISO | Normalizando digitos do CAPTCHA, aguarde...", 0xeb4000)
            wait(1000)
            sampAddChatMessage("{eb4000}| AVISO | Salvando as coordenadas...", 0xeb4000)

        openCaptchaPrevision()

            sampAddChatMessage("{eb4000}| AVISO | Segmentando digitos...", 0xeb4000)
            wait(4000)
            sampAddChatMessage("{eb4000}| AVISO | Prevendo dígitos do CAPTCHA, aguarde...", 0xeb4000)

        tirarPrint()

            wait(10000)
    end
end

function tirarPrint()
    setVirtualKeyDown(0x7B, true) -- F12 tirar print
    wait(300)
    sampSetChatInputEnabled(true)
    sampSetChatInputText('/sairafk ')
    wait(1000)
    setVirtualKeyDown(0x0D, true)
    wait(100) -- Enter
    setVirtualKeyDown(0x0D, false)
end

function normalizarTextdraws()
    for i = 2137, 2154 do
        
        local exists = sampTextdrawIsExists(i)
        
        if exists then
            posX, posY = sampTextdrawGetPos(i)   
            local box, color, sizeX, sizeY = sampTextdrawGetBoxEnabledColorAndSize(i)
            
            if sizeX >= sizeY then
                sampTextdrawSetBoxColorAndSize(i, box, color, sizeX, 5)
            else
                sampTextdrawSetBoxColorAndSize(i, box, color, 5, sizeY)
            end
        end
    end
end

function salvarCoordenadas()
    x, y = sampTextdrawGetPos(2135) --Pegamos a posição. O valor retorna nas coords do jogo
    x1, y1 = convertGameScreenCoordsToWindowScreenCoords(x, y)
    local arquivo_path = "C:\\Users\\Administrador\\Downloads\\Download Completo\\GTA San Andreas\\GTA San Andreas\\moonloader\\Python\\Bypass Captcha-3.12-dev\\Treinar Modelo\\coordenadas.txt"

    -- Abrir o arquivo no modo de escrita
    local arquivo = io.open(arquivo_path, "w")

    -- Verificar se o arquivo foi aberto corretamente
    if arquivo then
        -- Escrever no arquivo
        arquivo:write("x="..x1.."\n") --Eixo X
        arquivo:write("y="..y1.."\n") --Eixo Y
        arquivo:write("w=375\n") --Largura
        arquivo:rite("h=220\n") --Altura
        
        -- Fechar o arquivo
        arquivo:close()
    else
        print("Erro ao abrir o arquivo para escrita.")
    end
end

function ativacao()
    status = not status

    if status then
        sampAddChatMessage("{32cd32}| INFO |{ffffff} Bypass CAPTCHA Ver. 3.12 {32cd32}ativado{ffffff} com sucesso!", 0x32cd32)
    else
        sampAddChatMessage("{32cd32}| INFO |{ffffff} Bypass CAPTCHA Ver. 3.12  {eb4000}desativado{ffffff} com sucesso!", 0x32cd32)
    end
end

function openCaptchaPrevision()
    local batchFilePath = "C:\\Users\\Administrador\\Downloads\\Download Completo\\GTA San Andreas\\GTA San Andreas\\moonloader\\Python\\Bypass Captcha-3.12-dev\\Treinar Modelo\\executar.bat"
    
    -- Formatar o comando para abrir minimizado
    local command = string.format('start /min "" "%s"', batchFilePath)
    
    -- Executar o comando
    os.execute(command)
end

function start()
    writeMemory(7634870, 1, 1, 1)
    writeMemory(7635034, 1, 1, 1)
    memory.fill(7623723, 144, 8)
    memory.fill(5499528, 144, 6)
end