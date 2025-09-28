from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Livro de Receitas")

class CreateReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Receita(BaseModel):
    id: int
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

receitas = [
    {"nome": "Brownie", "ingredientes": ["3 ovos","6 colheres de açúcar","5 colheres de manteiga derretida","6 colheres de chocolate em pó","8 colheres de farinha de trigo","1 pitada de sal"], "modo_de_preparo": "Misture ovos e açúcar. Acrescente manteiga, chocolate, farinha e sal. Despeje na forma untada e asse a 180°C por ~25–30 min."},
    {"nome": "Omelete", "ingredientes": ["2 ovos","1 pitada de sal","1 pitada de orégano","Cheiro verde a gosto"], "modo_de_preparo": "Misture os ingredientes na tigela e leve para a frigideira, virando os lados para dourar bem."},
    {"nome": "Batata Frita", "ingredientes": ["Batatas Inglesas","Óleo","1 pitada de sal"], "modo_de_preparo": "Descasque e corte as batatas em formato de palitos. Esquente o óleo na panela e frite as batatas por imersão. Retire e adicione sal a gosto."},
    {"nome": "Brigadeiro", "ingredientes": ["1 Caixa de Leite Condensado","1/2 Colher de Manteiga","3 Colheres de Achocolatado"], "modo_de_preparo": "Adicione os ingredientes em uma panela e leve ao fogo até que se torne uma mistura homogênea. Para uma consistência perfeita espere o brigadeiro desgrudar do fundo da panela."},
    {"nome": "Molho Branco", "ingredientes": ["2 xícaras de leite","2 colheres (sopa) de farinha de trigo","noz-moscada a gosto","2 colheres (sopa) de manteiga","sal a gosto","pimenta-do-reino branca a gosto"], "modo_de_preparo": "Ferva o leite. Derreta a manteiga, junte a farinha e mexa bem até obter uma pasta homogênea. Aos poucos, acrescente o leite e bata, constantemente, para não empelotar. Deixe cozinhar por alguns minutos e tempere com sal, noz-moscada e pimenta."},
    {"nome": "Salada de Frutas", "ingredientes": ["3 Bananas","3 Maçãs","3 Goiabas","1 Mamão","1 Caixa de Leite Condensado","1/2 Caixa de Creme de Leite"], "modo_de_preparo": "Descasque e corte todas as frutas. Coloque dentro de um recipiente juntamente com o leite condensado e o creme de leite."}
]

proxima_id = 1

@app.get("/receitas", response_model=List[dict])
def get_todas_receitas():
    return receitas

@app.get("/receitas/nome/{nome}", response_model=dict)
def get_receita_por_nome(nome: str):
    for receita in receitas:
        if receita["nome"].lower() == nome.lower():
            return receita
    raise HTTPException(status_code=404, detail="Receita não encontrada")

@app.get("/receitas/id/{id}", response_model=Receita)
def get_receita_por_id(id: int):
    for receita in receitas:
        if "id" in receita and receita["id"] == id:
            return Receita(**receita)
    raise HTTPException(status_code=404, detail="Receita não encontrada")

@app.post("/receitas", response_model=Receita, status_code=201)
def create_receita(nova_receita: CreateReceita):
    global proxima_id
    for receita in receitas:
        if receita["nome"].lower() == nova_receita.nome.lower():
            raise HTTPException(status_code=400, detail="Já existe uma receita com esse nome.")
    receita_criada = {"id": proxima_id, **nova_receita.dict()}
    proxima_id += 1
    receitas.append(receita_criada)
    return Receita(**receita_criada)

@app.put("/receitas/{id}", response_model=Receita)
def update_receita(id: int, dados: CreateReceita):
    for receita in receitas:
        if "id" in receita and receita["id"] == id:
            for r in receitas:
                if "id" in r and r["nome"].lower() == dados.nome.lower() and r["id"] != id:
                    raise HTTPException(status_code=400, detail="Já existe uma receita com esse nome.")
            if dados.nome == "" or len(dados.ingredientes) == 0 or dados.modo_de_preparo == "":
                raise HTTPException(status_code=400, detail="Nenhum campo pode ficar vazio.")
            receita.update(dados.dict())
            return Receita(**receita)
    raise HTTPException(status_code=404, detail="Receita não encontrada")

@app.delete("/receitas/{id}")
def deletar_receita(id: int):
    for i, receita in enumerate(receitas):
        if "id" in receita and receita["id"] == id:
            receita_deletada = receitas.pop(i)
            return {
                "mensagem": "Receita deletada com sucesso.",
                "receita": receita_deletada
            }
    raise HTTPException(status_code=404, detail="Receita não encontrada")
