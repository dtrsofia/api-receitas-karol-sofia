from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from schema import CreateReceita, Receita, Usuario, BaseUsuario, UsuarioPublic
from models import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_session

usuarios: List[Usuario] = []

receitas: List[Receita] = []

app = FastAPI(title="Livro de Receitas")

'''
receitas_anteriores = [
    {
        'nome': 'brownie',
        'ingredientes': [
            '3 ovos',
            '6 colheres de açúcar',
            '5 colheres de manteiga derretida',
            '6 colheres de chocolate em pó',
            '8 colheres de farinha de trigo',
            '1 pitada de sal'
        ],
        'utensílios': ['tigela', 'colher', 'forma', 'forno'],
        'modo_de_preparo': 'Misture ovos e açúcar. Acrescente manteiga, chocolate, farinha e sal. Despeje na forma untada e asse a 180°C por ~25–30 min.'
    },
    {
        'nome': 'omelete',
        'ingredientes': [
            '2 ovos',
            '1 pitada de sal',
            '1 pitada de orégano',
            'Cheiro verde a gosto'
        ],
        'utensílios': ['tigela', 'colher', 'frigideira', '1 fio de azeite/óleo/manteiga/margarina'],
        'modo_de_preparo': 'Misture os ingredientes na tigela e leve para a frigideira, virando os lados para dourar bem.'
    },
    {
        'nome': 'batata frita',
        'ingredientes': [
            'Batatas Inglesas',
            'Óleo',
            '1 pitada de Sal'
        ],
        'utensílios': ['faca', 'panela'],
        'modo_de_preparo': 'Descasque e corte as batatas em formato de palitos. Esquente o óleo na panela e frite as batatas por imersão. Retire e adicione sal a gosto.'
    },
    {
        'nome': 'Brigadeiro',
        'ingredientes': [
            '1 Caixa de Leite Condensado',
            '1/2 Colher de Manteiga',
            '3 Colheres de Achocolatado'
        ],
        'utensílios': ['colher', 'panela'],
        'modo_de_preparo': 'Adicione os ingredientes em uma panela e leve ao fogo até que se torne uma mistura homogênea. Para uma consistência perfeita espere o brigadeiro desgrudar do fundo da panela.'
    },
    {
        'nome': 'Molho Branco',
        'ingredientes': [
            '2 xícaras de leite',
            '2 colheres (sopa) de farinha de trigo',
            'noz-moscada a gosto',
            '2 colheres (sopa) de manteiga',
            'sal a gosto',
            'pimenta-do-reino branca a gosto'
        ],
        'utensílios': ['colher de pau', 'panela', 'faca', 'tábua de corte'],
        'modo_de_preparo': 'Ferva o leite. Derreta a manteiga, junte a farinha e mexa bem até obter uma pasta homogênea. Aos poucos, acrescente o leite e bata constantemente para não empelotar. Deixe cozinhar por alguns minutos e tempere com sal, noz-moscada e pimenta.'
    },
    {
        'nome': 'Salada de Frutas',
        'ingredientes': [
            '3 Bananas',
            '3 Maças',
            '3 Goiabas',
            '1 Mamão',
            '1 Caixa de Leite Condensado',
            '1/2 Caixa de Creme de Leite'
        ],
        'utensílios': ['vasilha', 'faca', 'colher'],
        'modo_de_preparo': 'Descasque e corte todas as frutas. Coloque dentro de um recipiente juntamente com o leite condensado e o creme de leite.'
    }
]
'''


receitas: List[Receita] = []

@app.get("/")
def hello():
    return {"title": "Livro de Receitas"}

@app.get("/receitas", response_model=List[Receita], status_code=HTTPStatus.OK)
def get_todas_receitas():
    return receitas

@app.get("/receitas/id/{id}", response_model=Receita)
def get_receita_por_id(id: int):
    for receita in receitas:
        if receita.id == id:
            return receita
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

@app.get("/receitas/{nome_receita}", response_model=Receita)
def get_receita_por_nome(nome_receita: str):
    for receita in receitas:
        if receita.nome.lower() == nome_receita.lower():  
            return receita
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="receita não encontrada")

@app.post("/receitas", response_model=Receita, status_code=HTTPStatus.CREATED) 
def create_receita(nova_receita: CreateReceita):
    if len(nova_receita.nome) < 2 or len(nova_receita.nome) > 50:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="O nome da receita deve ter entre 2 e 50 caracteres.")
    
    if len(nova_receita.ingredientes) < 1 or len(nova_receita.ingredientes) > 20:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A receita deve ter entre 1 e 20 ingredientes.")

    for receita in receitas:
        if receita.nome.lower() == nova_receita.nome.lower(): 
           raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe uma receita com esse nome.")
    
    novo_id = receitas[-1].id + 1 if receitas else 1
    receita_criada = Receita(id=novo_id, **nova_receita.dict()) 
    receitas.append(receita_criada)
    return receita_criada

@app.put("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def update_receita(id: int, dados: CreateReceita):
    
    if len(dados.nome) < 2 or len(dados.nome) > 50:
         raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="O nome da receita deve ter entre 2 e 50 caracteres.") 
    if len(dados.ingredientes) < 1 or len(dados.ingredientes) > 20:
         raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A receita deve ter entre 1 e 20 ingredientes.") 
    if not dados.nome or not dados.ingredientes or not dados.modo_de_preparo:
          raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Nenhum campo pode ficar vazio.") 
    
    for receita in receitas:
        if receita.nome.lower() == dados.nome.lower() and receita.id != id:  
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe uma receita com esse nome.")

    achou = False
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_atualizada = Receita(id=id, **dados.dict()) 
            receitas[i] = receita_atualizada
            achou = True
            return receita_atualizada
    
    if not achou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada.")

@app.delete("/receitas/{id}", status_code=HTTPStatus.OK) 
def delete_receita(id: int): 
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_deletada = receitas.pop(i) 
            return {
                "mensagem": "Receita deletada com sucesso.",
                "receita": receita_deletada.dict()
            }
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
def create_usuario(dados:BaseUsuario):
 
    if len(dados.nome_usuario) < 2 or len(dados.nome_usuario) > 50:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="O nome do usuário deve ter entre 2 e 50 caracteres.")
    
    if len(dados.email) < 5:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="O e-mail deve ter no mínimo 5 caracteres.")

    if len(dados.senha) < 6:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A senha deve ter no mínimo 6 caracteres.")

    # email duplicado 
    for usuario in usuarios:
        if usuario.email.lower() == dados.email.lower():
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe um usuário com esse e-mail."
            )

    novo_id = usuarios[-1].id + 1 if usuarios else 1
    usuario_criado = Usuario(id=novo_id, **dados.dict())
    usuarios.append(usuario_criado)
    return usuario_criado
def valida_senha(senha: str):
    tem_letra = False
    tem_numero = False

    for caractere in senha:
        if caractere.isalpha():
            tem_letra = True
        if caractere.isdigit():
            tem_numero = True

    if not tem_letra or not tem_numero:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A senha deve conter pelo menos uma letra e um número."
        )


@app.get("/usuarios", status_code=HTTPStatus.OK, response_model=List[UsuarioPublic])
def get_todos_usuarios():
    return usuarios


@app.get("/usuarios/{nome_usuario}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_nome(nome_usuario: str):
    for usuario in usuarios:
        if usuario.nome.lower() == nome_usuario.lower():
            return usuario
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")


@app.get("/usuarios/id/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_id(id: int):
    for usuario in usuarios:
        if usuario.id == id:
            return usuario
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")


@app.put("/usuarios/id/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def update_usuario(id: int, dados: BaseUsuario):
    if len(dados.nome) < 2 or len(dados.nome) > 50:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="O nome do usuário deve ter entre 2 e 50 caracteres."
        )

    if len(dados.email) < 5:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="O e-mail deve ter no mínimo 5 caracteres."
        )

    if len(dados.senha) < 6:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A senha deve ter no mínimo 6 caracteres."
        )

    # senha precisa ter letra e número
    valida_senha(dados.senha)

    for usuario in usuarios:
        if usuario.email.lower() == dados.email.lower() and usuario.id != id:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe um usuário com esse e-mail."
            )

    achou = False
    for i in range(len(usuarios)):
        if usuarios[i].id == id:
            usuario_atualizado = Usuario(id=id, **dados.dict())
            usuarios[i] = usuario_atualizado
            achou = True
            return usuario_atualizado

    if not achou:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado."
        )


@app.delete("/usuarios/id/{id}", status_code=HTTPStatus.OK)
def delete_usuario(id: int):
    for i in range(len(usuarios)):
        if usuarios[i].id == id:
            usuario_deletado = usuarios.pop(i)
            return {
                "mensagem": "Usuário deletado com sucesso.",
                "usuario": usuario_deletado.dict()
            }

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
