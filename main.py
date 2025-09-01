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
            'Sal',
        ],
        'utensílios': ['faca', 'panela'],
        'modo de preparo': 'Descasque e corte as batatas em formato de palitos. Esquente o óleo na panela e frite as batatas por imersão. Retire e adicione sal a gosto.'
    },


]

@app.get("/")
def hello():
    return {"title": "Livro de Receitas"}

@app.get("/receitas/{nome_receita}")
def get_receita(nome_receita: str):
    for i in receitas:
        if i["nome"].lower() == nome_receita.lower():
            return i
    return {"erro": "Receita não encontrada"}
