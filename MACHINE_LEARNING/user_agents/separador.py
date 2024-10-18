import re

# Função para classificar os user-agents por navegador e sistema operacional
def classificar_user_agents(user_agents):
    chrome_windows_agents = []
    chrome_linux_agents = []
    chrome_mac_agents = []
    
    firefox_windows_agents = []
    firefox_linux_agents = []
    firefox_mac_agents = []
    
    safari_windows_agents = []
    safari_linux_agents = []
    safari_mac_agents = []

    for agent in user_agents:
        if 'Chrome' in agent or 'Chromium' in agent:
            if re.search(r'Windows NT', agent):
                chrome_windows_agents.append(agent)
            elif re.search(r'X11; Linux', agent):
                chrome_linux_agents.append(agent)
            elif re.search(r'Macintosh', agent):
                chrome_mac_agents.append(agent)
        elif 'Firefox' in agent:
            if re.search(r'Windows NT', agent):
                firefox_windows_agents.append(agent)
            elif re.search(r'X11; Linux', agent):
                firefox_linux_agents.append(agent)
            elif re.search(r'Macintosh', agent):
                firefox_mac_agents.append(agent)
        elif 'Safari' in agent and 'Version' in agent:
            if re.search(r'Windows NT', agent):
                safari_windows_agents.append(agent)
            elif re.search(r'X11; Linux', agent):
                safari_linux_agents.append(agent)
            elif re.search(r'Macintosh', agent):
                safari_mac_agents.append(agent)
    
    return (
        chrome_windows_agents, chrome_linux_agents, chrome_mac_agents,
        firefox_windows_agents, firefox_linux_agents, firefox_mac_agents,
        safari_windows_agents, safari_linux_agents, safari_mac_agents
    )

# Leitura do arquivo de user-agents
with open("./user_agents/user-agent.txt", mode="r") as f:
    file_content = f.read()

# Quebra os user-agents por linha
user_agents = file_content.splitlines()

# Classifica os user-agents
(
    chrome_windows_agents, chrome_linux_agents, chrome_mac_agents,
    firefox_windows_agents, firefox_linux_agents, firefox_mac_agents,
    safari_windows_agents, safari_linux_agents, safari_mac_agents
) = classificar_user_agents(user_agents)

# Função para escrever os user-agents em arquivos separados
def escrever_user_agents_em_arquivos(
    chrome_windows_agents, chrome_linux_agents, chrome_mac_agents,
    firefox_windows_agents, firefox_linux_agents, firefox_mac_agents,
    safari_windows_agents, safari_linux_agents, safari_mac_agents
):
    with open("./user_agents/chrome/chrome_windows_agents.txt", mode="w") as f:
        f.write("\n".join(chrome_windows_agents))
    
    with open("./user_agents/chrome/chrome_linux_agents.txt", mode="w") as f:
        f.write("\n".join(chrome_linux_agents))
    
    with open("./user_agents/chrome/chrome_mac_agents.txt", mode="w") as f:
        f.write("\n".join(chrome_mac_agents))
    
    with open("./user_agents/firefox/firefox_windows_agents.txt", mode="w") as f:
        f.write("\n".join(firefox_windows_agents))
    
    with open("./user_agents/firefox/firefox_linux_agents.txt", mode="w") as f:
        f.write("\n".join(firefox_linux_agents))
    
    with open("./user_agents/firefox/firefox_mac_agents.txt", mode="w") as f:
        f.write("\n".join(firefox_mac_agents))
    
    with open("./user_agents/safari/safari_windows_agents.txt", mode="w") as f:
        f.write("\n".join(safari_windows_agents))
    
    with open("./user_agents/safari/safari_linux_agents.txt", mode="w") as f:
        f.write("\n".join(safari_linux_agents))
    
    with open("./user_agents/safari/safari_mac_agents.txt", mode="w") as f:
        f.write("\n".join(safari_mac_agents))

# Escreve os user-agents nos arquivos
escrever_user_agents_em_arquivos(
    chrome_windows_agents, chrome_linux_agents, chrome_mac_agents,
    firefox_windows_agents, firefox_linux_agents, firefox_mac_agents,
    safari_windows_agents, safari_linux_agents, safari_mac_agents
)

print("User-agents foram classificados e salvos em arquivos separados.")
