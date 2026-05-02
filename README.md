#  Non-Compliance por Categoria

Gráfico de barras horizontais em Python com as despesas fora da política corporativa, agrupadas por categoria.

![Preview](Captura%20de%20tela%202026-05-02%20174414.png)

---

## O que faz

- Filtra registros com `Fora_Politica == "S"`
- Agrupa e soma os valores por `Categoria`
- Exibe valor (R$ mil) e percentual por categoria
- Cards laterais com total, nº de categorias e maior categoria

## DataFrame

O `dataset` foi **criado em Python**. Cada linha representa uma despesa, com os campos:

| Coluna | Descrição |
|---|---|
| `Filial` | Filial responsável pela despesa |
| `Categoria` | Tipo da despesa (ex.: Aéreo, Hotel, Carro) |
| `Valor` | Valor gasto em reais |
| `Limite_Politica` | Limite permitido pela política corporativa |
| `Fora_Politica` | `"S"` se `Valor > Limite_Politica`, caso contrário `"N"` |
| `Data` | Data da despesa |
| `Antecedencia_Reserva` | Dias de antecedência da reserva |

## Dependências

```bash
pip install pandas matplotlib numpy
```

| Biblioteca | Uso |
|---|---|
| `pandas` | Manipulação e agregação do DataFrame |
| `matplotlib` | Geração do gráfico (`pyplot`, `ticker`, `patches`) |
| `numpy` | Geração do gradiente de cores das barras |
