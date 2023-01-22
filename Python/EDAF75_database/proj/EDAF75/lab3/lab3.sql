PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS theatres;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS performances; 
DROP TABLE IF EXISTS tickets;

PRAGMA foreign_keys=ON;


CREATE TABLE theatres(
	th_name		TEXT PRIMARY KEY,
	capacity	INT
);

CREATE TABLE movies(
	imdb_key	TEXT PRIMARY KEY,
	title		TEXT,
	year		INT,
	length		INT
);

CREATE TABLE customers(
	usr_name	TEXT PRIMARY KEY,
	full_name	TEXT NOT NULL,
	password	TEXT NOT NULL
);

CREATE TABLE performances(
	p_id		TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
	screen_date	DATE,
	start_time	TIME,
	th_name		TEXT,
	imdb_key	TEXT NOT NULL,
	FOREIGN KEY (th_name) REFERENCES theatres(th_name),
	FOREIGN KEY (imdb_key) REFERENCES movies(imdb_key)
);


CREATE TABLE tickets(
	t_id		TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
	p_id		TEXT NOT NULL,
	usr_name	TEXT,
	FOREIGN KEY (p_id) REFERENCES performances(p_id),
	FOREIGN KEY (usr_name) REFERENCES customers(usr_name)
);


INSERT
INTO 	theatres(th_name, capacity)
VALUES ('Kino', 9), ('Regal', 16), ('Skandia', 100);

