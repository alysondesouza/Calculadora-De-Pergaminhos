def calcular_custo(
    tabela,
    nivel_atual,
    nivel_desejado,
    quantidade_pergaminhos
):
    total_segredo = 0
    total_soro = 0
    total_ryos = 0

    for nivel in range(nivel_atual, nivel_desejado):
        custo = tabela[nivel]

        total_segredo += custo["segredo"]
        total_soro += custo["soro"]
        total_ryos += custo["ryos"]

    return {
        "segredo": total_segredo * quantidade_pergaminhos,
        "soro": total_soro * quantidade_pergaminhos,
        "ryos": total_ryos * quantidade_pergaminhos
    }