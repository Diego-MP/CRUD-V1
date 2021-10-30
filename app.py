from flask import Flask
from flask import render_template
from flask import request
import re, os

from banco import insert_banco, recria_banco, retorna_banco, proximo_id, retorna_banco_id, atualiza_banco, delete_id, carrega_teste

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/", methods = ['GET', 'POST'])
def index():

    urlstring = request.args #GET
    form = request.form #POST

    #variaveis usada para retorno no rende_template
    #usadas nas funçoes retrornado as consultas do banco
    read_id = ''
    read_name = ''
    read_owner = ''
    read_price = ''

  
    #recebe as informaçoes dos formmularios HTML via GET quando precionado o botaão CREATE
    if (urlstring.get("btn_create") == "Create") and (request.method == "GET"):

        #armazena e converte os dados obtidos dos campos input do index.html
        txt_id = int(urlstring.get("input_id") or -1) # pega o campo id, caso vazio passa o 0 devido a erro de conversao de um literal para int
        text_name = str(urlstring.get("input_name").upper())
        text_owner =str(urlstring.get("input_owner").upper())
        text_price = urlstring.get("input_price")#esse campo nao é convertido por ser tratado pelo tipo money no proprio banco de dados

        #insere no banco os dados lido do index.html obtidos via GET
        if txt_id > 0:
            insert_banco(txt_id, text_name, text_owner, text_price)
       
        elif txt_id == 0:
            carrega_teste()
        
        else:
            pass
    
    elif (urlstring.get("btn_read") == "Read") and (request.method == "GET"):
        
        #armazena e converte os dados obtidos dos campos input do index.html
        txt_id = int(urlstring.get("input_id") or 0) # pega o campo id, caso vazio passa o 0 devido a erro de conversao de um literal para int
        
        #retorna um dicionario com a consulta do banco
        retorno_produtos_id = retorna_banco_id(txt_id)
        
        #testa se o retorno contem algum cadastro caso contrario ha um erro de fora do indice
        if retorno_produtos_id != []:
            read_id = retorno_produtos_id[0]['id']
            read_name = retorno_produtos_id[0]['name']
            read_owner = retorno_produtos_id[0]['owner']
            read_price = retorno_produtos_id[0]['price']
        else:
            pass

    elif (urlstring.get("btn_update") == "Update") and (request.method == "GET"):
        
        #armazena e converte os dados obtidos dos campos input do index.html
        txt_id = int(urlstring.get("input_id") or 0) # pega o campo id, caso vazio passa o 0 devido a erro de conversao de um literal para int
        text_name = str(urlstring.get("input_name").upper())
        text_owner =str(urlstring.get("input_owner").upper())
        text_price = urlstring.get("input_price")#esse campo nao é convertido por ser tratado pelo tipo money no proprio banco de dados

        #insere no banco os dados lido do index.html obtidos via GET
        atualiza_banco(txt_id, text_name, text_owner, text_price)

    elif (urlstring.get("btn_delete") == "Delete") and (request.method == "GET"):

        #armazena e converte os dados obtidos dos campos input do index.html
        txt_id = int(urlstring.get("input_id") or 0) # pega o campo id, caso vazio passa o 0 devido a erro de conversao de um literal para int
        #deleta um produto quando preenchido o ID
        delete_id(txt_id)

            
        
    elif (urlstring.get("btn_delete_all") == "Delete All") and (request.method == "GET"):
        #deleta o banco todo
        recria_banco()

    #identifica o valor contido no botao editar gerado dinamicamente o '|' vai funcionar como um delimitador para pehar o numero gerado que sera o id
    elif ("Edit_Prod:" in str(urlstring.get("edit_item"))) and (request.method == "GET"):
        string = urlstring.get("edit_item")
        #procura no valor do botao o numero do id contido entre ::       
        txt_id = re.search(r':([^:]+):', string).group()
        #remove da sstring encontrada pelo REGEX os caracteres ::
        txt_id = int(txt_id.replace(":", ""))
        #retorna um dicionario com a consulta do banco
        retorno_produtos_id = retorna_banco_id(txt_id)
        print(f'numero de retorno id: {txt_id}')
        
        #testa se o retorno contem algum cadastro caso contrario ha um erro de fora do indice
        if retorno_produtos_id != []:
            read_id = retorno_produtos_id[0]['id']
            read_name = retorno_produtos_id[0]['name']
            read_owner = retorno_produtos_id[0]['owner']
            read_price = retorno_produtos_id[0]['price']
        else:
            pass

    elif ("Delete_Prod:" in str(urlstring.get("delete_item"))) and (request.method == "GET"):
        string = urlstring.get("delete_item")
        #procura no valor do botao o numero do id contido entre ::
        txt_id = re.search(r':([^:]+):', string).group()
        #remove da sstring encontrada pelo REGEX os caracteres ::
        txt_id = int(txt_id.replace(":", ""))
        #retorna um dicionario com a consulta do banco
        print('tentei deleat')
        delete_id(txt_id)
    
  
    else:
        pass    

    list_banco = retorna_banco()
    linhas_banco = len(list_banco)

    if proximo_id() == 1:
        proximo_id_prod = "Entre com Código 0 para carregar a tabela de teste"
    else:
        proximo_id_prod = proximo_id() 

    #print(f'Retorno do banco: {list_banco}')

    return  render_template("index.html", 
                        list_banco = list_banco, 
                        linhas_banco = linhas_banco, 
                        proximo_id = proximo_id_prod,
                        read_id = read_id,
                        read_name = read_name,
                        read_owner = read_owner,
                        read_price = read_price                     
                        )


if __name__ == "__main__":
#DEPLOY HEROKU
    port = int(os.environ.get("PORT", 5051))
    app.run(host='0.0.0.0', port=port)

#LOCAL 
    #app.run(host = "127.0.0.1", port = 5050, debug = True)