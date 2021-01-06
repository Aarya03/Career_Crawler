CREATE TABLE SearchData(
	id int,
	name varchar(100),
	website varchar(30),
	type varchar(30),
	PRIMARY KEY(id));

LOAD DATA LOCAL INFILE 'C:\Users\Aaryavart Joshi\Downloads\Institutes (2).csv' INTO TABLE searchdata
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'  
(@col1,@col2,@col3,@col4,@col5,@col6,@col7,@col8) set id=@col1,name=@col2,website=@col3,type=@col4 ;