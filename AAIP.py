#Augu augšanas analīzes un informācijas programmas kods

#Programmas koda licencesana
#autors: Arts Inarts Kubilis
#licence: CC BY-NC-ND 4.0 (https://creativecommons.org/licenses/by-nc-nd/4.0/)

#bibliotekas
import requests #https://pypi.org/project/requests/
from cryptography.fernet import Fernet #https://pypi.org/project/cryptography/
import mysql.connector #https://pypi.org/project/mysql-connector-python/
from decimal import Decimal
import os
import shutil
import ctypes
import json
from datetime import datetime
import pytz

#funkcijas
def dienasvidejais(vert,cipskaizkomata,diena): #videja aprekinasana
    vertf=[]
    vertf.extend(vert)
    if diena==-2:
        pass
    
    if diena==-1:
        i=0
        while i<24:
            vertf.pop(0)
        
            i=i+1
    if diena==0:
        i=0
        while i<48:
            vertf.pop(0)
        
            i=i+1
    if diena==1:
        i=0
        while i<72:
            vertf.pop(0)
        
            i=i+1
            
    if diena==2:
        i=0
        while i<96:
            vertf.pop(0)
        
            i=i+1
    
    vertSk=24
    vertSum=0
    i=0
    while i<vertSk:
        vertSum=vertSum+vertf[i]
        
        i=i+1
    vertVid=vertSum/vertSk
    vertVid=Decimal(str(vertVid))
    vertf.clear()
    return round(vertVid,cipskaizkomata)

def debespuse(sk): #parveido gradus uz debespusem
    gradi=[0.0, 22.5, 45.0, 67.5, 90.0, 112.5, 135.0, 157.5, 180.0, 202.5, 225.0, 247.5, 270.0, 292.5, 315.0, 337.5, 360.0]
    sk=359

    rezultati=[]
    rezultatisak=[]
    for i in gradi:
        starpiba=abs(sk-i)
        rezultati.append(starpiba)

    rezultatisak.extend(rezultati)
    rezultatisak.sort()
    mazstarp=rezultatisak[0]

    j=0
    for i in rezultati:
        if i==mazstarp:
            break
        
        j=j+1

    if gradi[j]==0.0 or gradi[j]==360.0:
        virziens='Ziemelu vejs'
        
    if gradi[j]==22.5:
        virziens='Ziemelu-ziemelaustrumu vejs'
        
    if gradi[j]==45.0:
        virziens='Ziemelaustrumu vejs'
        
    if gradi[j]==67.5:
        virziens='Austrumu-ziemelaustrumu vejs'
        
    if gradi[j]==90.0:
        virziens='Austrumu vejs'
        
    if gradi[j]==112.5:
        virziens='Austrumu-dienvidaustrumu vejs'
        
    if gradi[j]==135.0:
        virziens='Dienvidaustrumu vejs'

    if gradi[j]==157.5:
        virziens='Dienvidu-dienvidaustrumu vejs'
        
    if gradi[j]==180.0:
        virziens='Dienvidu vejs'
        
    if gradi[j]==202.5:
        virziens='Dienvidu-dienvidrietumu vejs'
        
    if gradi[j]==225.0:
        virziens='Dienvidrietumu vejs'

    if gradi[j]==247.5:
        virziens='Rietumu-dienvidrietumu vejs'

    if gradi[j]==270.0:
        virziens='Rietumu vejs'
        
    if gradi[j]==292.5:
        virziens='Rietumu-ziemelrietumu vejs'
        
    if gradi[j]==315.0:
        virziens='Ziemelrietumu vejs'
        
    if gradi[j]==337.5:
        virziens='Ziemelu-ziemelrietumus vejs'
        
    return virziens

def gadalaks(menesis):
    gadalaiki=[]

    ziema=['Decembris', 'Janvaris', 'Februaris', 'Ziema']
    pavasaris=['Marts', 'Aprilis', 'Maijs', 'Pavasaris']
    vasara=['Junijs', 'Julijs', 'Augusts', 'Vasara']
    rudens=['Septembris', 'Oktobris', 'Novembris', 'Rudens']

    gadalaiki.append(ziema)
    gadalaiki.append(pavasaris)
    gadalaiki.append(vasara)
    gadalaiki.append(rudens)

    menesis='Maijs'

    for i in gadalaiki:
        if menesis in i:
            glaiks=(i[-1])

    return glaiks

#datu apstrade
def sifresana(atrv, lat, long, tzona): #datu sifresanas funkcija
    global sifratslega
    
    dati=[atrv,lat,long,tzona]
    sifrdati=[]
    sifrs=Fernet(sifratslega)
    
    for i in dati:
        i=str(i)
        i=i.encode('utf-8')
        sifrdati.append(sifrs.encrypt(i))

    return sifrdati

def atsifresana(nepsifrdati): #sifreto datu atsifresanas funkcija
    global sifratslega
    
    sifrs=Fernet(sifratslega)
    
    i=-1
    while len(nepsifrdati)/2>i:
        i=i+1
        nepsifrdati.pop(i)
        
    atsifrdati=[]
    i=0
    
    while len(nepsifrdati)>i:
        x=nepsifrdati[i]
        x=x.decode('utf-8')
        x=x.replace("b'",''); x=x.replace("'",'')
        x=sifrs.decrypt(x)
        atsifrdati.append(x.decode('utf-8'))
        
        i=i+1
    
    return atsifrdati

#datu saglabasana, atversana un papildinasana
def saglabasana(nosauk, atrv, lat , long, tzona, augs, latinnosauk, augid, iestadlaiks, auglaiks): #saglaba datus json failos jauniem augiem
    global auganr
    global dirmape
    
    #parastie
    dati={'nosaukums':nosauk,
          'augaid': augid,
          'augs':f'{augs} ({latinnosauk})',
          'iestadisanaslaiks':iestadlaiks,
          'atlikusaisaugsanaslaiks':auglaiks
          
         }
    
    dirmapesast=sorted(os.listdir(dirmape), key=len)
    if len(dirmapesast)>0:
        num=[]
        pedfails=dirmapesast[-1]
        for i in pedfails:
            if i.isdigit():
                num.append(i)
        
        num=''.join(num)
        auganr=int(num)+1
        
    dirfails=os.path.join(dirmape, f'{auganr}augs.json')
    jsonfails=open(dirfails, 'w')
    jsondati=json.dumps(dati)
    jsonfails.write(jsondati)
    jsonfails.close()
    
    #sifretie
    sifrdatukopa=sifresana(atrv,lat,long,tzona)
    sifrdati=f'atrasanasvieta:\n{sifrdatukopa[0]}\nlatitude:\n{sifrdatukopa[1]}\nlongitude:\n{sifrdatukopa[2]}\nlaikazona:\n{sifrdatukopa[3]}'
    sifrdati=sifrdati.encode('utf-8')
    
    dirsifrfails=os.path.join(dirmape, f'{auganr}augslok.json')
    jsonsifrfails=open(dirsifrfails, 'wb')
    jsonsifrfails.write(sifrdati)
    jsonsifrfails.close()
    
    auganr=auganr+1

def atversana(): #paradadatus par augu un atjauno tos
    global dirmape
    global cursors
    
    dirmapesast=sorted(os.listdir(dirmape), key=len)
    print('')
    print('Izvelies augu: (ievadi nr)')
    sastavs=[]
    skaits=[]
    j=1
    for i in dirmapesast:
        for l in i:
            sastavs.append(l)
        
        if 'l' not in sastavs:
            dirsifrfails=os.path.join(dirmape, i)
            jsonsifrfails=open(dirsifrfails, 'r')
            nosauk=jsonsifrfails.readlines()
            nosauk=nosauk[0]
            nosauk=json.loads(nosauk)
            jsonsifrfails.close()
            
            fnosauk=''
            for k in i:
                vaiskaitlis=k.isdigit()
                if vaiskaitlis ==True:
                    fnosauk=fnosauk+k
            
            print(f'{fnosauk}. {nosauk["nosaukums"]}')
            skaits.append(fnosauk)
            
            j=j+1
        
        sastavs.clear()
    
    while True:
        inp=input('> ')
        if inp in skaits:
            break
    
    dirsifrfails=os.path.join(dirmape, f'{inp}augslok.json')
    jsonsifrfails=open(dirsifrfails, 'rb')
    sifrdatinofaila=jsonsifrfails.readlines()
    atsifrdati=atsifresana(sifrdatinofaila)
    jsonsifrfails.close()
    
    dirfails=os.path.join(dirmape, f'{inp}augs.json')
    jsonfails=open(dirfails, 'r')
    jsondati=jsonfails.readlines()
    jsondati=jsondati[0]
    jsondati=json.loads(jsondati)
    jsonsifrfails.close()
    
    laikapstakli(atsifrdati[1],atsifrdati[2],atsifrdati[3],inp)
    
    dirfails=os.path.join(dirmape, f'{inp}augs.json')
    jsonfails=open(dirfails, 'r')
    jsondati=jsonfails.readlines()
    jsondati=jsondati[0]
    jsondati=json.loads(jsondati)
    jsonsifrfails.close()
    
    sql=f'SELECT skirne,apraksts,veids,dzivesilgums,izturiba,gaismas_vide,vide,stadisanas_menesis FROM augi WHERE id={jsondati["augaid"]}'
    cursors.execute(sql)
    sqldati=cursors.fetchall()
    sqldati=sqldati[0]
    
    stadlaiks=gadalaks(sqldati[7])
    
    #bistamibas stadijas
    if jsondati['iedzivosanasiespeja']=='maksimalas':
        stavoklis='Caurspidigs' #augam nedraud briesmas
        
    if jsondati['iedzivosanasiespeja']=='lielas':
        stavoklis='Zals' #augam draud nelielas briesmas
    
    if jsondati['iedzivosanasiespeja']=='videjas':
        stavoklis='Dzeltens' #augam iespejams draud briesmas
        
    if jsondati['iedzivosanasiespeja']=='mazas':
        stavoklis='Sarkans' #augam draud briesmas
    
    if jsondati['iedzivosanasiespeja']=='nekadas':
        stavoklis='Melns' #augs nomirst
        
    #informacijas attelosana lietotajam
    print('')
    print('')
    print(jsondati['nosaukums'])
    print('----------------------')
    print(f'Augs: {jsondati["augs"]}')
    print(f'Skirne: {sqldati[0]}')
    print(f'Veids: {sqldati[2]}')
    print(f'Apraksts: {sqldati[1]}')
    print(f'Stadisanas laiks: {stadlaiks}')
    print(f'Gaismas vide: {sqldati[5]}')
    print(f'Zemes vide: {sqldati[6]}')
    print(f'Dzives ilgums: {sqldati[3]}')
    print(f'Izturiba: {sqldati[4]}')
    print('')
    print(f'Atrasanas vieta: {atsifrdati[0]}')
    print(f'Iestadisanas laiks: {jsondati["iestadisanaslaiks"]}')
    if jsondati["atlikusaisaugsanaslaiks"]<=0:
        print('Dienas lidz nobriedumam: nobriedis')
    
    else:
        print(f'Dienas lidz nobriedumam: {jsondati["atlikusaisaugsanaslaiks"]}')
    
    if jsondati["laistisanasbiezums"]==1:
        print(f'Laistisanas biezums nedela: {jsondati["laistisanasbiezums"]} reize')
        
    else:
        print(f'Laistisanas biezums nedela: {jsondati["laistisanasbiezums"]} reizes')
        
    print(f'Auga stavoklis: {stavoklis}')
    print('')
    print(f'Nokrisni: {jsondati["nokrisnuveids"]}')
    print(f'Veja stiprums: {jsondati["vejastiprums"]} ({jsondati["vejaatrums"]}Km/h)')
    print(f'Veja virziens: {jsondati["vejavirziens"]}')
    
#laikapstaklu datu iegusana un analize
def laikapstakli(lat,long,tzona,nr=0): #tagadejo, un nakotnes prognozeto laikapstaklu datu ieguve un ar laikapstakliem saistitu datu ievietosana augu json failos, auga atlikuso dienu aprekinasana
#tagadejo laikapstaklu datu iegusana
    global dirmape
    global cursors

    Url=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&past_days=2&forecast_days=3&daily=temperature_2m_min,precipitation_probability_mean,precipitation_hours,rain_sum&hourly=temperature_2m,windspeed_10m,winddirection_10m,cloudcover,rain,soil_moisture_0_1cm,soil_moisture_1_3cm,soil_moisture_3_9cm,soil_moisture_9_27cm,soil_moisture_27_81cm&current_weather=true&timezone={tzona}"
    #https://api.open-meteo.com/v1/forecast?latitude=56.946&longitude=24.10589&past_days=2&forecast_days=3&daily=temperature_2m_min,precipitation_probability_mean,precipitation_hours,rain_sum&hourly=temperature_2m,windspeed_10m,winddirection_10m,cloudcover,rain,soil_moisture_0_1cm,soil_moisture_1_3cm,soil_moisture_3_9cm,soil_moisture_9_27cm,soil_moisture_27_81cm&current_weather=true&timezone=Europe%2FRiga
    Dati=requests.get(Url)
    Dati=Dati.json()
    
    #stunda
    hDati=Dati['hourly']
    hLaiks=hDati['time'] #datetime
    hTemp=hDati['temperature_2m'] #C
    hVejaatr=hDati['windspeed_10m'] #km/h
    hVejavirz=hDati['winddirection_10m'] #gradi
    hMakonudaudz=hDati['cloudcover'] #%
    hLetusdaudz=hDati['rain'] #mm
    hMitr0_1=hDati['soil_moisture_0_1cm'] #m^3/m^3
    hMitr1_3=hDati['soil_moisture_1_3cm'] #m^3/m^3
    hMitr3_9=hDati['soil_moisture_3_9cm'] #m^3/m^3
    hMitr9_27=hDati['soil_moisture_9_27cm'] #m^3/m^3
    hMitr27_81=hDati['soil_moisture_27_81cm'] #m^3/m^3
    
    #diena
    dDati=Dati['daily']
    dTempmin=dDati['temperature_2m_min'] #C
    dNokriesp=dDati['precipitation_probability_mean'] #%
    dNokrlaiks=dDati['precipitation_hours'] #h
    dLietussum=dDati['rain_sum'] #mm
    
    vidtemp=[]
    vidvejaatr=[]
    vidmakonudaudz=[]
    vidmitr0_1=[]
    vidmitr1_3=[]
    vidmitr3_9=[]
    vidmitr9_27=[]
    vidmitr27_81=[]
    
    i=-2
    while i<=2:
        vidtemp.append(dienasvidejais(hTemp,1,i)) #C
        vidvejaatr.append(dienasvidejais(hVejaatr,1,i)) #km/h
        vidmakonudaudz.append(dienasvidejais(hMakonudaudz,0,i)) #%
        vidmitr0_1.append(dienasvidejais(hMitr0_1,3,i)) #m^3/m^3
        vidmitr1_3.append(dienasvidejais(hMitr1_3,3,i)) #m^3/m^3
        vidmitr3_9.append(dienasvidejais(hMitr3_9,3,i)) #m^3/m^3
        vidmitr9_27.append(dienasvidejais(hMitr9_27,3,i)) #m^3/m^3
        vidmitr27_81.append(dienasvidejais(hMitr27_81,3,i)) #m^3/m^3
        
        i=i+1

    #datu analize
    sql=f'SELECT saknu_dzilums, minimala_temperatura, laistisanas_biezums, gaismas_vide, vide, izturiba FROM augi WHERE id={"id"}'
    cursors.execute(sql)
    dbdati=cursors.fetchall()
    dbdati=dbdati[0]
    #izdzivosanas iespejas
    vide=dbdati[4].split('-')
    makonudaudz=[]
                
    mitr0_1=[0,1]
    mitr1_3=[2,3]
    mitr3_9=[4,5,6,7,8,9]
    mitr9_27=[10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
    mitr27_81=[28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81]
    
    if dbdati[0] in mitr0_1:
        mitrums=vidmitr0_1
    
    elif dbdati[0] in mitr1_3:
        mitrums=vidmitr1_3
    
    elif dbdati[0] in mitr3_9:
        mitrums=vidmitr3_9
    
    elif dbdati[0] in mitr9_27:
        mitrums=vidmitr9_27
    
    elif dbdati[0] in mitr27_81:
        mitrums=vidmitr27_81
    
    #izdzivosanas iespeju parbaude
    izdzivvarbutiba=0
    if dbdati[5] == 'Liela':
        if dbdati[1]>dTempmin[2]:
            izdzivvarbutiba=4
            
        if 'Mitra' or 'mitra' in vide:
            if mitrums[0]<-1.5 and mitrums[1]<-1.5 and mitrums[2]<-1.5 and mitrums[3]<-1.5 and mitrums[4]<-1.5:
                izdzivvarbutiba=izdzivvarbutiba+1
                
        if dbdati[3]=='Saule':
            for i in vidmakonudaudz:
                if i>80:
                    makonudaudz.append(i)
            if len(makonudaudz) == len(vidmakonudaudz):
                izdzivvarbutiba=izdzivvarbutiba+1
        
        if vidtemp[0]>30 and vidtemp[1]>30 and vidtemp[2]>30 and vidtemp[3]>30 and vidtemp[4]>30:
            izdzivvarbutiba=izdzivvarbutiba+1
        
        if vidvejaatr[2]>48:
            izdzivvarbutiba=izdzivvarbutiba+1
            
        if dLietussum[2]>330:
            izdzivvarbutiba=izdzivvarbutiba+1
        
        #varbutibas pielidzinasa
        if izdzivvarbutiba==0:
            izdziviesp='maksimalas'
        
        elif izdzivvarbutiba==1:
            izdziviesp='lielas'
        
        elif izdzivvarbutiba==2:
            izdziviesp='videjas'
        
        elif izdzivvarbutiba==3:
            izdziviesp='mazas'
        
        elif izdzivvarbutiba>=4:
            izdziviesp='nekadas'

    elif dbdati[5] == 'Standarta':
        if dbdati[2]>dTempmin[2]:
            izdzivvarbutiba=3
        
        if 'Mitra' or 'mitra' in vide:
            if mitrums[0]<-1.5 and mitrums[1]<-1.5 and mitrums[2]<-1.5 and mitrums[3]<-1.5 and mitrums[4]<-1.5:
                izdzivvarbutiba=izdzivvarbutiba+1
            
        if dbdati[3]=='Saule':
            for i in vidmakonudaudz:
                if i>80:
                    makonudaudz.append(i)
            
            if len(makonudaudz) == len(vidmakonudaudz):
                izdzivvarbutiba=izdzivvarbutiba+1
        
        if vidtemp[0]>30 and vidtemp[1]>30 and vidtemp[2]>30 and vidtemp[3]>30 and vidtemp[4]>30:
            izdzivvarbutiba=izdzivvarbutiba+1
        
        if vidvejaatr[2]>48:
            izdzivvarbutiba=izdzivvarbutiba+1
            
        if dLietussum[2]>330:
            izdzivvarbutiba=izdzivvarbutiba+1
        
        #varbutibas pielidzinasa
        if izdzivvarbutiba==0:
            izdziviesp='maksimalas'
        
        elif izdzivvarbutiba==1:
            izdziviesp='videjas'
        
        elif izdzivvarbutiba==2:
            izdziviesp='mazas'
        
        elif izdzivvarbutiba>=3:
            izdziviesp='nekadas'
        
    elif dbdati[5] == 'Maza':
        if dbdati[2]>dTempmin[2]:
            izdzivvarbutiba=2
        
        if 'Mitra' or 'mitra' in vide:
            if mitrums[0]<-1.5 and mitrums[1]<-1.5 and mitrums[2]<-1.5 and mitrums[3]<-1.5 and mitrums[4]<-1.5:
                izdzivvarbutiba=izdzivvarbutiba+1
            
        if dbdati[3]=='Saule':
            for i in vidmakonudaudz:
                if i>80:
                    makonudaudz.append(i)
            
            if len(makonudaudz) == len(vidmakonudaudz):
                izdzivvarbutiba=izdzivvarbutiba+1
        
        if vidtemp[0]>30 and vidtemp[1]>30 and vidtemp[2]>30 and vidtemp[3]>30 and vidtemp[4]>30:
            izdzivvarbutiba=izdzivvarbutiba+1
        
        if vidvejaatr[2]>48:
            izdzivvarbutiba=izdzivvarbutiba+1
            
        if dLietussum[2]>330:
            izdzivvarbutiba=izdzivvarbutiba+1
        
        #varbutibas pielidzinasa
        if izdzivvarbutiba==0:
            izdziviesp='maksimalas'
        
        elif izdzivvarbutiba==1:
            izdziviesp='mazas'
        
        elif izdzivvarbutiba>=2:
            izdziviesp='nekadas'

    #laistisanas biezuma izmainu noteiksana
    if mitrums[2]<-1.5:
        biezums=dbdati[2]+1
    
    elif mitrums[0]<-1.5 and mitrums[1]<-1.5 and mitrums[2]<-1.5:
        biezums=dbdati[2]+2
    
    elif mitrums[0]<-1.5 and mitrums[1]<-1.5 and mitrums[2]<-1.5 and mitrums[3]<-1.5 and mitrums[4]<-1.5:
        biezums=dbdati[2]+3
    
    elif dNokriesp[2]<40:
        biezums=dbdati[2]+1
    
    elif dNokrlaiks[2]>12:
        biezums=0
    
    else:
        biezums=dbdati[2]
    
    #datu iegusana
    if nr==0:
        dirmapesast=sorted(os.listdir(dirmape), key=len)
        if len(dirmapesast)>0:
            num=[]
            pedfails=dirmapesast[-1]
            for i in pedfails:
                if i.isdigit():
                    num.append(i)
            
            num=''.join(num)
            auganr=int(num)
        
    else:
        auganr=nr
        
    dirfails=os.path.join(dirmape, f'{auganr}augs.json')
        
    jsonfails=open(dirfails, 'r+')
    jsondati=jsonfails.readlines()
    jsondati=jsondati[0]
    jsondati=json.loads(jsondati)
    jsonfails.close()
    
    atftzona=tzona.split('%2F')
    atftzona='/'.join(atftzona)
    atverlaiks=datetime.now(pytz.timezone(atftzona))
    atverlaiks=str(atverlaiks.strftime('%d/%m/%Y/%H:%M'))
    
    laiks1=atverlaiks
    laiks1=laiks1.split('/')
    laiks1diena=laiks1[0]
    laiks1menesis=laiks1[1]
    laiks1gads=laiks1[2]
    laiks1laiks=laiks1[-1]
    laiks1laiks=laiks1laiks.split(':')
    laiks1stunda=laiks1laiks[0]
    laiks1minute=laiks1laiks[-1]
    
    j=0
    for i in hLaiks:
        i=i.split('-')
        i=i[-1]
        i=i.split('T')
        laiks2diena=i[0]
        laiks2stunda=i[-1]
        laiks2stunda=laiks2stunda.split(':')
        laiks2stunda=laiks2stunda[0]
        
        if laiks2diena==laiks1diena and laiks2stunda==laiks1stunda:
            kartasnr=j
            break
        
        j=j+1
    
    #nokrisnu dati
    if hLetusdaudz[kartasnr]>=0.5:
        nokrveids='Smidzina'
        
    elif hLetusdaudz[kartasnr]>1:
        nokrveids='List'
    
    elif hLetusdaudz[kartasnr]>8:
        nokrveids='Lietusgazes'
    
    elif hMakonudaudz[kartasnr]>88:
        nokrveids='Makonains'
        
    elif hMakonudaudz[kartasnr]>=75:
        nokrveids='Parsvara makonains'
        
    elif hMakonudaudz[kartasnr]>=38:
        nokrveids='Nedaudz makonains'
        
    elif hMakonudaudz[kartasnr]>=13:
        nokrveids='Lielakoties saulains'
        
    else:
        nokrveids='Saulains'
        
    #veja dati
    vejaatrums=hVejaatr[kartasnr]
    
    if vejaatrums>61:
        vejastiprums='Loti stiprs'
    
    elif vejaatrums>40:
        vejastiprums='Stiprs'
    
    elif vejaatrums>13:
        vejastiprums='Videjs'
    
    elif vejaatrums>2:
        vejastiprums='Vajs'
        
    else:
        vejaatrums='Nav'
    
    
    if vejaatrums=='Nav':
        vejavirziens='Nav'
    
    else:
        vejavirziens=debespuse(hVejavirz[kartasnr])
    
    #augsanas dienu samazinasana
    laiks0=jsondati['iestadisanaslaiks']
    laiks0=laiks0.split('/')
    laiks0diena=laiks0[0]
    laiks0menesis=laiks0[1]
    laiks0gads=laiks0[2]
    laiks0laiks=laiks0[-1]
    laiks0laiks=laiks0laiks.split(':')
    laiks0stunda=laiks0laiks[0]
    laiks0minute=laiks0laiks[-1]

    dienas=int(jsondati['atlikusaisaugsanaslaiks'])
    if laiks0diena<laiks1diena and laiks0menesis<=laiks1menesis and laiks0gads<=laiks1gads:
        if laiks0stunda<=laiks1stunda and laiks0minute<=laiks1minute:
            atnemamais=int(laiks1diena)-int(laiks0diena)
            dienas=dienas-atnemamais
    
    #datu pievienosana failam
    jsondati['atversanaslaiks']=atverlaiks
    jsondati['atlikusaisaugsanaslaiks']=dienas
    jsondati['iedzivosanasiespeja']= izdziviesp
    jsondati['laistisanasbiezums']= biezums
    jsondati['nokrisnuveids']= nokrveids
    jsondati['vejaatrums']= vejaatrums
    jsondati['vejastiprums']= vejastiprums
    jsondati['vejavirziens']= vejavirziens
    
    jsonfails=open(dirfails, 'w')
    jsondati=json.dumps(jsondati)
    jsonfails.write(jsondati)
    jsonfails.close()
    

#MySql datu bazes savienosana
datubaze = mysql.connector.connect(
host="localhost",
user="root",
password="Skola12dit",
database="augudatubaze"
    
)

cursors=datubaze.cursor()

#galvenais loops 
while True:
    #globalie mainigie un kods
    mapesnosauk='augi'
    auganr=1

    dir= os.getcwd()
    dirsast=os.listdir(dir)
    dirmape=os.path.join(dir, mapesnosauk)

    dirsast=os.listdir(dir)
    if mapesnosauk not in dirsast: #"augi" mapes izveide, ja ta nepastav
        os.makedirs(dirmape)
        ctypes.windll.kernel32.SetFileAttributesW(dirmape, 0x02)

    dirmapesast=os.listdir(dirmape)

    #datu sifresanas atslega
    diratslega=os.path.join(dir, 'atslega.key')

    if 'atslega.key' not in dirsast:
        sifratslega=Fernet.generate_key()
        
        failsatslega=open(diratslega, 'wb')
        failsatslega.write(sifratslega)
        failsatslega.close()
        
        ctypes.windll.kernel32.SetFileAttributesW(diratslega, 0x02)
        
        if len(dirmapesast)>0:
            shutil.rmtree(dirmape)
            os.makedirs(dirmape)
            ctypes.windll.kernel32.SetFileAttributesW(dirmape, 0x02)
            print(''); print(''); print('')
            print('!!!! VISI DATI IZDZESTI SIFRATSLEGAS KOMPROMIZACIJAS DEL !!!!')
            print(''); print(''); print('')

    failsatslega=open(diratslega, 'rb')
    sifratslega=failsatslega.read()
    failsatslega.close()

    dirfails=os.path.join(dirmape, 'augs.json')

    #galvena programmas dala
    #saglabato augu sk parbaude
    dirmapesast=os.listdir(dirmape)
    
    #augu izvelne
    print('Opcijas: (ievadi nr)')
    print('1. Pievienot augu')
    if len(dirmapesast)>0:
        print('2. Augu izvelne')

    while True:
        opcija=input('> ')
        if opcija=='1':
            break
        
        if opcija=='2' and len(dirmapesast)>0:
            break
    
    if opcija=='1': #pievienosana
        print('')
        print('Ievadi nosaukumu: (lidz 200 rakstzimem)')
        while True:
            nosaukums=input('> ')
            if len(nosaukums)<=200:
                break
    
        print('')
        print('Ievadi atrasanas vietu: (Valsts-Pilseta (Anglu valoda))')
        O=0
        while 1>O:
            atrvieta=input('> ')
            atrvietas=atrvieta.split('-')
            if len(atrvietas)==2:
                pilseta=atrvietas[1]
                valsts=atrvietas[0]
                geoUrl=f"https://geocoding-api.open-meteo.com/v1/search?name={pilseta}"
                Dati=requests.get(geoUrl)
                Dati=Dati.json()
                Dati=Dati['results']
                for i in Dati:
                    j=i['country']
                    if j==valsts:
                        latitude=i['latitude']
                        longitude=i['longitude']
                        laikazona=i['timezone']
                        O=1
                        break
        
        flaikazona=laikazona.split('/')
        flaikazona='%2F'.join(flaikazona)
        
        #datu ieguve no datubazes
        
        while True:
            print('')
            print('Izvelies auga veidu: (ievadi nr)')
            sql='SELECT nosaukums, latiniskais_nosaukums FROM augi'
            cursors.execute(sql)
            dbdati=cursors.fetchall()
            
            auguskaits=[]
            j=0
            for i in dbdati:
                j=j+1
                auguskaits.append(str(j))
                print(f'{j}. {i[0]} ({i[1]})')
            
            while True:
                augaid=input('> ')
                if augaid in auguskaits:
                    sql=f"SELECT apraksts FROM augi WHERE id='{augaid}'"
                    cursors.execute(sql)
                    augadati=cursors.fetchall()
                    augadati=augadati[0]
                    print('')
                    print(f'Auga apraksts: {augadati[0]}')
                    print('')
                    print('Apstiprinat (Y/N)')
                    while True:
                        apstiprinajums=input('> ')
                        if apstiprinajums=='Y' or apstiprinajums=='y':
                            break
                        
                        if apstiprinajums=='N' or apstiprinajums=='n':
                            break
                    
                    break
            
            if apstiprinajums=='Y' or apstiprinajums=='y':
                break
    
    if opcija!='2':
        sql=f"SELECT nosaukums, augsanas_ilgums, latiniskais_nosaukums FROM augi WHERE id='{augaid}'"
        cursors.execute(sql)
        augadati=cursors.fetchall()
        augadati=augadati[0]
        
        augaid=int(augaid)
        auganosauk=augadati[0]
        augilgums=int(augadati[1])
        augalatinnosauk=augadati[2]
        iestadlaiks=datetime.now(pytz.timezone(laikazona))
        iestadlaiks=str(iestadlaiks.strftime('%d/%m/%Y/%H:%M'))
            
        saglabasana(nosaukums, atrvieta, latitude, longitude, flaikazona, auganosauk, augalatinnosauk, augaid, iestadlaiks, augilgums)
        laikapstakli(latitude, longitude, flaikazona)
        
        print('')
        print(f'Auga "{auganosauk}" ieraksts veiksmigi izveidots')
    
    if opcija=='2': #atversana
        atversana()
        
    print('')
    print('')
    print('')