from fastapi import FastAPI, HTTPException
from .schema import CreateReceita, Receita

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

@app.get("/receitas", response_model=List[Receita])
def get_todas_receitas():
    return receitas

@app.get("/receitas/id/{id}", response_model=Receita)
def get_receita_por_id(id: int):
    for receita in receitas:
        if receita.id == id:
            return receita
    return {"erro": "Receita não encontrada"}

@app.get("/receitas/{nome_receita}", response_model=Receita)
def get_receita_por_nome(nome_receita: str):
    for receita in receitas:
        if receita.nome.lower() == nome_receita.lower():  # desafio extra: ignorar maiúsculas/minúsculas
            return receita
    return {"erro": "Receita não encontrada"}

@app.post("/receitas", response_model=Receita, status_code=201)
def create_receita(nova_receita: CreateReceita):
    # desafio extra: validar tamanho do nome da receita
    if len(nova_receita.nome) < 2 or len(nova_receita.nome) > 50:
        return {"erro": "O nome da receita deve ter entre 2 e 50 caracteres."}
    
    # desafio extra: validar quantidade de ingredientes
    if len(nova_receita.ingredientes) < 1 or len(nova_receita.ingredientes) > 20:
        return {"erro": "A receita deve ter entre 1 e 20 ingredientes."}

    for receita in receitas:
        if receita.nome.lower() == nova_receita.nome.lower():  # desafio extra: ignorar maiúsculas/minúsculas
            return {"erro": "Já existe uma receita com esse nome."}
    
    novo_id = receitas[-1].id + 1 if receitas else 1
    receita_criada = Receita(id=novo_id, **nova_receita.dict())
    receitas.append(receita_criada)
    return receita_criada

@app.put("/receitas/{id}", response_model=Receita)
def update_receita(id: int, dados: CreateReceita):
    # desafio extra: validar nome e ingredientes
    if len(dados.nome) < 2 or len(dados.nome) > 50:
        return {"erro": "O nome da receita deve ter entre 2 e 50 caracteres."}
    if len(dados.ingredientes) < 1 or len(dados.ingredientes) > 20:
        return {"erro": "A receita deve ter entre 1 e 20 ingredientes."}
    if not dados.nome or not dados.ingredientes or not dados.modo_de_preparo:
        return {"erro": "Nenhum campo pode ficar vazio."}
    
    for receita in receitas:
        if receita.nome.lower() == dados.nome.lower() and receita.id != id:  # desafio extra: ignorar maiúsculas/minúsculas
            return {"erro": "Já existe uma receita com esse nome."}

    # atualizar receita 
    achou = False
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_atualizada = Receita(id=id, **dados.dict())
            receitas[i] = receita_atualizada
            achou = True
            return receita_atualizada

    if not achou:
        return {"erro": "Receita não encontrada."}

@app.delete("/receitas/{id}")
def deletar_receita(id: int):
    # deletar receita 
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_deletada = receitas[i]
            receitas = receitas[:i] + receitas[i+1:]
            return {
                "mensagem": "Receita deletada com sucesso.",
                "receita": receita_deletada.dict()
            }
    return {"erro": "Receita não encontrada."}
