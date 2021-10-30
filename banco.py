from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine('sqlite:///dados.db')

def cria_tabela():
    with engine.connect() as con:
        create_tabela_produtos = text (
            """CREATE TABLE IF NOT EXISTS Produtos(
                id    INTEGER PRIMARY KEY,
                name  TEXT NOT NULL,
                owner TEXT,
                price NUMERIC
            )          
            """)
        
        con.execute(create_tabela_produtos)

def insert_banco(id, name, owner , price):
    with engine.connect() as con:
        insert_tabela_produto = text (
            """INSERT INTO produtos 
                            (id, name, owner, price)
                        VALUES
                            (:id, :name, :owner, :price)
            """)
        try:
            con.execute(insert_tabela_produto, id = id, name = name, owner = owner, price = price)
            return text("Salvo!")
        except:
            return text("Erro")

def retorna_banco_id(id):
    with engine.connect() as con:
        searsh_tabela_produto = text(
            """SELECT *
                FROM produtos
                WHERE id = :id
            """)
        dic_result = []

        try:
            retorno = con.execute(searsh_tabela_produto, id = id)
            result = retorno.fetchone()

            dic_result.append(dict(result))
        except:
            pass

    return dic_result

def recria_banco():
    with engine.connect() as con:
        reset_tabela_produto = text("DROP TABLE produtos")
        con.execute(reset_tabela_produto)
        cria_tabela()


def retorna_banco():
    with engine.connect() as con:
        searsh_tabela_produto = text(
            """SELECT *
                FROM produtos
            """)
        retorno = con.execute(searsh_tabela_produto)
        dic_result = []

        while True:

            result = retorno.fetchone()

            if result == None:
                break

            else:
                dic_result.append(dict(result))

    return dic_result

def proximo_id():
    with engine.connect() as con:
        searsh_tabela_produto = text("SELECT * FROM Produtos WHERE id=(SELECT max(id) FROM Produtos)")
        try:
            retorno = con.execute(searsh_tabela_produto)
            result = retorno.fetchone()
       
            proximo_id = int(result["id"] + 1)
        except:
            proximo_id = 1

    return proximo_id

def atualiza_banco(id, name, owner , price):
    with engine.connect() as con:
        update_tabela_produto = text(
        """ UPDATE Produtos
            SET name = :name,
            owner = :owner,
            price = :price
            WHERE id = :id
        """)

        try:
            con.execute(update_tabela_produto, id = id, name = name, owner = owner, price = price)
            return text("Salvo!")
        except:
            return text("Erro")

def delete_id(id):
    with engine.connect() as con:
        delete_tuple = text("DELETE FROM Produtos WHERE id = :id")

        try:
            con.execute(delete_tuple, id=id)
        except:
            pass

def carrega_teste():
    cria_tabela()
    insert_banco(1, "CALCULADORA HP 50G", "HP", 450.00)
    insert_banco(2, "CALCULADORA HP 10S", "HP", 75.00)
    insert_banco(3, "TRANSISTOR TP120", "FAIRCHILD", 1.20)
    insert_banco(4, "TRANSISTOR TP130", "FAIRCHILD", 2.00)
    insert_banco(5, "CAPACITOR 10UF","EPCOS", 4.50)
    
