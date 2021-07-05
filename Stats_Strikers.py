## BIBLIOTECAS

import requests
import psycopg2
from bs4 import BeautifulSoup as soup

## BANCO DE DADOS

conn = psycopg2.connect(database = 'projeto_integrado' , user = 'postgres' , password = '123' )
cur = conn.cursor()

## FUNÇÕES
def Data_Format (lista):

    del(lista [0])
    del(lista [6:11])
    del(lista [8:])
    
def Replace_Float(lista, lista_nova):
    for i in lista:
        z = i.replace(",",".")
        lista_nova.append(float(z))

# REQUESTS / BEAUTIFULSOUP
url = 'https://fbref.com/pt/stathead/player_comparison.cgi?request=1&sum=0&comp_type=spec&dom_lg=1&spec_comps=8&player_id1=1f44ac21&p1yrfrom=2020-2021&player_id2=42fd9c7f&p2yrfrom=2020-2021&player_id3=a1d5bd30&p3yrfrom=2020-2021&player_id4=69384e5d&p4yrfrom=2020-2021&player_id5=04e17fd5&p5yrfrom=2020-2021&player_id6=e342ad68&p6yrfrom=2020-2021&player_id7=129af0db&p7yrfrom=2020-2021'

r = requests.get(url)

soup = soup(r.text, 'html.parser')

league_table = soup.find('table', class_ = 'min_width per_g_toggle sortable stats_table min_width shade_zero')

# LISTAS DE MANIPULAÇÃO
Headers = [] # Titulos da coluna
Jogadores_Artilheiros = [] # Lista com nome dos artilheiros
Teams_Strikers = [] # Times dos artilheiros
Data_Strikers = [] # Dados dos artilheiros
Position_Players = [] # Posição dos jogadores
# ENCONTRANDO OS ELEMENTOS

# LISTA DE JOGADORES
for content in league_table.find_all('tbody'):
    access_tr_1 = content.find_all('tr')
    for value in access_tr_1:
        players_list =  value.find('th', class_ = 'left').text
        Jogadores_Artilheiros.append(players_list)
        
# DADOS 
for content in league_table.find_all('tbody'): # Encontrar o tbody (estrutura todo conteúdo da tabela 'corpo')
    access_tr_2 = content.find_all('tr')  # Encontrar todos os tr
    for content_ in access_tr_2:
        access_td = content_.find_all('td', class_ = 'right') # Especificar div e a classe
        for value in access_td:
            header_table = ((value.get('data-stat'))) # header da tabela
            value_table = (value.get_text()) # valor
            Data_Strikers.append(value_table) 
            Headers.append(header_table)
# EQUIPE
for content in league_table.find_all('tbody'): # Encontrar o tbody (estrutura todo conteúdo da tabela 'corpo')
    access_tr_3 = content.find_all('tr')  # Encontrar todos os tr
    for content_ in access_tr_3:
        access_td = content_.find_all('td', class_ = 'left') # Especificar div e a classe
        for value in access_td:
            y = (value.get_text()) # valor
            Teams_Strikers.append(y)

Teams_Strikers = Teams_Strikers[1::2]              

Teams_Strikers[0] = 'Borussia Dortmund'
Teams_Strikers[1] = 'Paris Saint Germain'
Teams_Strikers[3] = 'Paris Saint Germain'

# POSIÇÃO
for content in league_table.find_all('tbody'): # Encontrar o tbody (estrutura todo conteúdo da tabela 'corpo')
    access_tr_4 = content.find_all('tr')  # Encontrar todos os tr
    for content_ in access_tr_4:
        access_td = content_.find_all('td', class_ = 'center') # Especificar div e a classe
        for value in access_td:
            p = (value.get_text()) # valor
            Position_Players.append(p)

# DELIMITANDO DADOS NAS LISTAS
Data_Striker_1 = Data_Strikers[0:26]
Data_Striker_2 = Data_Strikers[26:52]
Data_Striker_3 = Data_Strikers[52:78]
Data_Striker_4 = Data_Strikers[78:104]
Data_Striker_5 = Data_Strikers[104:130]
Data_Striker_6 = Data_Strikers[130:156]

# Objetivos : games - games_start - minutes - minutes_90s - goals - assists - goals_90 - assists_90
Headers = Headers[:26]
# UTILIZAÇÃO DA FUNÇÃO DE FORMATAÇÃO DE LISTAS
Data_Format(Headers)
Data_Format(Data_Striker_1)
Data_Format(Data_Striker_2)
Data_Format(Data_Striker_3)
Data_Format(Data_Striker_4)
Data_Format(Data_Striker_5)
Data_Format(Data_Striker_6)

# DADOS FORMATADOS DE CADA ARTILHEIRO
Data_Striker_Format_1 = [] 
Data_Striker_Format_2 = [] 
Data_Striker_Format_3 = [] 
Data_Striker_Format_4 = [] 
Data_Striker_Format_5 = [] 
Data_Striker_Format_6 = [] 

Replace_Float(Data_Striker_1, Data_Striker_Format_1)
Replace_Float(Data_Striker_2, Data_Striker_Format_2)
Replace_Float(Data_Striker_3, Data_Striker_Format_3)
Replace_Float(Data_Striker_4, Data_Striker_Format_4)
Replace_Float(Data_Striker_5, Data_Striker_Format_5)
Replace_Float(Data_Striker_6, Data_Striker_Format_6)

##### INSERÇÃO NO BANCO DE DADOS POSTGRES #####


# INSERÇÃO ARTILHEIROS
cur.execute("""INSERT INTO Stats_UCL_ATK_MID (player, team, position_player, games, games_starts, minutes, minutes_90s, goals,assists, goals_per90, assists_per90) VALUES(%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Jogadores_Artilheiros[0],Teams_Strikers[0],Position_Players[0], Data_Striker_Format_1[0], Data_Striker_Format_1[1], Data_Striker_Format_1[2], Data_Striker_Format_1[3], Data_Striker_Format_1[4], Data_Striker_Format_1[5],Data_Striker_Format_1[6], Data_Striker_Format_1[7]))

cur.execute("""INSERT INTO Stats_UCL_ATK_MID (player, team, position_player, games, games_starts, minutes, minutes_90s, goals,assists, goals_per90, assists_per90) VALUES(%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Jogadores_Artilheiros[1],Teams_Strikers[1],Position_Players[1], Data_Striker_Format_2[0], Data_Striker_Format_2[1], Data_Striker_Format_2[2], Data_Striker_Format_2[3], Data_Striker_Format_2[4], Data_Striker_Format_2[5],Data_Striker_Format_2[6], Data_Striker_Format_2[7]))

cur.execute("""INSERT INTO Stats_UCL_ATK_MID (player, team, position_player, games, games_starts, minutes, minutes_90s, goals,assists, goals_per90, assists_per90) VALUES(%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Jogadores_Artilheiros[2],Teams_Strikers[2],Position_Players[2], Data_Striker_Format_3[0], Data_Striker_Format_3[1], Data_Striker_Format_3[2], Data_Striker_Format_3[3], Data_Striker_Format_3[4], Data_Striker_Format_3[5],Data_Striker_Format_3[6], Data_Striker_Format_3[7]))

cur.execute("""INSERT INTO Stats_UCL_ATK_MID (player, team, position_player, games, games_starts, minutes, minutes_90s, goals,assists, goals_per90, assists_per90) VALUES(%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Jogadores_Artilheiros[3],Teams_Strikers[3],Position_Players[3], Data_Striker_Format_4[0], Data_Striker_Format_4[1], Data_Striker_Format_4[2], Data_Striker_Format_4[3], Data_Striker_Format_4[4], Data_Striker_Format_4[5],Data_Striker_Format_4[6], Data_Striker_Format_4[7]))

cur.execute("""INSERT INTO Stats_UCL_ATK_MID (player, team, position_player, games, games_starts, minutes, minutes_90s, goals,assists, goals_per90, assists_per90) VALUES(%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Jogadores_Artilheiros[4],Teams_Strikers[4],Position_Players[4], Data_Striker_Format_5[0], Data_Striker_Format_5[1], Data_Striker_Format_5[2], Data_Striker_Format_5[3], Data_Striker_Format_5[4], Data_Striker_Format_5[5],Data_Striker_Format_5[6], Data_Striker_Format_5[7]))

cur.execute("""INSERT INTO Stats_UCL_ATK_MID (player, team, position_player, games, games_starts, minutes, minutes_90s, goals,assists, goals_per90, assists_per90) VALUES(%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Jogadores_Artilheiros[5],Teams_Strikers[5],Position_Players[5], Data_Striker_Format_6[0], Data_Striker_Format_6[1], Data_Striker_Format_6[2], Data_Striker_Format_6[3], Data_Striker_Format_6[4], Data_Striker_Format_6[5],Data_Striker_Format_6[6], Data_Striker_Format_6[7]))

conn.commit()