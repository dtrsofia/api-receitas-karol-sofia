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

@app.get("/")
def hello():
    return {"title": "Livro de Receitas"}

@app.get("/receitas/{nome_receita}")
def get_receita(nome_receita: str):
    for i in receitas:
        if i["nome"].lower() == nome_receita.lower():
            return i
    return {"erro": "Receita não encontrada"}
