import os
import platform
import socket
import psutil
import json
import subprocess

def coletar_informacoes_basicas():
    try:
        # Informações gerais
        hostname = socket.gethostname()
        sistema = platform.system()
        versao_sistema = platform.version()
        arquitetura = platform.architecture()[0]
        processador = platform.processor()

        # CPU e memória
        num_nucleos = psutil.cpu_count(logical=True)
        memoria_total = round(psutil.virtual_memory().total / (1024 ** 3), 2)  # em GB

        # Disco
        disco = psutil.disk_usage('/')
        espaco_total = round(disco.total / (1024 ** 3), 2)  # em GB
        espaco_usado = round(disco.used / (1024 ** 3), 2)  # em GB

        # IP
        ip_address = socket.gethostbyname(hostname)

        return {
            "Hostname": hostname,
            "Sistema Operacional": sistema,
            "Versão do Sistema": versao_sistema,
            "Arquitetura": arquitetura,
            "Processador": processador,
            "Núcleos CPU": num_nucleos,
            "Memória Total (GB)": memoria_total,
            "Espaço Total no Disco (GB)": espaco_total,
            "Espaço Usado no Disco (GB)": espaco_usado,
            "Endereço IP": ip_address,
        }
    except Exception as e:
        return {"Erro": str(e)}

def coletar_aplicativos_instalados():
    aplicativos = []
    sistema = platform.system()

    try:
        if sistema == "Windows":
            # Comando PowerShell para listar programas instalados
            cmd = 'powershell "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName"'
            result = subprocess.check_output(cmd, shell=True, text=True)
            for line in result.splitlines():
                if line.strip():
                    aplicativos.append(line.strip())
        elif sistema == "Linux":
            # Listar pacotes instalados em distribuições baseadas em Debian
            result = subprocess.check_output("dpkg --get-selections", shell=True, text=True)
            for line in result.splitlines():
                aplicativos.append(line.split('\t')[0])
    except Exception as e:
        aplicativos.append(f"Erro ao coletar aplicativos: {str(e)}")

    return aplicativos

def coletar_memorias_ram():
    memoria_info = []
    sistema = platform.system()

    try:
        if sistema == "Linux":
            # Extrair informações de /proc/meminfo
            cmd = "dmidecode --type memory"
            result = subprocess.check_output(cmd, shell=True, text=True)
            for line in result.splitlines():
                if "Size:" in line and "No Module Installed" not in line:
                    memoria_info.append(line.strip())
        elif sistema == "Windows":
            # Usar WMI no Windows
            cmd = 'powershell "Get-WmiObject Win32_PhysicalMemory | Select-Object Capacity"'
            result = subprocess.check_output(cmd, shell=True, text=True)
            for line in result.splitlines():
                if line.strip().isdigit():
                    tamanho_gb = int(line.strip()) / (1024 ** 3)
                    memoria_info.append(f"{round(tamanho_gb, 2)} GB")
    except Exception as e:
        memoria_info.append(f"Erro ao coletar memória RAM: {str(e)}")

    return memoria_info

def salvar_inventario(inventario, arquivo="inventario_completo.json"):
    with open(arquivo, 'w') as f:
        json.dump(inventario, f, indent=4)

if __name__ == "__main__":
    inventario = coletar_informacoes_basicas()
    inventario["Aplicativos Instalados"] = coletar_aplicativos_instalados()
    inventario["Memórias RAM"] = coletar_memorias_ram()

    salvar_inventario(inventario)
    print("Inventário completo salvo em 'inventario_completo.json'.")
