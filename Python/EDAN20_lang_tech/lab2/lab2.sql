DROP TABLE IF EXISTS theatres;
CREATE TABLE theatres(
	th_name		TEXT PRIMARY KEY,
	capacity	INT
);

DROP TABLE IF EXISTS movies;
CREATE TABLE movies(
	title		TEXT,
	year		INT,
	imdb_key	TEXT,
	length		INT,
	PRIMARY KEY (title, year)
);

DROP TABLE IF EXISTS customers;
CREATE TABLE customers(
	usr_name	TEXT PRIMARY KEY,
	full_name	TEXT NOT NULL,
	password	TEXT NOT NULL
);

DROP TABLE IF EXISTS performances; 
CREATE TABLE performances(
	screen_date	DATE,
	start_time	TIME,
	th_name		TEXT,
	title		TEXT NOT NULL,
	year		INT NOT NULL,
	PRIMARY KEY (th_name, title, year, screen_date, start_time),
	FOREIGN KEY (th_name) REFERENCES theatres(th_name),
	FOREIGN KEY (title, year) REFERENCES movies(title, year)
);

DROP TABLE IF EXISTS tickets;
CREATE TABLE tickets(
	t_id		TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
	th_name		TEXT NOT NULL,
	title		TEXT NOT NULL,
	year		INT NOT NULL,
	screen_date	DATE NOT NULL,
	start_time	TIME NOT NULL,
	usr_name	TEXT,
	FOREIGN KEY (th_name) REFERENCES theatres(th_name),
	FOREIGN KEY (title, year) REFERENCES movies(title, year),
	FOREIGN KEY (th_name, title, year, screen_date, start_time) REFERENCES performances(th_name, title, year, screen_date, start_time),
	FOREIGN KEY (usr_name) REFERENCES customers(usr_name)
);

INSERT
INTO 	theatres(th_name, capacity)
VALUES	('Lund', 150),
		('Malmö', 200),
		('Landskrona', 120),
		('Helsingborg', 150);
	
INSERT
INTO	customers(usr_name, full_name, password)
VALUES	('lemur', 'Anna Ek', 'qwe123'),
		('wildcat', 'Jonny Balle', 'asdfgh'),
		('bison', 'Kim Jong Un', 'rocketman'),
		('greyhound', 'Angela merkel', 'zxcvbnm');

INSERT
INTO	movies(title, year, imdb_key, length)
VALUES	('The Shawshank Redemption', 1994, 'tt0111161', 142),
		('The Godfather', 1972, 'tt0068646', 175),
		('The Dark Knight', 2008, 'tt0468569', 152),
		('Pulp Fiction', 1994, 'tt0110912', 154),
		('The Lord of the Rings: The Fellowship of the Ring', 2001, 'tt0120737', 178);
		

WITH performance_data(title, year, screen_date, start_time, th_name) AS (
	VALUES	('The Shawshank Redemption', 1994, '2021-02-11', '19:30', 'Lund'),
			('The Shawshank Redemption', 1994, '2021-02-12', '19:00', 'Lund'),
			('The Shawshank Redemption', 1994, '2021-02-11', '18:00', 'Malmö'),
			('The Shawshank Redemption', 1994, '2021-02-11', '20:30', 'Malmö'),
			('The Shawshank Redemption', 1994, '2021-02-12', '18:00', 'Malmö'),
			('The Shawshank Redemption', 1994, '2021-02-12', '20:30', 'Malmö'),
			('The Shawshank Redemption', 1994, '2021-02-11', '19:30', 'Landskrona'),
			('The Shawshank Redemption', 1994, '2021-02-11', '19:30', 'Helsingborg'),
			('The Godfather', 1972, '2021-02-11', '21:00', 'Lund'),
			('The Godfather', 1972, '2021-02-12', '20:30', 'Lund'),
			('The Godfather', 1972, '2021-02-13', '21:00', 'Malmö'),
			('The Godfather', 1972, '2021-02-14', '21:00', 'Malmö'),
			('The Godfather', 1972, '2021-02-12', '20:30', 'Landskrona'),
			('The Godfather', 1972, '2021-02-12', '20:30', 'Helsingborg'),
			('Pulp Fiction', 1994, '2021-02-13', '18:00', 'Lund'),
			('Pulp Fiction', 1994, '2021-02-13', '21:00', 'Lund'),
			('Pulp Fiction', 1994, '2021-02-13', '18:00', 'Malmö'),
			('Pulp Fiction', 1994, '2021-02-13', '20:00', 'Landskrona'),
			('Pulp Fiction', 1994, '2021-02-13', '20:00', 'Helsingborg'),
			('The Lord of the Rings: The Fellowship of the Ring', 2001, '2021-02-14', '15:00', 'Lund'),
			('The Lord of the Rings: The Fellowship of the Ring', 2001, '2021-02-14', '18:00', 'Lund'),
			('The Lord of the Rings: The Fellowship of the Ring', 2001, '2021-02-14', '21:00', 'Lund'),
			('The Lord of the Rings: The Fellowship of the Ring', 2001, '2021-02-14', '17:30', 'Malmö')
)

INSERT
INTO	performances(title, year, screen_date, start_time, th_name)
	SELECT m.title, m.year, pd.screen_date, pd.start_time, th.th_name
	FROM performance_data pd
	JOIN movies m ON m.title = pd.title AND m.year = pd.year
	JOIN theatres th ON th.th_name = pd.th_name
;

	
WITH ticket_data(t_id, th_name, title, year, screen_date, start_time, usr_name) AS (
	VALUES	(lower(hex(randomblob(16))), 'Lund', 'The Shawshank Redemption', 1994, '2021-02-11', '19:30', 'lemur'),
			(lower(hex(randomblob(16))), 'Lund', 'The Shawshank Redemption', 1994, '2021-02-11', '19:30', 'wildcat'),
			(lower(hex(randomblob(16))), 'Lund', 'The Shawshank Redemption', 1994, '2021-02-11', '19:30', 'bison'),
			(lower(hex(randomblob(16))), 'Lund', 'The Shawshank Redemption', 1994, '2021-02-12', '19:00', 'greyhound')
)
INSERT
INTO	tickets(t_id, th_name, title, year, screen_date, start_time, usr_name)
	SELECT	td.t_id, td.th_name, td.title, td.year, td.screen_date, td.start_time, td.usr_name
	FROM	ticket_data td
	JOIN	performances p ON p.th_name = td.th_name AND p.screen_date = td.screen_date AND p.start_time = td.start_time
;
	
