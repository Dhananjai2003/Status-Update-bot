import sqlite3
import datetime
from unicodedata import name


#database -> members (name text,status text,cat text,pending int)
#log -> ('user','time','status')

def add_members(name_user,cata): #implimented

    data = (str(name_user),'pending',str(cata),0,)
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM members WHERE name=? AND cat=? ",(str(name_user),str(cata),))

    conn.commit()

    if len(cur.fetchall())==0:
        cur.execute("INSERT INTO members VALUES (?,?,?,?);", data)
        conn.commit()
        conn.close()
        return False
    else:
        conn.commit()
        conn.close()
        return True


def remove_members(name,cat): #implimented
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM members WHERE name=? AND cat=?",(str(name),str(cat),))

    conn.commit()
    conn.close()


def start_round(author): #untested implimented
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    x = datetime.datetime.now()

    cur.execute("""UPDATE members SET pending=pending+1 WHERE status='pending';""")
    cur.execute("""UPDATE members SET status='pending';""")

    # conn.commit()

    cur.execute("INSERT INTO log VALUES (?,?,?);",(str(author),str(x.strftime("%x")),'running'))

    conn.commit()
    conn.close()


def stop_round(): # untested implimented
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("UPDATE log SET status='terminated' WHERE status='running'")

    cur.execute("UPDATE members SET pending=pending+1 WHERE status='pending'")

    conn.commit()
    conn.close()


def show_status(): #untested #implimented
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT name,status FROM members")

    name_list = cur.fetchall()

    conn.commit()
    conn.close()

    return name_list


def show_pending(pending): # untested # implimented
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT name,cat,pending FROM members WHERE pending>=?;",(pending))

    name_list = cur.fetchall()

    return name_list

    conn.commit()
    conn.close()
        

def check_round_author(author): #untested # implimented
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT user FROM log WHERE status='running'")

    if cur.fetchall()[0][0]==str(author):
        conn.commit()
        conn.close()
        return True
    
    conn.commit()
    conn.close()
    return False


def check_round_active(): #untested #implimented
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT user FROM log WHERE status='running'")

    if len(cur.fetchall())!=0:
        conn.commit()
        conn.close()
        return True
    
    conn.commit()
    conn.close()

    return False


def update(name):
    conn = sqlite3.connect("database.db")

    cur = conn.cursor()

    cur.execute("UPDATE members SET pending=0, status='completed' WHERE name=?;" ,(str(name),))

    conn.commit()

    conn.close()
