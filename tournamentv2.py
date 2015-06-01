#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE from matches;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE from players;")
    conn.commit()
    cursor.execute("DELETE from playerstanding;")
    conn.commit()
    cursor.execute("DELETE from swisspairing;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) as count from players;")
    result = cursor.fetchone()
    numberofrows = result[0]
    return numberofrows    
    conn.close()
    

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT into players(playername) values (%s)",(name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""INSERT into playerstanding(playerid,playername)
            (SELECT p.playerID, p.playername from players p 
            GROUP BY p.playerid,p.playername);""")
    conn.commit()
    cursor.execute("""UPDATE playerstanding SET wins = (SELECT count(winnerID) from matches
                    where matches.winnerID  = playerstanding.playerid);
                    """)
    conn.commit()
    cursor.execute("""UPDATE playerstanding SET matches = (SELECT count(matchID) from matches
                    where matches.winnerID  = playerstanding.playerid
                    or matches.loserID  = playerstanding.playerid);
                    """)
    conn.commit()
    cursor.execute("SELECT * from playerstanding order by wins desc;")               
    standings = cursor.fetchall()
    return standings    
    conn.close()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT into matches(winnerID, loserID) values (%s,%s)",(winner,loser))
    cursor.execute("""UPDATE playerstanding SET wins = (SELECT count(winnerID) from matches
                    where matches.winnerID  = playerstanding.playerid);
                    """)
    conn.commit()
    cursor.execute("""UPDATE playerstanding SET matches = (SELECT count(matchID) from matches
                    where matches.winnerID  = playerstanding.playerid
                    or matches.loserID  = playerstanding.playerid);
                    """)
    conn.commit()
    conn.close()

     
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""SELECT p.playerid, p.playername from playerstanding p
                    where wins = 1;""")
    fetch1 = cursor.fetchall()
    for row in fetch1:
        pid1 = (row[0])
        pname1 = (row[1])
        cursor.execute("""INSERT into swisspairing(playerid1, playername1)
                    values (%s,%s)""",(pid1,pname1))
        conn.commit()
    cursor.execute("""SELECT p.playerid, p.playername from playerstanding p
                    where wins = 0;""")
    fetch2 = cursor.fetchall()
    for row in fetch2:
        pid2 = (row[0])
        pname2 = (row[1])
        cursor.execute("UPDATE swisspairing SET playerid2 = (%s)", [pid2])
        conn.commit()
        cursor.execute("UPDATE swisspairing SET playername2 = (%s)", [pname2])
        conn.commit()
    cursor.execute("""SELECT * from swisspairing""")
    results = cursor.fetchall()
    return results
    conn.close()


