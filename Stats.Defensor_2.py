## BIBLIOTECAS

import requests
import psycopg2
from bs4 import BeautifulSoup as soup

## BANCO DE DADOS

conn = psycopg2.connect(database = 'projeto_integrado' , user = 'postgres' , password = '123' )
cur = conn.cursor()

# FUNÇÃO
def Data_Clean_DEF (lista,lista_nova): # Função para utilizar apenas os dados que eu quero trabalhar

    del(lista[24])
    del(lista[22])
    del(lista[19])
    del(lista[7:17])
    del(lista[0])

    for i in lista:
        lista_nova.append(float(i))

def Data_Clean_STD (lista,lista_nova): # Função para tabela standar GAMES - MINUTES - START
    lista = lista[1:4]
    for i in lista:
        lista_nova.append(float(i))


# REQUESTS / BEAUTIFULSOUP

url = 'https://fbref.com/en/stathead/player_comparison.cgi?request=1&sum=0&comp_type=spec&dom_lg=1&spec_comps=8&player_id1=d5f2f82b&p1yrfrom=2020-2021&player_id2=436a9dd0&p2yrfrom=2020-2021&player_id3=d2424d1b&p3yrfrom=2020-2021&player_id4=45db685d&p4yrfrom=2020-2021&player_id5=4d224fe8&p5yrfrom=2020-2021&player_id6=57d88cf9&p6yrfrom=2020-2021&player_id7=53cad200&p7yrfrom=2020-2021'

r = requests.get(url)

soup = soup(r.text, 'html.parser')

league_table = soup.find('table', {"id": "defense_stats"})
league_table_standard = soup.find('table', class_ = 'min_width per_g_toggle sortable stats_table min_width shade_zero')

# LISTAS DE MANIPULAÇÃO

Headers = [] # Titulos da coluna
Defensors_name = [] # Lista com nome dos artilheiros
Position_Players = [] # Posição dos jogadores
Data_Defensors = [] # Dados dos goleiros
Data_Defensors_std = [] # Dados dos jogadores (tabela standard)
Teams_Defensors = [] # Time dos goleiros

# LISTA DE JOGADORES
for content in league_table.find_all('tbody'):
    access_tr_1 = content.find_all('tr')
    for value in access_tr_1:
        players_list =  value.find('th', class_ = 'left').text
        Defensors_name.append(players_list)

# DADOS GERAIS

for content in league_table.find_all('tbody'): # Encontrar o tbody (estrutura todo conteúdo da tabela 'corpo')
    access_tr_2 = content.find_all('tr')  # Encontrar todos os tr
    for content_ in access_tr_2:
        access_td = content_.find_all('td', class_ = 'right') # Especificar div e a classe
        for value in access_td:
            header_table = ((value.get('data-stat'))) # header da tabela
            value_table = (value.get_text()) # valor
            Data_Defensors.append(value_table) 
            Headers.append(header_table)

# DADOS DE GAMES - STARTS - MINUTES
for content in league_table_standard.find_all('tbody'): # Encontrar o tbody (estrutura todo conteúdo da tabela 'corpo')
    access_tr_2 = content.find_all('tr')  # Encontrar todos os tr
    for content_ in access_tr_2:
        access_td = content_.find_all('td', class_ = 'right') # Especificar div e a classe
        for value in access_td:
            header_table = ((value.get('data-stat'))) # header da tabela
            value_table = (value.get_text()) # valor
            Data_Defensors_std.append(value_table) 
    

# EQUIPE
for content in league_table.find_all('tbody'): # Encontrar o tbody (estrutura todo conteúdo da tabela 'corpo')
    access_tr_3 = content.find_all('tr')  # Encontrar todos os tr
    for content_ in access_tr_3:
        access_td = content_.find_all('td', class_ = 'left') # Especificar div e a classe
        for value in access_td:
            y = (value.get_text()) # valor
            Teams_Defensors.append(y)

Teams_Defensors = Teams_Defensors[1::2] 
Teams_Defensors[0] = 'Paris Saint Germain'
Teams_Defensors[1] = 'Paris Saint Germain'
Teams_Defensors[5] = 'Borussia Dortmund'


# POSIÇÃO
for content in league_table.find_all('tbody'): # Encontrar o tbody (estrutura todo conteúdo da tabela 'corpo')
    access_tr_4 = content.find_all('tr')  # Encontrar todos os tr
    for content_ in access_tr_4:
        access_td = content_.find_all('td', class_ = 'center') # Especificar div e a classe
        for value in access_td:
            p = (value.get_text()) # valor
            Position_Players.append(p)

# DELIMITANDO DADOS NAS LISTAS PARA CADA JOGADOR

# DADOS TABELA DEFENSIVE
Data_Defensors_1 = Data_Defensors[0:25]
Data_Defensors_2 = Data_Defensors[25:50]
Data_Defensors_3 = Data_Defensors[50:75]
Data_Defensors_4 = Data_Defensors[75:100]
Data_Defensors_5 = Data_Defensors[100:125]
Data_Defensors_6 = Data_Defensors[125:]

# DADOS TABELA STANDARD
Data_Defensors_std_1 = Data_Defensors_std[0:26]
Data_Defensors_std_2 = Data_Defensors_std[26:52]
Data_Defensors_std_3 = Data_Defensors_std[52:78]
Data_Defensors_std_4 = Data_Defensors_std[78:104]
Data_Defensors_std_5 = Data_Defensors_std[104:130]
Data_Defensors_std_6 = Data_Defensors_std[130:]

# CRIAÇÃO DE LISTAS PARA FORMATAÇÃO 

# DADOS FORMATADOS TABELA DEFENSIVE ACTION
Data_Defensors_Format_1 = []
Data_Defensors_Format_2 = []
Data_Defensors_Format_3 = []
Data_Defensors_Format_4 = []
Data_Defensors_Format_5 = []
Data_Defensors_Format_6 = []

# DADOS FORMATADOS TABELA STANDARD
Data_Defensors_std_Format_1 = []
Data_Defensors_std_Format_2 = []
Data_Defensors_std_Format_3 = []
Data_Defensors_std_Format_4 = []
Data_Defensors_std_Format_5 = []
Data_Defensors_std_Format_6 = []

# APLICANDO A FUNÇÃO PARA EXCLUIR DADOS QUE NÃO FOREM UTILIZADOS
Data_Defensors_std_4[3] = 1028

Data_Clean_DEF(Data_Defensors_1, Data_Defensors_Format_1)
Data_Clean_DEF(Data_Defensors_2, Data_Defensors_Format_2)
Data_Clean_DEF(Data_Defensors_3, Data_Defensors_Format_3)
Data_Clean_DEF(Data_Defensors_4, Data_Defensors_Format_4)
Data_Clean_DEF(Data_Defensors_5, Data_Defensors_Format_5)
Data_Clean_DEF(Data_Defensors_6, Data_Defensors_Format_6)

Data_Clean_STD(Data_Defensors_std_1, Data_Defensors_std_Format_1)
Data_Clean_STD(Data_Defensors_std_2, Data_Defensors_std_Format_2)
Data_Clean_STD(Data_Defensors_std_3, Data_Defensors_std_Format_3)
Data_Clean_STD(Data_Defensors_std_4, Data_Defensors_std_Format_4)
Data_Clean_STD(Data_Defensors_std_5, Data_Defensors_std_Format_5)
Data_Clean_STD(Data_Defensors_std_6, Data_Defensors_std_Format_6)

##### INSERÇÃO NO BANCO DE DADOS POSTGRES #####

cur.execute("""INSERT INTO Stats_UCL_DEF (player, team, position_player, games, games_starts, minutes, minutes_90s, tackle, tackle_won, tackle_DEF, tackle_MID, tackle_ATK, blocks, blocks_shot, blocks_pass, interception, cleareance) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Defensors_name[0],Teams_Defensors[0], Position_Players[0], Data_Defensors_std_Format_1[0], Data_Defensors_std_Format_1[1], Data_Defensors_std_Format_1[2], # PLAYER, TEAM, POSITION_PLAYER, GAMES, GAMES_START, MINUTES
Data_Defensors_Format_1[0], Data_Defensors_Format_1[1], Data_Defensors_Format_1[2], Data_Defensors_Format_1[3], # MINUTES_90S, TACKLE, TACKLE WON, TACKLE_DEF
Data_Defensors_Format_1[4], Data_Defensors_Format_1[5], Data_Defensors_Format_1[6], # TACKLE_MID, TACKLE_ATK, BLOCKS
Data_Defensors_Format_1[7], Data_Defensors_Format_1[8], Data_Defensors_Format_1[9], Data_Defensors_Format_1[10])) # BLOCKS_SHOT, BLOCKS_PASS, INTERCEPTIONS, CLEARENCES)) 


cur.execute("""INSERT INTO Stats_UCL_DEF (player, team, position_player, games, games_starts, minutes, minutes_90s, tackle, tackle_won, tackle_DEF, tackle_MID, tackle_ATK, blocks, blocks_shot, blocks_pass, interception, cleareance) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Defensors_name[1],Teams_Defensors[1], Position_Players[1], Data_Defensors_std_Format_2[0], Data_Defensors_std_Format_2[1], Data_Defensors_std_Format_2[2], # PLAYER, TEAM, POSITION_PLAYER, GAMES, GAMES_START, MINUTES
Data_Defensors_Format_2[0], Data_Defensors_Format_2[1], Data_Defensors_Format_2[2], Data_Defensors_Format_2[3], # MINUTES_90S, TACKLE, TACKLE WON, TACKLE_DEF
Data_Defensors_Format_2[4], Data_Defensors_Format_2[5], Data_Defensors_Format_2[6], # TACKLE_MID, TACKLE_ATK, BLOCKS
Data_Defensors_Format_2[7], Data_Defensors_Format_2[8], Data_Defensors_Format_2[9], Data_Defensors_Format_2[10])) # BLOCKS_SHOT, BLOCKS_PASS, INTERCEPTIONS, CLEARENCES)) 

cur.execute("""INSERT INTO Stats_UCL_DEF (player, team, position_player, games, games_starts, minutes, minutes_90s, tackle, tackle_won, tackle_DEF, tackle_MID, tackle_ATK, blocks, blocks_shot, blocks_pass, interception, cleareance) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Defensors_name[2],Teams_Defensors[2], Position_Players[2], Data_Defensors_std_Format_3[0], Data_Defensors_std_Format_3[1], Data_Defensors_std_Format_3[2], # PLAYER, TEAM, POSITION_PLAYER, GAMES, GAMES_START, MINUTES
Data_Defensors_Format_3[0], Data_Defensors_Format_3[1], Data_Defensors_Format_3[2], Data_Defensors_Format_3[3], # MINUTES_90S, TACKLE, TACKLE WON, TACKLE_DEF
Data_Defensors_Format_3[4], Data_Defensors_Format_3[5], Data_Defensors_Format_3[6], # TACKLE_MID, TACKLE_ATK, BLOCKS
Data_Defensors_Format_3[7], Data_Defensors_Format_3[8], Data_Defensors_Format_3[9], Data_Defensors_Format_3[10])) # BLOCKS_SHOT, BLOCKS_PASS, INTERCEPTIONS, CLEARENCES)) 

cur.execute("""INSERT INTO Stats_UCL_DEF (player, team, position_player, games, games_starts, minutes, minutes_90s, tackle, tackle_won, tackle_DEF, tackle_MID, tackle_ATK, blocks, blocks_shot, blocks_pass, interception, cleareance) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Defensors_name[3],Teams_Defensors[3], Position_Players[3], Data_Defensors_std_Format_4[0], Data_Defensors_std_Format_4[1], Data_Defensors_std_Format_4[2], # PLAYER, TEAM, POSITION_PLAYER, GAMES, GAMES_START, MINUTES
Data_Defensors_Format_4[0], Data_Defensors_Format_4[1], Data_Defensors_Format_4[2], Data_Defensors_Format_4[3], # MINUTES_90S, TACKLE, TACKLE WON, TACKLE_DEF
Data_Defensors_Format_4[4], Data_Defensors_Format_4[5], Data_Defensors_Format_4[6], # TACKLE_MID, TACKLE_ATK, BLOCKS
Data_Defensors_Format_4[7], Data_Defensors_Format_4[8], Data_Defensors_Format_4[9], Data_Defensors_Format_4[10])) # BLOCKS_SHOT, BLOCKS_PASS, INTERCEPTIONS, CLEARENCES)) 

cur.execute("""INSERT INTO Stats_UCL_DEF (player, team, position_player, games, games_starts, minutes, minutes_90s, tackle, tackle_won, tackle_DEF, tackle_MID, tackle_ATK, blocks, blocks_shot, blocks_pass, interception, cleareance) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
(Defensors_name[5],Teams_Defensors[5], Position_Players[5], Data_Defensors_std_Format_6[0], Data_Defensors_std_Format_6[1], Data_Defensors_std_Format_6[2], # PLAYER, TEAM, POSITION_PLAYER, GAMES, GAMES_START, MINUTES
Data_Defensors_Format_6[0], Data_Defensors_Format_6[1], Data_Defensors_Format_6[2], Data_Defensors_Format_6[3], # MINUTES_90S, TACKLE, TACKLE WON, TACKLE_DEF
Data_Defensors_Format_6[4], Data_Defensors_Format_6[5], Data_Defensors_Format_6[6], # TACKLE_MID, TACKLE_ATK, BLOCKS
Data_Defensors_Format_6[7], Data_Defensors_Format_6[8], Data_Defensors_Format_6[9], Data_Defensors_Format_6[10])) # BLOCKS_SHOT, BLOCKS_PASS, INTERCEPTIONS, CLEARENCES)) 

conn.commit()
