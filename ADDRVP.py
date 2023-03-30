#Augu datubāzes datu rediģēšanas un vizualizācijas programmas kods

#Programmas koda licencesana
#autors: Arts Inarts Kubilis
#licence: CC BY-NC-ND 4.0 (https://creativecommons.org/licenses/by-nc-nd/4.0/)

#bibliotekas
import csv
import os
import mysql.connector #https://pypi.org/project/mysql-connector-python/


#funkcijas
def pievienosana(): #pievieno datus no paraugam atbilstosa csv faila datubazei
  global datubaze
  global cursors
  
  #csv faila izvelesanas
  izv=0
  csvfaili=[]
  mapesnosauk='csvfaili'

  dir= os.getcwd()
  dirsast=os.listdir(dir)

  dirmape=os.path.join(dir, mapesnosauk)

  if mapesnosauk not in dirsast: #"augi" mapes izveide, ja ta nepastav
      izv=1
      os.makedirs(dirmape)

  faili=os.listdir(dirmape)

  for i in faili:
    fails=i.split('.')
    if fails[-1] == 'csv':
      csvfaili.append(i)

  if len(csvfaili)>0:
    print(f'Izvelies csv failu: (ievadi nr)')
    
    skaits=[]
    j=1
    for i in csvfaili:
      print(f'{j}. {i}')
      
      skaits.append(str(j))
      j=j+1
      
    while True:
      inp=input('> ')
      if inp in skaits:
        csvfails=csvfaili[int(inp)-1]
        break
    
  else:
    if izv==1:
      print(' ')
      print(f'Ievietojiet csv failus "{mapesnosauk}" mape!')
      return
    
    else:
      print(' ')
      print(f'Mape "{mapesnosauk}" nav nieviena csv faila!')
      return
    
  #datu iegusana no csv faila
  csvdati=[]
  csvfailadir=os.path.join(dirmape,  csvfails)
  atvcsvfails=open(csvfailadir, 'r')
  csvlasitajs=csv.reader(atvcsvfails)
  for i in csvlasitajs:
    csvdati.append(i)

  i=0

  #datu ievietosana datubaze
  dbdati=[]
  datuatsauces=[]
  while i<len(csvdati):
    rinda=csvdati[i]
    if (len(rinda)!=2 and i<14) or (len(csvdati)!=15):
      print(' ')
      print('CSV fails neatbilst paraugam!')
      return
      
    kolonna=rinda[1]
    
    if i<14:
      dbdati.append(kolonna)

    else:
      for j in rinda:
        datuatsauces.append(j)
        
      datuatsauces.pop(0)
    
    i=i+1

  #kollonas id iegusana(jo AUTO_INCREMENT nestrada)
  auguid=[]
  sql='SELECT id FROM augi'
  cursors.execute(sql)
  dbpiepras=cursors.fetchall()
  for i in dbpiepras:
    auguid.append(i[0])
    
  i=0
  while i<len(auguid):
    if auguid[i]!=i+1:
        pedejaisaugid=i+1
        break
    
    else:
      pedejaisaugid=auguid[-1]+1
    
    i=i+1
  
  if len(dbpiepras)==0:
    pedejaisaugid=1

  dbdati.insert(0, pedejaisaugid)

  try:
    sql='INSERT INTO augi (id, nosaukums, latiniskais_nosaukums, skirne, apraksts, veids, augsanas_ilgums, dzivesilgums, izturiba, saknu_dzilums, stadisanas_menesis, minimala_temperatura, laistisanas_biezums, gaismas_vide, vide) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursors.execute(sql, dbdati)
    datubaze.commit()

  except mysql.connector.Error:
    print(' ')
    print(f'Augs "{dbdati[1]} ({dbdati[2]})" jau eksiste datubaze!')
    return

  #atsaucu ievietosana datubaze
  atsaucesid=[]
  
  for i in datuatsauces:
    atsaucuid=[]
    #kollonas id iegusana
    sql='SELECT id FROM atsauces'
    cursors.execute(sql)
    dbpiepras=cursors.fetchall()
    for l in dbpiepras:
      atsaucuid.append(l[0])
    
    j=0
    while j<len(atsaucuid):
      if atsaucuid[j]!=j+1:
          pedejaisid=j+1
          break
    
      else:
        pedejaisid=atsaucuid[-1]+1
    
      j=j+1
    
    if len(dbpiepras)==0:
      pedejaisid=1
    
    sql="INSERT INTO atsauces (id, atsauce) VALUES (%s, %s)"
    vert=(pedejaisid, i)
    cursors.execute(sql, vert)
    datubaze.commit()
    
    print(pedejaisid)
  #atsaucu ievietosana starptabula augi_atsauce
  for i in datuatsauces:
    sql=f"SELECT id FROM atsauces WHERE atsauce='{i}'"
    cursors.execute(sql)
    dbpiepras=cursors.fetchall()
    dbpiepras=dbpiepras[0]
    dbpiepras=dbpiepras[0]
    atsaucesid.append(dbpiepras)
      
  sql=f"SELECT id FROM augi WHERE id={pedejaisaugid}"
  cursors.execute(sql)
  dbpiepras=cursors.fetchall()
  dbpiepras=dbpiepras[0]
  augaid=dbpiepras[0]

  for i in atsaucesid:
    sql='INSERT INTO augi_atsauce (auga_id, atsauces_Id) VALUES (%s,%s)'
    vert=(augaid, i)
    cursors.execute(sql, vert)
    datubaze.commit()

  print(' ')
  print(f'Augs "{dbdati[1]} ({dbdati[2]})" veiksmigi pievienots datubazei')

def izdzesana(): #izdzes augus no datubazes
  global datubaze
  global cursors
  
  #dzesama auga izvelesanas no datubazes
  print('Izvelies augu ko izdzest no datubazes: (ievadi nr)')
  sql='SELECT id, nosaukums , latiniskais_nosaukums FROM augi'
  cursors.execute(sql)
  dbaugs=cursors.fetchall()
  
  skaits=[]
  
  for augainfo in dbaugs:
    print(f'{augainfo[0]}. {augainfo[1]} ({augainfo[2]})')
    skaits.append(str(augainfo[0]))
    
  
  while True:
    inp=input('> ')
    
    if inp in skaits:
      break
  
  #atsaucu daudzuma iegusana
  atsaucuid=[]
  
  sql=f'SELECT atsauces_id FROM augi_atsauce WHERE auga_Id={int(inp)}'
  cursors.execute(sql)
  dbpiepras=cursors.fetchall()
  for i in dbpiepras:
    atsaucuid.append(i[0])
  
  #auga dzesana no datubazes "augi_atsauce" tabulas
  sql=f'DELETE FROM augi_atsauce WHERE auga_id={int(inp)}'
  cursors.execute(sql)
  datubaze.commit()
  
  #auga dzesana no datubazes "augi" tabulas
  sql=f'DELETE FROM augi WHERE id={int(inp)}'
  cursors.execute(sql)
  datubaze.commit()
  
  #auga dzesana no datubazes "atsauces" tabulas
  for i in atsaucuid:
    sql=f'DELETE FROM atsauces WHERE id={i}'
    cursors.execute(sql)
    datubaze.commit()
  
  try:
    augainfo=dbaugs[int(inp)-1]
  
  except IndexError:
    pass
  
  print(' ')
  print(f'Augs "{augainfo[1]} ({augainfo[2]})" veiksmigi izdests no datubazes')

def attelosana():
  print('Izvelies augu kura datubazes ierakstu attelot: (ievadi nr, lai attelotu visus ierakstus ievadi "0")')
  sql='SELECT id, nosaukums , latiniskais_nosaukums FROM augi'
  cursors.execute(sql)
  dbaugs=cursors.fetchall()
  
  skaits=[]
  
  for augainfo in dbaugs:
    print(f'{augainfo[0]}. {augainfo[1]} ({augainfo[2]})')
    skaits.append(str(augainfo[0]))
    
  tabula=[]
  while True:
    inp=input('> ')
    
    if inp=='0':
      sql='SELECT * FROM augi'
      cursors.execute(sql)
      dbdati=cursors.fetchall()
      
      sql='SELECT * FROM augi_atsauce'
      cursors.execute(sql)
      dbatsauces=cursors.fetchall()
      
      sql='SELECT * FROM atsauces'
      cursors.execute(sql)
      dbatsauceslinks=cursors.fetchall()
      print(dbatsauceslinks)
      
      for ieraksts in dbdati:
        print('')
        print(f'id: {ieraksts[0]}')
        print(f'nosaukums: {ieraksts[1]}')
        print(f'latiniskais_nosaukums: {ieraksts[2]}')
        print(f'skirne: {ieraksts[3]}')
        print(f'apraksts: {ieraksts[4]}')
        print(f'veids: {ieraksts[5]}')
        print(f'augsanas_ilgums: {ieraksts[6]}')
        print(f'dzivesilgums: {ieraksts[7]}')
        print(f'izturiba: {ieraksts[8]}')
        print(f'saknu_dzilums: {ieraksts[9]}')
        print(f'stadisanas_menesis: {ieraksts[10]}')
        print(f'minimala_temperatura: {ieraksts[11]}')
        print(f'laistisanas_biezums: {ieraksts[12]}')
        print(f'gaismas_vide: {ieraksts[13]}')
        print(f'vide: {ieraksts[14]}')
        for atsauce in dbatsauces:
          if atsauce[0]==ieraksts[0]:
            sql=f'SELECT * FROM atsauces WHERE id="{atsauce[1]}"'
            cursors.execute(sql)
            dbatsauceslinks=cursors.fetchall()
            dbatsauceslinks=dbatsauceslinks[0]
            dbatsauceslinks=dbatsauceslinks[-1]
            print(dbatsauceslinks)
      break
      
    if inp in skaits:
      sql=f'SELECT * FROM augi WHERE id="{inp}"'
      cursors.execute(sql)
      dbdati=cursors.fetchall()
      dbdati=dbdati[0]
      
      sql='SELECT * FROM augi_atsauce'
      cursors.execute(sql)
      dbatsauces=cursors.fetchall()
      
      sql='SELECT * FROM atsauces'
      cursors.execute(sql)
      dbatsauceslinks=cursors.fetchall()
      
      print('')
      print(f'id: {dbdati[0]}')
      print(f'nosaukums: {dbdati[1]}')
      print(f'latiniskais_nosaukums: {dbdati[2]}')
      print(f'skirne: {dbdati[3]}')
      print(f'apraksts: {dbdati[4]}')
      print(f'veids: {dbdati[5]}')
      print(f'augsanas_ilgums: {dbdati[6]}')
      print(f'dzivesilgums: {dbdati[7]}')
      print(f'izturiba: {dbdati[8]}')
      print(f'saknu_dzilums: {dbdati[9]}')
      print(f'stadisanas_menesis: {dbdati[10]}')
      print(f'minimala_temperatura: {dbdati[11]}')
      print(f'laistisanas_biezums: {dbdati[12]}')
      print(f'gaismas_vide: {dbdati[13]}')
      print(f'vide: {dbdati[14]}')
      for atsauce in dbatsauces:
        if atsauce[0]==dbdati[0]:
          sql=f'SELECT * FROM atsauces WHERE id="{atsauce[1]}"'
          cursors.execute(sql)
          dbatsauceslinks=cursors.fetchall()
          dbatsauceslinks=dbatsauceslinks[0]
          dbatsauceslinks=dbatsauceslinks[-1]
          print(dbatsauceslinks)
      break
  
  


#MySql datu bazes savienosana
datubaze = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Skola12dit",
  database="augudatubaze"
  
)

cursors=datubaze.cursor()


#galvenai loops
while True:
  sql='SELECT id FROM augi'
  cursors.execute(sql)
  dbaugs=cursors.fetchall()
  
  print('Opcijas: (ievadi nr)')
  print('1. Pievienot augu datubazei')
  if len(dbaugs)>0:
    print('2. Izdzest augu no datubazes')
    print('3. Attelot auga ierakstu no datubazes')
  
  while True:
    inp=input('> ')

    if inp=='1': #auga pievienosana datubazei
      print(' ')
      pievienosana()
      break
      
    if inp=='2' and len(dbaugs)>0: #auga izdzesana no datubazes
      print(' ')
      izdzesana()
      break
    
    if inp=='3' and len(dbaugs)>0: #datubazes auga ieraksta attelosana
      print(' ')
      attelosana()
      break
      
  print(' ')
  print(' ')