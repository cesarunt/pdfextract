BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"email"	VARCHAR(100),
	"password"	VARCHAR(100),
	"name"	VARCHAR(1000),
	PRIMARY KEY("id"),
	UNIQUE("email")
);
CREATE TABLE IF NOT EXISTS "pdf_attributes" (
	"att_id"	INTEGER,
	"att_name"	TEXT,
	"att_fecha"	TEXT,
	PRIMARY KEY("att_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "pdf_details" (
	"det_id"	INTEGER,
	"det_info"	INTEGER,
	"det_attribute"	INTEGER,
	"det_value"	TEXT,
	"det_npage"	INTEGER,
	"det_x"	INTEGER,
	"det_y"	INTEGER,
	"det_width"	INTEGER,
	"det_height"	INTEGER,
	PRIMARY KEY("det_id" AUTOINCREMENT),
	FOREIGN KEY("det_attribute") REFERENCES "pdf_attributes"("att_id"),
	FOREIGN KEY("det_info") REFERENCES "pdf_info"("pdf_id")
);
CREATE TABLE IF NOT EXISTS "pdf_info" (
	"pdf_id"	INTEGER,
	"pdf_name"	TEXT UNIQUE,
	"pdf_npages"	INTEGER,
	"pdf_size"	REAL,
	"pdf_created"	TEXT,
	PRIMARY KEY("pdf_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "key_info" (
	"key_id"	INTEGER,
	"key_name"	TEXT,
	"key_created"	TEXT,
	PRIMARY KEY("key_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "uni_info" (
	"uni_id"	INTEGER,
	"uni_name"	TEXT UNIQUE,
	"uni_nickname"	TEXT,
	"uni_city"	TEXT,
	"uni_created"	TEXT,
	PRIMARY KEY("uni_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "project_info" (
	"pro_id"	INTEGER,
	"pro_title"	TEXT,
	"pro_uni"	INTEGER,
	"pro_career"	TEXT,
	"pro_key_id1"	INTEGER,
	"pro_key_id2"	INTEGER,
	"pro_key_id3"	INTEGER,
	"pro_type"	TEXT,
	"pro_n_articles"	INTEGER,
	"pro_n_process"	INTEGER,
	"pro_created"	TEXT,
	PRIMARY KEY("pro_id"),
	FOREIGN KEY("pro_uni") REFERENCES "uni_info"("uni_id")
);
CREATE TABLE IF NOT EXISTS "pro_key_details" (
	"pro_key_id"	INTEGER,
	"pro_id"	INTEGER,
	"key_id"	INTEGER,
	"pro_key_created"	TEXT,
	PRIMARY KEY("pro_key_id"),
	FOREIGN KEY("pro_id") REFERENCES "project_info"("pro_id"),
	FOREIGN KEY("key_id") REFERENCES "key_info"("key_id")
);
CREATE TABLE IF NOT EXISTS "pdf_key_details" (
	"pdf_key_id"	INTEGER,
	"pdf_id"	INTEGER,
	"key_id"	INTEGER,
	"pdf_key_created"	TEXT,
	PRIMARY KEY("pdf_key_id" AUTOINCREMENT),
	FOREIGN KEY("pdf_id") REFERENCES "pdf_info"("pdf_id"),
	FOREIGN KEY("key_id") REFERENCES "key_info"("key_id")
);
INSERT INTO "user" VALUES (1,'cesarunt@gmail.com','sha256$MGpnfRZFSSdUvMvQ$49eacbac0dc06220a46f71bdc15734891634d6961a28017a6a7e88bfa4f85d17','Cesar Peña');
INSERT INTO "pdf_attributes" VALUES (1,'autor','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (2,'titulo','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (3,'entidad','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (4,'resumen','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (5,'año','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (6,'portada','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (7,'dedicatoria','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (8,'indice','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (9,'introducción','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (10,'objetivo','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (11,'marco','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (12,'hypotesis','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (13,'metodología','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (14,'discusión','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (15,'resultados','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (16,'conclusiones','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (17,'referencias','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (18,'anexo','2021/12/11 10:00:00');
INSERT INTO "pdf_attributes" VALUES (19,'adicional','2021/12/11 10:00:00');
INSERT INTO "pdf_details" VALUES (0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pdf_details" VALUES (1,1,1,'',1,35,28,115,18);
INSERT INTO "pdf_details" VALUES (2,1,2,'WILEY
',1,466,58,98,37);
INSERT INTO "pdf_details" VALUES (3,1,3,'...',1,'','','','');
INSERT INTO "pdf_details" VALUES (4,1,4,'Bor nies
',1,45,49,122,19);
INSERT INTO "pdf_details" VALUES (5,1,5,'...',1,'','','','');
INSERT INTO "pdf_details" VALUES (7,1,6,'Explaining stock markets’ performance
',1,'','','','');
INSERT INTO "pdf_details" VALUES (8,1,7,'...',4,'','','','');
INSERT INTO "pdf_details" VALUES (9,1,8,'...',5,'','','','');
INSERT INTO "pdf_details" VALUES (10,1,9,'...',5,'','','','');
INSERT INTO "pdf_details" VALUES (11,1,10,'Acta 2 Nov 2020
',1,40,25,129,30);
INSERT INTO "pdf_details" VALUES (12,1,11,'...',10,'','','','');
INSERT INTO "pdf_details" VALUES (13,1,12,'...',10,'','','','');
INSERT INTO "pdf_details" VALUES (14,1,13,'...',13,'','','','');
INSERT INTO "pdf_details" VALUES (15,1,14,'...',14,'','','','');
INSERT INTO "pdf_details" VALUES (16,1,15,'',16,'','','','');
INSERT INTO "pdf_details" VALUES (17,1,16,'...',17,'','','','');
INSERT INTO "pdf_details" VALUES (18,1,17,'...',19,'','','','');
INSERT INTO "pdf_details" VALUES (19,1,18,'...',20,'','','','');
INSERT INTO "pdf_details" VALUES (23,5,1,'...',1,'','','','');
INSERT INTO "pdf_details" VALUES (24,5,2,'Service quality measurement: the case of the Guarantee
Court from the city of Puerto Monti - Chile
',1,112,144,345,48);
INSERT INTO "pdf_details" VALUES (25,5,3,'...',1,'','','','');
INSERT INTO "pdf_details" VALUES (26,5,4,'...',1,'','','','');
INSERT INTO "pdf_details" VALUES (27,5,5,'...',2,'','','','');
INSERT INTO "pdf_details" VALUES (28,5,6,'...',3,'','','','');
INSERT INTO "pdf_details" VALUES (29,5,7,'','','','','','');
INSERT INTO "pdf_details" VALUES (30,5,8,'...',6,'','','','');
INSERT INTO "pdf_details" VALUES (31,5,9,'...',7,'','','','');
INSERT INTO "pdf_details" VALUES (32,5,10,'','','','','','');
INSERT INTO "pdf_details" VALUES (33,5,11,'',9,'','','','');
INSERT INTO "pdf_details" VALUES (34,5,12,'....',13,'','','','');
INSERT INTO "pdf_details" VALUES (35,5,13,'...',14,'','','','');
INSERT INTO "pdf_details" VALUES (36,5,14,'...',16,'','','','');
INSERT INTO "pdf_details" VALUES (37,5,15,'...',19,'','','','');
INSERT INTO "pdf_details" VALUES (38,5,16,'...',22,'','','','');
INSERT INTO "pdf_details" VALUES (39,5,17,'...',23,'','','','');
INSERT INTO "pdf_details" VALUES (40,5,18,'...',25,'','','','');
INSERT INTO "pdf_details" VALUES (41,6,1,'...',1,'','','','');
INSERT INTO "pdf_details" VALUES (42,6,2,'(QUALITY OF SERVICE AND CUSTOMER SATISFACTION IN
THE SERVICES SECTOR MSE « ITEM 3 STAR HOTELS
DISTRICT PIURA, 2015
',1,81,271,429,70);
INSERT INTO "pdf_details" VALUES (43,6,3,'...',1,'','','','');
INSERT INTO "pdf_details" VALUES (44,6,4,'...',1,'','','','');
INSERT INTO "pdf_details" VALUES (45,6,5,'','','','','','');
INSERT INTO "pdf_details" VALUES (46,6,6,'...',3,'','','','');
INSERT INTO "pdf_details" VALUES (47,6,7,'...',4,'','','','');
INSERT INTO "pdf_details" VALUES (48,6,8,'','','','','','');
INSERT INTO "pdf_details" VALUES (49,6,9,'....',6,'','','','');
INSERT INTO "pdf_details" VALUES (50,6,10,'...',7,'','','','');
INSERT INTO "pdf_details" VALUES (51,6,11,'...',9,'','','','');
INSERT INTO "pdf_details" VALUES (52,6,12,'...',11,'','','','');
INSERT INTO "pdf_details" VALUES (53,6,13,'','','','','','');
INSERT INTO "pdf_details" VALUES (54,6,14,'...',13,'','','','');
INSERT INTO "pdf_details" VALUES (55,6,15,'...',15,'','','','');
INSERT INTO "pdf_details" VALUES (56,6,16,'...',18,'','','','');
INSERT INTO "pdf_details" VALUES (57,6,17,'','','','','','');
INSERT INTO "pdf_details" VALUES (58,6,18,'....',24,'','','','');
INSERT INTO "pdf_info" VALUES (1,'id1_isaf1499.pdf',9,3.2,'2021/11/14 16:59:00');
INSERT INTO "pdf_info" VALUES (2,'id2_bse.2683.pdf',13,1.7,'2021/11/14 17:01:00');
INSERT INTO "pdf_info" VALUES (3,'id3_36725679003.pdf',32,0.23,'2021/11/14 17:05:00');
INSERT INTO "pdf_info" VALUES (4,'id4_SSRN-id2459293.pdf',156,1.0,'2021/11/14 17:06:00');
INSERT INTO "pdf_info" VALUES (5,'id5_10._GangaContreras-AlarconHenriquez_2019.pdf',14,0.63,'2021/11/14 17:07:00');
INSERT INTO "pdf_info" VALUES (6,'id6_1._Arias-Munoz2019.pdf',7,0.12,'2021/11/16 17:12:00');
INSERT INTO "pdf_info" VALUES (7,'id7_10._Thanh.pdf',11,0.43,'2021/11/16 17:14:00');
INSERT INTO "pdf_info" VALUES (8,'id8_1._Suciptawati.pdf',7,1.2,'2021/11/16 17:14:50');
INSERT INTO "pdf_info" VALUES (9,'id9_FabioCastro_PaolaUlloa_TrabajodeInvestigacion_Bachiller_2019.pdf',59,3.9,'2021/11/16 17:15:30');
INSERT INTO "key_info" VALUES (1,'calidad del servicio','');
INSERT INTO "key_info" VALUES (2,'satisfacción del cliente','');
INSERT INTO "key_info" VALUES (3,'marketing','');
INSERT INTO "key_info" VALUES (4,'publicidad','');
INSERT INTO "key_info" VALUES (5,'economía','');
INSERT INTO "key_info" VALUES (6,'planificación estratégica','');
INSERT INTO "key_info" VALUES (7,'desarrollo organizacional','');
INSERT INTO "key_info" VALUES (8,'empresas tecnológicas','');
INSERT INTO "key_info" VALUES (9,'informática','');
INSERT INTO "key_info" VALUES (10,'educación','');
INSERT INTO "key_info" VALUES (11,'sistemas de gestión','');
INSERT INTO "key_info" VALUES (12,'contabilidad de gestión','');
INSERT INTO "key_info" VALUES (13,'servicios públicos','');
INSERT INTO "key_info" VALUES (14,'limpieza pública','');
INSERT INTO "key_info" VALUES (15,'gestión pública','');
INSERT INTO "uni_info" VALUES (1,'Universidad Peruana de Ciencias Aplicadas','UPC','Lima','');
INSERT INTO "uni_info" VALUES (2,'Universidad Nacional de Ingeniería','UNI','Lima','');
INSERT INTO "uni_info" VALUES (3,'Universidad Nacional Mayor de San Marcos','UNMSM','Lima','');
INSERT INTO "uni_info" VALUES (4,'Universidad Cesar Vallejo','UCV','Trujillo','');
INSERT INTO "uni_info" VALUES (5,'Universidad Nacional de Trujillo','UNT','Trujillo','');
INSERT INTO "uni_info" VALUES (6,'Universidad Nacional de Chiclayo','UNCH','Chiclayo','');
INSERT INTO "uni_info" VALUES (7,'Universidad Nacional de Piura','UNP','Piura','');
INSERT INTO "project_info" VALUES (1,'Satisfacción de clientes en empresas tecnológicas ',1,'Economía','','','','A',0,0,'08/01/2022');
INSERT INTO "project_info" VALUES (2,'Planificación estratégica en empresas tecnológicas ',3,'Marketing','','','','A',0,0,'08/01/2022');
INSERT INTO "project_info" VALUES (3,'Calidad del servicio en empresas tecnológicas ',5,'Informática','','','','A',0,0,'08/01/2022');
INSERT INTO "project_info" VALUES (4,'Desarrollo y satisfacción de clientes en Lima',4,'Social','','','','A',0,0,'08/01/2022');
INSERT INTO "project_info" VALUES (5,'Publicidad y satisfcción de clientes en Lima',4,'Derecho','','','','A',0,0,'08/01/2022');
INSERT INTO "project_info" VALUES (6,'Marketing y satisfcción de clientes en Lima',4,'Social','','','','A',0,0,'08/01/2022');
INSERT INTO "project_info" VALUES (7,'Planificación de las organizaciones ',5,'Administración','','','','A',0,0,'08/01/2022');
INSERT INTO "project_info" VALUES (8,'Planificación tecnológica en empresas TI ',2,'Informática','','','','A',0,0,'08/01/2022');
INSERT INTO "project_info" VALUES (9,'Planificación tecnológica en el sector educativo',2,'Administración','','','','A',0,0,'09/01/2022');
INSERT INTO "project_info" VALUES (10,'Satisfacción de clientes usando herramientas científicas',1,'Informática','','','','A',0,0,'09/01/2022');
INSERT INTO "project_info" VALUES (11,'Implementación de servicios de calidad en el sector comercial de Lima Metropolitana ',3,'Marketing','','','','A',0,0,'09/01/2022');
INSERT INTO "project_info" VALUES (12,'Actualización y planificación del modelo educativo 2022 ',3,'Educación','','','','A',4,3,'10/01/2022');
INSERT INTO "project_info" VALUES (13,'Mejoramiento de la educación usando nuevas herramientas TI ',4,'Marketing','','','','A',2,1,'10/01/2022');
INSERT INTO "project_info" VALUES (15,'Mejoramiento de la educación pública con tecnologías Cloud ',2,'Educación','','','','A',0,0,'10/01/2022');
INSERT INTO "project_info" VALUES (16,'Proyectos de limpieza pública, periodo 2022 ',5,'Ing. Civil','','','','A',4,1,'10/01/2022');
INSERT INTO "pro_key_details" VALUES (1,1,1,'10-01-2021');
INSERT INTO "pro_key_details" VALUES (2,1,2,'10-01-2021');
INSERT INTO "pdf_key_details" VALUES (1,1,2,'');
INSERT INTO "pdf_key_details" VALUES (2,1,4,'');
INSERT INTO "pdf_key_details" VALUES (3,1,7,'');
INSERT INTO "pdf_key_details" VALUES (4,2,1,'');
INSERT INTO "pdf_key_details" VALUES (5,2,5,'');
INSERT INTO "pdf_key_details" VALUES (6,2,7,'');
INSERT INTO "pdf_key_details" VALUES (7,3,3,'');
INSERT INTO "pdf_key_details" VALUES (8,3,4,'');
INSERT INTO "pdf_key_details" VALUES (9,4,5,'');
INSERT INTO "pdf_key_details" VALUES (10,4,6,'');
INSERT INTO "pdf_key_details" VALUES (11,5,9,'');
INSERT INTO "pdf_key_details" VALUES (12,5,10,'');
INSERT INTO "pdf_key_details" VALUES (13,6,1,'');
INSERT INTO "pdf_key_details" VALUES (14,6,2,'');
INSERT INTO "pdf_key_details" VALUES (15,6,4,'');
INSERT INTO "pdf_key_details" VALUES (16,7,2,'');
INSERT INTO "pdf_key_details" VALUES (17,7,4,'');
INSERT INTO "pdf_key_details" VALUES (18,7,6,'');
INSERT INTO "pdf_key_details" VALUES (19,8,1,'');
INSERT INTO "pdf_key_details" VALUES (20,8,3,'');
INSERT INTO "pdf_key_details" VALUES (21,8,9,'');
COMMIT;
