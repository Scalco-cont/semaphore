import pyautogui
import time
import os
import pygetwindow as gw

# 🖥️ Abre o Paint (caso não esteja aberto)
if not any('Paint' in window for window in gw.getAllTitles()):
    os.system("start mspaint")
    time.sleep(3)  # Espera para garantir que o Paint abra

# 🪟 Garante que o Paint está ativo
paint_window = None
for window in gw.getWindowsWithTitle('Paint'):
    paint_window = window
    break

if paint_window:
    paint_window.activate()
    time.sleep(1)
else:
    print("❌ Não foi possível encontrar a janela do Paint.")
    exit(1)

# 🔄 Maximiza a janela
pyautogui.hotkey('alt', 'space')
pyautogui.press('x')
time.sleep(1)

# 🎯 Coordenadas ajustáveis
TOOL_ELLIPSE = (100, 70)  # Ferramenta Elipse (ajuste para sua tela)
TOOL_LINE = (130, 70)     # Ferramenta Linha (ajuste para sua tela)

CIRCLE_OUTER_START = (400, 300)
CIRCLE_OUTER_END = (600, 500)

CIRCLE_INNER_START = (460, 360)
CIRCLE_INNER_END = (540, 440)

LINES = [
    ((500, 300), (500, 500)),  # Vertical
    ((400, 400), (600, 400)),  # Horizontal
    ((420, 320), (580, 480)),  # Diagonal 1
    ((580, 320), (420, 480))   # Diagonal 2
]

# 🛠️ Seleciona ferramenta Elipse
pyautogui.click(*TOOL_ELLIPSE)
time.sleep(1)

# 🖌️ Desenha círculo externo
pyautogui.moveTo(*CIRCLE_OUTER_START)
pyautogui.mouseDown()
pyautogui.moveTo(*CIRCLE_OUTER_END)
pyautogui.mouseUp()
time.sleep(1)

# 🖌️ Desenha círculo interno
pyautogui.click(*TOOL_ELLIPSE)
time.sleep(1)
pyautogui.moveTo(*CIRCLE_INNER_START)
pyautogui.mouseDown()
pyautogui.moveTo(*CIRCLE_INNER_END)
pyautogui.mouseUp()
time.sleep(1)

# 🛠️ Seleciona ferramenta Linha
pyautogui.click(*TOOL_LINE)
time.sleep(1)

# 🖌️ Desenha raios
for start, end in LINES:
    pyautogui.moveTo(*start)
    pyautogui.mouseDown()
    pyautogui.moveTo(*end)
    pyautogui.mouseUp()
    time.sleep(1)

print("✅ Desenho concluído com sucesso no Paint!")
