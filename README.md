# FaunaLog API

FaunaLog API é o back-end do projeto **FaunaLog**, responsável por receber imagens enviadas pelo aplicativo mobile, comparar com uma base local de imagens de referência e retornar o animal mais provável.

A API foi desenvolvida em **Python com FastAPI** e utiliza o modelo **CLIP ViT-B/32**, através da biblioteca Sentence Transformers, para gerar embeddings das imagens e comparar similaridade visual.

Este projeto faz parte de um sistema de portfólio que demonstra integração entre aplicativo mobile, inteligência artificial, processamento de imagem e consumo de dados externos.

## Objetivo

O objetivo da API é identificar animais a partir de imagens enviadas pelo app mobile.

A API recebe uma imagem, compara com imagens de referência organizadas em pastas locais e retorna informações como:

* Animal identificado;
* Nome formatado para exibição;
* Nome usado na busca da Wikipédia;
* Confiança da identificação;
* Melhor imagem de referência encontrada;
* Lista dos principais resultados;
* Descrição e imagem obtidas pela Wikipédia.

## Tecnologias utilizadas

* Python
* FastAPI
* Uvicorn
* Pillow
* Sentence Transformers
* CLIP ViT-B/32
* PyTorch
* Wikipédia REST API
* Python Multipart
* Requests

## Como funciona

O funcionamento geral da API é:

1. Ao iniciar, a API carrega o modelo CLIP.
2. A API lê as imagens de referência dentro da pasta `references`.
3. Cada imagem de referência é convertida em um embedding.
4. O app mobile envia uma imagem para o endpoint `/predict`.
5. A imagem enviada também é convertida em embedding.
6. A API compara a imagem recebida com as referências locais.
7. O animal com maior similaridade é selecionado.
8. A API busca dados complementares na Wikipédia.
9. O resultado é retornado em JSON para o aplicativo.

## Estrutura do projeto

```txt
faunalog-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── clip_service.py
│   └── animal_service.py
│
├── references/
│   ├── mico-leao-dourado/
│   │   ├── imagem1.jpg
│   │   ├── imagem2.jpg
│   │   └── imagem3.jpg
│   │
│   ├── onca-pintada/
│   │   ├── imagem1.jpg
│   │   ├── imagem2.jpg
│   │   └── imagem3.jpg
│   │
│   └── tatu/
│       ├── imagem1.jpg
│       ├── imagem2.jpg
│       └── imagem3.jpg
│
├── requirements.txt
└── README.md
```

## Organização das imagens de referência

As imagens usadas para reconhecimento devem ficar dentro da pasta `references`.

Cada animal deve ter sua própria pasta:

```txt
references/
├── mico-leao-dourado/
├── onca-pintada/
└── tatu/
```

Dentro de cada pasta, coloque imagens nos formatos:

* `.jpg`
* `.jpeg`
* `.png`
* `.webp`

Exemplo:

```txt
references/onca-pintada/
├── imagem1.jpg
├── imagem2.jpg
├── imagem3.jpg
└── imagem4.jpg
```

Quanto maior a variedade das imagens de referência, melhor tende a ser a identificação.

É recomendado usar imagens com:

* Ângulos diferentes;
* Fundos diferentes;
* Boa iluminação;
* Animal visível;
* Pouca interferência visual;
* Exemplos próximos e distantes.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/EdiomarNogueira/faunalog-api.git
```

Acesse a pasta do projeto:

```bash
cd faunalog-api
```

Crie um ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual.

No Windows:

```bash
venv\Scripts\activate
```

No Linux/macOS:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

Execute a API com Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

A API ficará disponível em:

```txt
http://localhost:8000
```

Em rede local, para ser acessada pelo aplicativo mobile, use o IP da máquina onde a API está rodando:

```txt
http://SEU_IP_LOCAL:8000
```

Exemplo:

```txt
http://127.0.0.1:8000
```

## Endpoints

### Verificar status da API

```http
GET /
```

Resposta esperada:

```json
{
  "status": "online",
  "message": "API FaunaLog funcionando"
}
```

### Identificar animal

```http
POST /predict
```

O endpoint espera uma imagem enviada como `multipart/form-data`.

Campo esperado:

```txt
file
```

Exemplo usando `curl`:

```bash
curl -X POST "http://localhost:8000/predict" ^
  -F "file=@imagem.jpg"
```

No Linux/macOS:

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@imagem.jpg"
```

## Exemplo de resposta

```json
{
  "animal": "mico-leao-dourado",
  "display_name": "Mico-leão-dourado",
  "wikipedia_name": "Mico-leão-dourado",
  "confidence": 0.8419,
  "best_reference": "images (10).jpg",
  "data": {
    "name": "Mico-leão-dourado",
    "image": "https://upload.wikimedia.org/...",
    "description": "O mico-leão-dourado é um primata endêmico do Brasil...",
    "source": "https://pt.wikipedia.org/wiki/Mico-le%C3%A3o-dourado"
  },
  "top_results": [
    {
      "animal": "mico-leao-dourado",
      "display_name": "Mico-leão-dourado",
      "wikipedia_name": "Mico-leão-dourado",
      "confidence": 0.8419,
      "best_reference": "images (10).jpg"
    },
    {
      "animal": "sagui",
      "display_name": "Sagui",
      "wikipedia_name": "Sagui",
      "confidence": 0.8312,
      "best_reference": "imagem2.jpg"
    }
  ]
}
```

## Observações sobre nomes de pastas

Os nomes das pastas dentro de `references` são usados como base para identificar e formatar o nome do animal.

Exemplos recomendados:

```txt
mico-leao-dourado
onca-pintada
tatu
sagui
capivara
```

A API pode formatar esses nomes para exibição, transformando:

```txt
mico-leao-dourado
```

em:

```txt
Mico-leão-dourado
```

Dependendo da implementação, nomes sem acento podem precisar de tratamento extra para buscar corretamente na Wikipédia.

## Integração com o app mobile

O aplicativo mobile deve enviar a imagem para:

```txt
http://SEU_IP_LOCAL:8000/predict
```

Exemplo:

```ts
const API_URL = "http://127.0.0.1:8000/predict";
```

Durante o desenvolvimento com celular físico, o computador que executa a API e o celular precisam estar conectados na mesma rede Wi-Fi.

## Limitações

* A API não treina um modelo próprio.
* A identificação é feita por comparação visual com imagens de referência.
* A precisão depende da qualidade da base local.
* Animais visualmente parecidos podem gerar resultados próximos.
* A busca de descrição depende da disponibilidade da página na Wikipédia.
* O primeiro carregamento pode demorar, pois o modelo CLIP precisa ser carregado.

## Possíveis melhorias futuras

* Criar painel administrativo para cadastrar animais;
* Criar upload de imagens de referência via API;
* Salvar embeddings em cache para acelerar o carregamento;
* Adicionar banco de dados;
* Adicionar autenticação;
* Criar histórico de identificações;
* Melhorar tratamento de nomes com acentos;
* Integrar com iNaturalist;
* Integrar com GBIF;
* Criar endpoint para listar animais disponíveis;
* Criar endpoint para adicionar novas referências;
* Publicar a API em um servidor online;
* Criar testes automatizados;
* Adicionar Docker.

## Status do projeto

Projeto em desenvolvimento.

Atualmente, a API já realiza carregamento de referências, comparação visual com CLIP, identificação do animal e busca de informações complementares na Wikipédia.

## Autor

Desenvolvido por **Ediomar Nogueira** como projeto de portfólio.
