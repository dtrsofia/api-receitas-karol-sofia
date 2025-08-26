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
    ]

@app.get("/")
def hello():
    return{"title": "Livro de Receitas"}

@app.get("/")
def get_receita():