#%%
##### Biblioteca #####

import requests
import psycopg2
from bs4 import BeautifulSoup

#%%

##### Banco de Dados #####

conn = psycopg2.connect(database = 'projeto_integrado' , user = 'postgres' , password = '123' )
cur = conn.cursor()

#%%

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}

#%%

##### Requisição / Solicitação #####

response = requests.get('https://www.gazetaesportiva.com/campeonatos/uefa-champions-league-2020/', headers = headers)

#%%

##### Status #####

print("STATUS\n")
print(response.status_code)

#%%

##### Cabeçalho #####

print("CABEÇALHO\n")
print(response.headers)

#%%

#### All html #####

print("Todo Conteúdo HTML\n")
print(response.content)

#%%

##### Transição #####

# Todo conteúdo HTML passado para o VSCODE, utilizando o content da biblioteca request, onde o typo é byte
content = response.content

site = BeautifulSoup(content, "html.parser") # Aqui o type é um objeto da classe BS

#%%

##### TIMES ##### PARTE 1

# O local no Html onde possui os nomes dos times integrado ao BS
html_UCL = site.find_all('a', attrs={'class' : 'team-link'})
# html_UCL é como se fosse uma 'lista' do BS
print(html_UCL[6].get_text()) # Obter apenas o texto da posição 0

#%%

##### TIMES ##### PARTE 2

# Lista que vai receber os times, porém a lista não está formatada
times_UCL = []

# (For) para percorrer os itens do html_UCL para colocar na lista times_UCL.
for conteudo in html_UCL:
    if conteudo.get_text() != '': # no html_UCL possui alguns textos vazios, logo o uso do IF
        times_UCL.append(conteudo.get_text())
    
# Lista de times não formatadas    
print(times_UCL)

#%%

##### TIMES ##### PARTE 3 #####

##### FORMATAÇÃO DA LISTA DE TIMES #####

''' OITAVAS = 16 TIMES, COM IDA E VOLTA SÃO 32 JOGOS 
    QUARTAS = 8 TIMES, COM IDA E VOLTA SÃO 16 JOGOS
    SEMIS = 4 TIMES, COM IDA E VOLTA SÃO 08 JOGOS
'''
# Jogos das oitavas, quartas e semis

oitavas_de_final = times_UCL[0:32]
print(oitavas_de_final)

print('\n')

quartas_de_final = times_UCL[32:48]
print(quartas_de_final)

print('\n')

semi_final = times_UCL[48:56]
print(semi_final)

print('\n')

final = times_UCL[56:]
print(final)

#%%

# Formatação dos jogos das oitavas, quartas e semis finais
# Objetivo: separar por lista de jogos

# Formatação Oitavas
times_oitavas_final = []

for i in range(0,len(oitavas_de_final),2):
    times_oitavas_final.append([oitavas_de_final[i],oitavas_de_final[i+1]])
print(times_oitavas_final)

print('\n')

# Formatação Quartas
times_quartas_final = []

for i in range(0, len(quartas_de_final),2):
    times_quartas_final.append([quartas_de_final[i],quartas_de_final[i+1]])
print(times_quartas_final)

print('\n')

# Formatação Semis
times_semi_final = []

for i in range(0, len(semi_final),2):
    times_semi_final.append([semi_final[i], semi_final[i+1]])
print(times_semi_final)    

#%%

##### PLACARES DOS JOGOS ##### 

# O local no Html onde possui o placar 
# A formatação dos placares possuem o placar da partida com espaços(\n)
placares_UCL = site.find_all('span', attrs={'class' : 'score'})

# Formatação dos placares 
resultados_jogos_UCL = []

# For para formatar os placares
for resultado in placares_UCL:

    # Pegar o conteúdo de texto do placares_UCL e jogar pro placar_texto, isso inclui os espaços
    placar_texto = resultado.get_text() 

    # lista para trabalhar com os valores 
    placar_texto_format = []

    for conteudo_placar in placar_texto: 
        # Se conteúdo dentro do placar_texto for diferente de (\n) vai add na lista placar_texto_format com o type int
        if conteudo_placar != '\n':
            placar_texto_format.append(int(conteudo_placar))

    # Jogar os valores do placar_texto format para a variável resultados_jogos_UCL
    resultados_jogos_UCL.append(placar_texto_format)

print(resultados_jogos_UCL)

#%%

##### PLACARES DOS JOGOS DE ACORDO COM A FASE #####

print('Resultados das Oitavas \n')
resultados_UCL_oitavas = resultados_jogos_UCL[0:16]
print(resultados_UCL_oitavas)

print('\n\n')

print('Resultados das Quartas \n')
resultados_UCL_quartas = resultados_jogos_UCL[16:24]
print(resultados_UCL_quartas)

print('\n\n')

print('Resultados das Semis Finais \n')
resultados_UCL_semis = resultados_jogos_UCL[24:28]
print(resultados_UCL_semis)

print('\n\n')

print('Resultado da final \n')
resultados_UCL_final = resultados_jogos_UCL[28:]
print(resultados_UCL_final)

# %%

##### DIA, DATA, HORA, ESTADIO ##### 

# O local no Html onde possui os (Dia, data, hora, estádio)
info_site_UCL = site.find_all('span', attrs={'class' : 'date'})

# O texto é dado em apenas um string, sendo dia,data,hora,estádio em ordem

# Formatação das informações (dia, data, hora, estádio) para deixar cada atributo separado e 
# padronizado em uma lista de lista, assim como os jogos estão organizados

# Criação de lista de informações
info_format_UCL = []

for info in info_site_UCL:

    # Informações de texto do info_site_UCL
    info_texto = info.get_text()
    
    # Separar o dia da semana, ou seja, DIA DA SEMANA vai ter o index = 0 
    informacoes_gerais = info_texto.split('-')

    # Repartindo a variável info_texto entre os limites que refere ao DIA DO JOGO, onde possui index = 1
    informacoes_gerais[1] = info_texto[6:11]

    # Repartir o texto da variável e add na variável info_gerais para obter o HORÁRIO
    informacoes_gerais.append(info_texto[12:17]) 

    # Repartir o texto da variável e add na variável info_gerais para obter o ESTÁDIO
    informacoes_gerais.append(info_texto[20:])

    info_format_UCL.append(informacoes_gerais) 

print(info_format_UCL)
#%%

# Formatação das informações gerais 

informacoes_oitavas = info_format_UCL[0:16]
print(informacoes_oitavas)

print('\n')

informacoes_quartas = info_format_UCL[16:24]
print(informacoes_quartas)

print('\n')

informacoes_semis = info_format_UCL[24:28]
print(informacoes_semis)

print('\n')

informacoes_final = info_format_UCL[28:]
print(informacoes_final)

# %%

##### INSERÇÃO NO BANCO DE DADOS POSTGRES #####

# Inserção dos dados das oitavas de finais

for i in range(len(times_oitavas_final)):
    inserir_oitavas = "Insert into uefa_champions_league (time_mandante, time_visitante, placar_mandante, placar_visitante, estadio_jogo, dia_semana, data_jogo, horario_jogo, etapa) values( %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cur.execute(inserir_oitavas,(times_oitavas_final[i][0], times_oitavas_final[i][1], str(resultados_UCL_oitavas[i][0]), str(resultados_UCL_oitavas[i][1]), informacoes_oitavas[i][3], informacoes_oitavas[i][0], informacoes_oitavas[i][1], informacoes_oitavas[i][2], 'Oitavas de final'))

conn.commit()

#%%
# Inserção dos dados das Quartas de finais

for i in range(len(times_quartas_final)):
    inserir_quartas = "Insert into uefa_champions_league (time_mandante, time_visitante, placar_mandante, placar_visitante, estadio_jogo, dia_semana, data_jogo, horario_jogo, etapa) values( %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cur.execute(inserir_quartas,(times_quartas_final[i][0], times_quartas_final[i][1], str(resultados_UCL_quartas[i][0]), str(resultados_UCL_quartas[i][1]), informacoes_quartas[i][3], informacoes_quartas[i][0], informacoes_quartas[i][1], informacoes_quartas[i][2], 'Quartas de finais'))

conn.commit()

#%%
# Inserção dos dados das Semifinais

for i in range(len(times_semi_final)):
    inserir_semi =  "Insert into uefa_champions_league (time_mandante, time_visitante, placar_mandante, placar_visitante, estadio_jogo, dia_semana, data_jogo, horario_jogo, etapa) values( %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    
    if len(resultados_UCL_semis[i]) != 0:
        cur.execute(inserir_semi,(times_semi_final[i][0], times_semi_final[i][1], str(resultados_UCL_semis[i][0]), str(resultados_UCL_semis[i][1]), informacoes_semis[i][3], informacoes_semis[i][0], informacoes_semis[i][1], informacoes_semis[i][2], 'Semifinal'))
    
conn.commit()

# %%
