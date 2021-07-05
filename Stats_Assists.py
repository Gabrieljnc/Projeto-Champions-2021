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
    

# REQUESTS / BEAUTIFULSOUP
url = 'https://fbref.com/en/stathead/player_comparison.cgi?request=1&sum=0&comp_type=spec&dom_lg=1&spec_comps=8&player_id1=0ab1f153&p1yrfrom=2020-2021&player_id2=19cda00b&p2yrfrom=2020-2021&player_id3=e46012d4&p3yrfrom=2020-2021&player_id4=49296448&p4yrfrom=2020-2021&player_id5=dbf053da&p5yrfrom=2020-2021&player_id6=2475dcc6&p6yrfrom=2020-2021&player_id7=30941e96&p7yrfrom=2020-2021'

r = requests.get(url)

soup = soup(r.text, 'html.parser')

league_table = soup.find('table', class_ = 'min_width per_g_toggle sortable stats_table min_width shade_zero')

# LISTAS DE MANIPULAÇÃO
Headers = [] # Titulos da coluna
Jogadores_Assists = [] # Lista com nome dos artilheiros
Teams_Assists = [] # Times dos artilheiros
Data_Assists = [] # Dados dos artilheiros
Position_Players = [] # Posição dos jogadores
# ENCONTRANDO OS ELEMENTOS

# LISTA DE JOGADORES
for content in league_table.find_all('tbody'):
    access_tr_1 = content.find_all('tr')
    for value in access_tr_1:
        players_list =  value.find('th', class_ = 'left').text
        Jogadores_Assists.append(players_list)
        
# DADOS 
for content in league_table.find_all('tbody'): # Encontrar o tbody (estrutura todo conteúdo da tabela 'corpo')
    access_tr_2 = content.find_all('tr')  # Encontrar todos os tr
    for content_ in access_tr_2:
        access_td = content_.find_all('td', class_ = 'right') # Especificar div e a classe
        for value in access_td:
            header_table = ((value.get('data-stat'))) # header da tabela
            value_table = (value.get_text()) # valor
            Data_Assists.append(value_table) 
            Headers.append(header_table)

# EQUIPE
for content in league_table.find_all('tbody'): # Encontrar o tbody (estrutura todo conteúdo da tabela 'corpo')
    access_tr_3 = content.find_all('tr')  # Encontrar todos os tr
    for content_ in access_tr_3:
        access_td = content_.find_all('td', class_ = 'left') # Especificar div e a classe
        for value in access_td:
            y = (value.get_text()) # valor
            Teams_Assists.append(y)

Teams_Assists = Teams_Assists[1::2] 
Teams_Assists[1] = 'Paris Saint Germain'
Teams_Assists[4] = 'Borussia Dortmund'
 
# POSIÇÃO

for content in league_table.find_all('tbody'): # Encontrar o tbody (estrutura todo conteúdo da tabela 'corpo')
    access_tr_4 = content.find_all('tr')  # Encontrar todos os tr
    for content_ in access_tr_4:
        access_td = content_.find_all('td', class_ = 'center') # Especificar div e a classe
        for value in access_td:
            p = (value.get_text()) # valor
            Position_Players.append(p)

# DELIMITANDO DADOS NAS LISTAS ( JOGADOR POR JOGADOR )
Data_Assists_1 = Data_Assists[0:26]
Data_Assists_2 = Data_Assists[26:52]
Data_Assists_3 = Data_Assists[52:78]
Data_Assists_4 = Data_Assists[78:104]
Data_Assists_5 = Data_Assists[104:130]
Data_Assists_6 = Data_Assists[130:156]

# Objetivos : games - games_start - minutes - minutes_90s - goals - assists - goals_90 - assists_90
Headers = Headers[:26]
# UTILIZAÇÃO DA FUNÇÃO DE FORMATAÇÃO DE LISTAS
Data_Format(Headers)
Data_Format(Data_Assists_1)
Data_Format(Data_Assists_2)
Data_Format(Data_Assists_3)
Data_Format(Data_Assists_4)
Data_Format(Data_Assists_5)
Data_Format(Data_Assists_6)

##### INSERÇÃO NO BANCO DE DADOS POSTGRES #####

cur.execute("""INSERT INTO Stats_UCL_ATK_MID (player, team, position_player, games, games_starts, minutes, minutes_90s, goals,assists, goals_per90, assists_per90) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Jogadores_Assists[0],Teams_Assists[0], Position_Players[0], Data_Assists_1[0], Data_Assists_1[1], Data_Assists_1[2], Data_Assists_1[3], Data_Assists_1[4], Data_Assists_1[5],Data_Assists_1[6], Data_Assists_1[7]))

cur.execute("""INSERT INTO Stats_UCL_ATK_MID (player, team, position_player, games, games_starts, minutes, minutes_90s, goals,assists, goals_per90, assists_per90) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Jogadores_Assists[1],Teams_Assists[1], Position_Players[1], Data_Assists_2[0], Data_Assists_2[1], Data_Assists_2[2], Data_Assists_2[3], Data_Assists_2[4], Data_Assists_2[5],Data_Assists_2[6], Data_Assists_2[7]))

cur.execute("""INSERT INTO Stats_UCL_ATK_MID (player, team, position_player, games, games_starts, minutes, minutes_90s, goals,assists, goals_per90, assists_per90) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Jogadores_Assists[2],Teams_Assists[2], Position_Players[2], Data_Assists_3[0], Data_Assists_3[1], Data_Assists_3[2], Data_Assists_3[3], Data_Assists_3[4], Data_Assists_3[5],Data_Assists_3[6], Data_Assists_3[7]))

cur.execute("""INSERT INTO Stats_UCL_ATK_MID (player, team, position_player, games, games_starts, minutes, minutes_90s, goals,assists, goals_per90, assists_per90) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Jogadores_Assists[3],Teams_Assists[3], Position_Players[3], Data_Assists_4[0], Data_Assists_4[1], Data_Assists_4[2], Data_Assists_4[3], Data_Assists_4[4], Data_Assists_4[5],Data_Assists_4[6], Data_Assists_4[7]))

cur.execute("""INSERT INTO Stats_UCL_ATK_MID (player, team, position_player, games, games_starts, minutes, minutes_90s, goals,assists, goals_per90, assists_per90) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Jogadores_Assists[4],Teams_Assists[4], Position_Players[4], Data_Assists_5[0], Data_Assists_5[1], Data_Assists_5[2], Data_Assists_5[3], Data_Assists_5[4], Data_Assists_5[5],Data_Assists_5[6], Data_Assists_5[7]))

cur.execute("""INSERT INTO Stats_UCL_ATK_MID (player, team, position_player, games, games_starts, minutes, minutes_90s, goals,assists, goals_per90, assists_per90) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Jogadores_Assists[5],Teams_Assists[5], Position_Players[5], Data_Assists_6[0], Data_Assists_6[1], Data_Assists_6[2], Data_Assists_6[3], Data_Assists_6[4], Data_Assists_6[5],Data_Assists_6[6], Data_Assists_6[7]))

conn.commit()