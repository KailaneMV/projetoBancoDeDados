import sqlite3
con = sqlite3.connect('baseDeDados.db') 
cur = con.cursor() 

sql = """
    CREATE TABLE funcionarios(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    sobrenome TEXT NOT NULL,
                    cpf INTEGER NOT NULL,
                    tempoDeServico INTEGER NOT NULL,
                    remuneracao FLOAT NOT NULL)

"""
cur.execute(sql)
con.commit() 
con.close()