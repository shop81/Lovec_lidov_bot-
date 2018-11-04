import sqlite3

def add_id(arg):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (id, words, time_date, groups) VALUES (?, ?, 0, ?)',
                   (arg, '', ''))
    conn.commit()
    cursor.close()
    conn.close()
    f = open('admins.txt', 'a')
    f.write(arg)
    f.close()


def add_words(user_id, word):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT words FROM users WHERE id=:user_id',
                   {'user_id': user_id})
    words = str(cursor.fetchone()[0]) + word + ','
    cursor.execute('UPDATE users SET words=:words WHERE id=:user_id',
                   {'words':words, 'user_id':user_id})
    conn.commit()
    cursor.close()
    conn.close()

def collect_words(user_id):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT words FROM users WHERE id=:user_id',
                   {'user_id': user_id})
    words = str(cursor.fetchone()[0])
    conn.commit()
    cursor.close()
    conn.close()
    return words.split(',')[:-1]

def delete_words(user_id, word):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT words FROM users WHERE id=:user_id',
                   {'user_id': user_id})
    words = str(cursor.fetchone()[0])

    words1 = words.split(',')
    words = ''
    for i in words1:
        if i != word and i != '':
            words+=i + ','
    cursor.execute('UPDATE users SET words=:words WHERE id=:user_id',
                   {'words': words, 'user_id': user_id})
    conn.commit()
    cursor.close()
    conn.close()

def delete_id(user_id):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id=:user_id',
                   {'user_id': user_id})
    conn.commit()
    cursor.close()
    conn.close()


def collect_All_words():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT words FROM users ')
    words = cursor.fetchall()
    word = ''
    for i in words:
        word += i[0]
    conn.commit()
    cursor.close()
    conn.close()
    return word.split(',')[:-1]

def collect_All_id():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users ')
    words = cursor.fetchall()
    word = []
    conn.commit()
    cursor.close()
    conn.close()
    for i in words:
        word.append( i[0])
    return word

def incert_date(user_id, datet):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET time_date=:detet WHERE id=:user_id',
                   {'detet': datet, 'user_id': user_id})
    conn.commit()
    cursor.close()
    conn.close()


def all_about_all(mes):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users ')
    words = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    ai = []
    for i in words:
        if mes in i[1].split(','):
            ai.append(i[0])

    return ai

def all_licience():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, time_date FROM users ')
    words = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return words

def all_groups():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, groups, words FROM users ')
    words = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return words

def add_group(user_id, word):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT groups FROM users WHERE id=:user_id',
                   {'user_id': user_id})
    words = str(cursor.fetchone()[0])
    if word not in words.split(','):
        words += word + ','
    cursor.execute('UPDATE users SET groups=:words WHERE id=:user_id',
                       {'words':words, 'user_id':user_id})
    conn.commit()
    cursor.close()
    conn.close()