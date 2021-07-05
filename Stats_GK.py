## BIBLIOTECAS

from os import replace
import requests
import psycopg2
from bs4 import BeautifulSoup as soup

## BANCO DE DADOS

conn = psycopg2.connect(database = 'projeto_integrado' , user = 'postgres' , password = '123' )
cur = conn.cursor()

# FUNÇÃO

def Remove_comma (lista, lista2):
    for i in lista:
        z = float(i.replace(",","."))
        lista2.append(z)
    if lista2[2] == 1.08:
        lista2[2] = 1080
        

# REQUESTS / BEAUTIFULSOUP
url = 'https://fbref.com/en/stathead/player_comparison.cgi?request=1&sum=0&comp_type=spec&dom_lg=1&spec_comps=8&player_id1=ecada4fc&p1yrfrom=2020-2021&player_id2=8778c910&p2yrfrom=2020-2021&player_id3=33887998&p3yrfrom=2020-2021&player_id4=853b7c48&p4yrfrom=2020-2021&player_id5=1840e36d&p5yrfrom=2020-2021&player_id6=903b6e8b&p6yrfrom=2020-2021&player_id7=a3b0ed18&p7yrfrom=2020-2021'

r = requests.get(url)

soup = soup(r.text, 'html.parser')

league_table = soup.find('table', class_ = 'min_width per_g_toggle sortable stats_table min_width shade_zero')

# LISTAS DE MANIPULAÇÃO

Headers = [] # Titulos da coluna
Goalkeepers_name = [] # Lista com nome dos artilheiros
Position_Players = [] # Posição dos jogadores
Data_Goalkeepers = [] # Dados dos goleiros
Teams_Goalkeepers = [] # Time dos goleiros

# ENCONTRANDO OS ELEMENTOS

# LISTA DE JOGADORES
for content in league_table.find_all('tbody'):
    access_tr_1 = content.find_all('tr')
    for value in access_tr_1:
        players_list =  value.find('th', class_ = 'left').text
        Goalkeepers_name.append(players_list)

# DADOS 
for content in league_table.find_all('tbody'): # Encontrar o tbody (estrutura todo conteúdo da tabela 'corpo')
    access_tr_2 = content.find_all('tr')  # Encontrar todos os tr
    for content_ in access_tr_2:
        access_td = content_.find_all('td', class_ = 'right') # Especificar div e a classe
        for value in access_td:
            header_table = ((value.get('data-stat'))) # header da tabela
            value_table = (value.get_text()) # valor
            Data_Goalkeepers.append(value_table) 
            Headers.append(header_table)

# EQUIPE
for content in league_table.find_all('tbody'): # Encontrar o tbody (estrutura todo conteúdo da tabela 'corpo')
    access_tr_3 = content.find_all('tr')  # Encontrar todos os tr
    for content_ in access_tr_3:
        access_td = content_.find_all('td', class_ = 'left') # Especificar div e a classe
        for value in access_td:
            y = (value.get_text()) # valor
            Teams_Goalkeepers.append(y)

Teams_Goalkeepers = Teams_Goalkeepers[1::2] 
Teams_Goalkeepers[0] = 'Paris Saint Germain'

# POSIÇÃO
for content in league_table.find_all('tbody'): # Encontrar o tbody (estrutura todo conteúdo da tabela 'corpo')
    access_tr_4 = content.find_all('tr')  # Encontrar todos os tr
    for content_ in access_tr_4:
        access_td = content_.find_all('td', class_ = 'center') # Especificar div e a classe
        for value in access_td:
            p = (value.get_text()) # valor
            Position_Players.append(p)

# DELIMITANDO DADOS NAS LISTAS ( JOGADOR POR JOGADOR )

Data_Goalkeepers_1 = Data_Goalkeepers[1:10]
Data_Goalkeepers_2 = Data_Goalkeepers[21:30]
Data_Goalkeepers_3 = Data_Goalkeepers[41:50]
Data_Goalkeepers_4 = Data_Goalkeepers[61:70]
Data_Goalkeepers_5 = Data_Goalkeepers[81:90]
Data_Goalkeepers_6 = Data_Goalkeepers[101:110]

# OBJETIVO - player - team - position_player - games - start - min - min90 - Goal_against - Goal_against90 - ShotsonTarget - Saves - Saves%

# DADOS FORMATADOS DE CADA ARTILHEIRO
Data_Goalkeeper_Format_1 = [] 
Data_Goalkeeper_Format_2 = [] 
Data_Goalkeeper_Format_3 = [] 
Data_Goalkeeper_Format_4 = [] 
Data_Goalkeeper_Format_5 = [] 
Data_Goalkeeper_Format_6 = [] 

# FUNÇÃO PARA TIRAR A VIRGULA E FORMATAR VALORES DE MINUTOS

Remove_comma (Data_Goalkeepers_1, Data_Goalkeeper_Format_1)
Remove_comma (Data_Goalkeepers_2, Data_Goalkeeper_Format_2)
Remove_comma (Data_Goalkeepers_3, Data_Goalkeeper_Format_3)
Remove_comma (Data_Goalkeepers_4, Data_Goalkeeper_Format_4)
Remove_comma (Data_Goalkeepers_5, Data_Goalkeeper_Format_5)
Remove_comma (Data_Goalkeepers_6, Data_Goalkeeper_Format_6)


##### INSERÇÃO NO BANCO DE DADOS POSTGRES #####

cur.execute("""INSERT INTO Stats_UCL_GK (player, team, position_player, games, games_starts, minutes, minutes_90s, goals_against, goals_against_per90, shots_on_target, saves, saves_percent) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Goalkeepers_name[0],Teams_Goalkeepers[0], Position_Players[0], Data_Goalkeeper_Format_1[0], 
Data_Goalkeeper_Format_1[1], Data_Goalkeeper_Format_1[2], Data_Goalkeeper_Format_1[3], Data_Goalkeeper_Format_1[4], 
Data_Goalkeeper_Format_1[5],Data_Goalkeeper_Format_1[6], Data_Goalkeeper_Format_1[7],Data_Goalkeeper_Format_1[8]))

cur.execute("""INSERT INTO Stats_UCL_GK (player, team, position_player, games, games_starts, minutes, minutes_90s, goals_against, goals_against_per90, shots_on_target, saves, saves_percent) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Goalkeepers_name[1],Teams_Goalkeepers[1], Position_Players[1], Data_Goalkeeper_Format_2[0], 
Data_Goalkeeper_Format_2[1], Data_Goalkeeper_Format_2[2], Data_Goalkeeper_Format_2[3], Data_Goalkeeper_Format_2[4], 
Data_Goalkeeper_Format_2[5],Data_Goalkeeper_Format_2[6], Data_Goalkeeper_Format_2[7],Data_Goalkeeper_Format_2[8]))

cur.execute("""INSERT INTO Stats_UCL_GK (player, team, position_player, games, games_starts, minutes, minutes_90s, goals_against, goals_against_per90, shots_on_target, saves, saves_percent) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Goalkeepers_name[2],Teams_Goalkeepers[2], Position_Players[2], Data_Goalkeeper_Format_3[0], 
Data_Goalkeeper_Format_3[1], Data_Goalkeeper_Format_3[2], Data_Goalkeeper_Format_3[3], Data_Goalkeeper_Format_3[4], 
Data_Goalkeeper_Format_3[5],Data_Goalkeeper_Format_3[6], Data_Goalkeeper_Format_3[7],Data_Goalkeeper_Format_3[8]))

cur.execute("""INSERT INTO Stats_UCL_GK (player, team, position_player, games, games_starts, minutes, minutes_90s, goals_against, goals_against_per90, shots_on_target, saves, saves_percent) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Goalkeepers_name[3],Teams_Goalkeepers[3], Position_Players[3], Data_Goalkeeper_Format_4[0], 
Data_Goalkeeper_Format_4[1], Data_Goalkeeper_Format_4[2], Data_Goalkeeper_Format_4[3], Data_Goalkeeper_Format_4[4], 
Data_Goalkeeper_Format_4[5],Data_Goalkeeper_Format_4[6], Data_Goalkeeper_Format_4[7],Data_Goalkeeper_Format_4[8]))

cur.execute("""INSERT INTO Stats_UCL_GK (player, team, position_player, games, games_starts, minutes, minutes_90s, goals_against, goals_against_per90, shots_on_target, saves, saves_percent) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Goalkeepers_name[4],Teams_Goalkeepers[4], Position_Players[4], Data_Goalkeeper_Format_5[0], 
Data_Goalkeeper_Format_5[1], Data_Goalkeeper_Format_5[2], Data_Goalkeeper_Format_5[3], Data_Goalkeeper_Format_5[4], 
Data_Goalkeeper_Format_5[5],Data_Goalkeeper_Format_5[6], Data_Goalkeeper_Format_5[7],Data_Goalkeeper_Format_5[8]))

cur.execute("""INSERT INTO Stats_UCL_GK (player, team, position_player, games, games_starts, minutes, minutes_90s, goals_against, goals_against_per90, shots_on_target, saves, saves_percent) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Goalkeepers_name[5],Teams_Goalkeepers[5], Position_Players[5], Data_Goalkeeper_Format_6[0], 
Data_Goalkeeper_Format_6[1], Data_Goalkeeper_Format_6[2], Data_Goalkeeper_Format_6[3], Data_Goalkeeper_Format_6[4], 
Data_Goalkeeper_Format_6[5],Data_Goalkeeper_Format_6[6], Data_Goalkeeper_Format_6[7],Data_Goalkeeper_Format_6[8]))

conn.commit()
