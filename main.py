from fastapi import FastAPI 

app = FastAPI(title="livro de receitas")


'''
   receitas = [
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
        'modo de preparo': 'Misture ovos e açúcar. Acrescente manteiga, chocolate, farinha e sal. Despeje na forma untada e asse a 180°C por ~25–30 min.'
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
        'modo de preparo': 'Misture os ingredientes na tigela e leve para a frigideira, virando os lados para dourar bem.'
    },

     {
        'nome': 'batata frita',
        'ingredientes': [
            'Batatas Inglesas',
            'Óleo',
            '1 pitada de Sal',
        ],
        'utensílios': ['faca', 'panela'],
        'modo de preparo': 'Descasque e corte as batatas em formato de palitos. Esquente o óleo na panela e frite as batatas por imersão. Retire e adicione sal a gosto.'
    },

      {
        'nome': 'Brigadeiro',
        'ingredientes': [
            '1 Caixa de Leite Condensado',
            '1/2 Colher de Manteiga',
            '3 Colheres de Achocolatado',
        ],
        'utensílios': ['colher', 'panela'],
        'modo de preparo': 'Adicione os ingrendientes em uma panela e leve ao fogo até que se torne uma mistura homogênea. Para uma consistência perfeita espere o brigadeiro desgrudar do fundo da panela.'
    },

    {
        'nome': 'Molho Branco',
        'ingredientes': [
            '2 xícaras de leite',
            '2 colheres (sopa) de farinha de trigo',
            'noz-moscada a gosto',
            '2 colheres (sopa) de manteiga'
            'sal a gosto'
            'pimenta-do-reino branca a gosto'
        ],
        'utensílios': ['colher de pau', 'panela', 'faca', 'tábua de corte'],
        'modo de preparo': 'Ferva o leite. Derreta a manteiga, junte a farinha e mexa bem até obter uma pasta homogênea. Aos poucos, acrescente o leite e bata, constantemente, para não empelotar. Deixe cozinhar por alguns minutos e tempere com sal, noz-moscada e pimenta.'
    },

    {
        'nome': 'Salada de Frutas',
        'ingredientes': [
            '3 Bananas',
            '3 Maças'
            '3 Goiabas',
            '1 Mamão'
            '1 Caixa de Leite Condensado'
            '1/2 Caixa de Creme de Leite'
        ],
        'utensílios': ['vasilha', 'faca', 'colher'],
        'modo de preparo': 'Descasque e corte todas as frutas. Coloque dentro de um recipiciente juntamente com o leite condensado e o creme de leite.'
    },


]

'''

@app.get("/")
def hello():
    return {"title": "Livro de Receitas"}

@app.get("/receitas/{nome_receita}")
def get_receita(nome_receita: str):
    for i in receitas:
        if i["nome"].lower() == nome_receita.lower():
            return i
    return {"erro": "Receita não encontrada"}



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class CreateReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Receita(BaseModel):
    id: int
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

receitas: List[Receita] = []

@app.get("/receitas", response_model=List[Receita])
def get_todas_receitas():
    return receitas

@app.get("/receitas/id/{id}", response_model=Receita)
def get_receita_por_id(id: int):
    for receita in receitas:
        if receita.id == id:
            return receita
    raise HTTPException(status_code=404, detail="Receita não encontrada")

@app.post("/receitas", response_model=Receita, status_code=201)
def create_receita(nova_receita: CreateReceita):
    for receita in receitas:
        if receita.nome.lower() == nova_receita.nome.lower():
            raise HTTPException(status_code=400, detail="Já existe uma receita com esse nome.")
    novo_id = receitas[-1].id + 1 if receitas else 1
    receita_criada = Receita(id=novo_id, **nova_receita.dict())
    receitas.append(receita_criada)
    return receita_criada


@app.put("/receitas/{id}")
def uptade_receita(id: int, dados: CreateReceita):

    for i in range(len(receitas)):

@app.put("/receitas/{id}")
def update _receita(id: int, dados: CreateReceita):
    for i in range(len(receitas)):

        if receitas[i].id == id:
            receita_atualizada = Receita(
              id=id,
              nome=dados.nome,
              ingredientes=dados.ingredientes,
              modo_de_preparo=dados.modo_de_preparo,
            )

           receitas[i] = (receita_atualizada)
           return receita_atualizada

    return {"mensagem": "Receita não encontrada"}


