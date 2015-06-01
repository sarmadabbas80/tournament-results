-- Table definitions for the tournament project.

-- 3 tables to get the tournament application to work have been created. These are:
—- Players, Matches and Playerstandings. 

—- I also created Tournament and SwissPairing tables but did not use them and so they have —- been commented out. The Tournament table was for extra credit to allow to register a  —— tournament but I was not able to get to this. Swisspairing table was setup to help in —- getting the swissPairing method login but I shifted focus from using this approach.

—- CREATE TABLE tournaments (
—— tournamentID SERIAL,
—— tournamentname VARCHAR(100),
-- tournamenttype VARCHAR(100));

CREATE TABLE players (
playerID SERIAL,
playername VARCHAR(100));
—- tournamentID INTEGER);

CREATE TABLE matches(
matchID SERIAL,
winnerID INTEGER,
loserID INTEGER);

CREATE TABLE playerstanding(
playerid INTEGER,
playername varchar(100),
wins integer,
matches integer);

—- CREATE TABLE swisspairing(
-— playerid1  INTEGER,
-- playername1 varchar(100),
—- playerid2 INTEGER,
—- playername2 varchar(100));