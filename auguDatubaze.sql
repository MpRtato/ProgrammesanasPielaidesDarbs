#Augu datubazes kods

#Datubazes koda licencesana
#autors: Arts Inarts Kubilis
#licence: CC BY-NC-ND 4.0 (https://creativecommons.org/licenses/by-nc-nd/4.0/)

#datubazes izveidosana un izvelesanas
CREATE DATABASE augudatubaze;

USE augudatubaze;

#datubazes tabulu un ailu izveidosana
CREATE TABLE augi(
  id int PRIMARY KEY AUTO_INCREMENT NOT NULL,
  nosaukums varchar(200) NOT NULL,
  latiniskais_nosaukums varchar(200) UNIQUE NOT NULL,
  skirne varchar(200) NOT NULL,
  apraksts varchar(1000) NOT NULL,
  veids varchar(100) NOT NULL,
  augsanas_ilgums int NOT NULL,
  dzivesilgums varchar(20) NOT NULL,
  izturiba varchar(20) NOT NULL,
  saknu_dzilums int NOT NULL,
  stadisanas_menesis varchar(20) NOT NULL,
  minimala_temperatura int NOT NULL,
  laistisanas_biezums int NOT NULL,
  gaismas_vide varchar(20) NOT NULL,
  vide varchar(100) NOT NULL

);

CREATE TABLE atsauces(
  id int PRIMARY KEY AUTO_INCREMENT NOT NULL,
  atsauce varchar(1000) NOT NULL

);

CREATE TABLE augi_atsauce(
auga_id int,
atsauces_Id int,

FOREIGN KEY(auga_id) REFERENCES augi(id),
FOREIGN KEY(atsauces_id) REFERENCES atsauces(id)

);