# OpenWeather Pipeline

Pipeline de dados meteorológicos em tempo real com arquitetura orientada a eventos. O sistema coleta dados climáticos via API da OpenWeather, publica eventos no Kafka e os persiste no Supabase.

## Arquitetura

```
POST /weather?city_id=<id>
        │
        ▼
   Flask API
        │
        ├──► OpenWeather API  (busca temperatura, umidade, descrição)
        │
        └──► Kafka Producer   (publica evento em weather-events)
                  │
                  ▼
          Kafka Consumer
                  │
                  ▼
            Supabase DB       (persiste em weather_readings)
```

## Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| API | Flask 3.1 |
| Mensageria | Apache Kafka (Confluent 7.5) |
| Banco de dados | Supabase (PostgreSQL) |
| Orquestração | Apache Airflow 2.7.3 |
| Infraestrutura | Docker Compose |
| Dados externos | OpenWeather API 2.5 |

## Pré-requisitos

- Python 3.11+
- Docker e Docker Compose

## Configuração

### 1. Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPEN_WEATHER_API_KEY=sua_chave_aqui
URL_SUPABASE=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_supabase
```

### 2. Dependências Python

```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 3. Infraestrutura

```bash
docker-compose up -d
```

Serviços disponibilizados:

| Serviço | URL |
|---------|-----|
| Airflow UI | http://localhost:8080 |
| Kafka UI | http://localhost:7900 |
| Flask API | http://localhost:5000 |

> Credenciais padrão do Airflow: `admin` / `admin`

## Execução

Execute o servidor e o consumer em terminais separados:

```bash
# Terminal 1 — API Flask
python src/app.py

# Terminal 2 — Kafka Consumer
python src/consumer.py
```

## Uso da API

### Coletar dados meteorológicos de uma cidade

```http
POST /weather?city_id=<id>
```

**Resposta (202 Accepted):**

```json
{
  "event_id": "uuid-gerado",
  "status": "accepted"
}
```

O processamento ocorre de forma assíncrona via Kafka. Os dados ficam disponíveis no Supabase após o consumer processar o evento.

## Estrutura do projeto

```
openweather/
├── docker-compose.yml
├── requirements.txt
├── .env
├── dags/                     # DAGs do Airflow (a implementar)
├── logs/
└── src/
    ├── app.py                # Servidor Flask
    ├── consumer.py           # Consumer Kafka
    └── services/
        ├── weather_service.py    # Integração OpenWeather API
        ├── kafka_service.py      # Producer Kafka
        └── database_manager.py   # Operações de banco (placeholder)
```

## Schema do banco de dados (Supabase)

**Tabela `cities`**

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | uuid | Identificador único |
| name | text | Nome da cidade |
| latitude | float | Latitude |
| longitude | float | Longitude |
| active | bool | Cidade habilitada |

**Tabela `weather_readings`**

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| event_id | uuid | ID do evento Kafka |
| event_timestamp | timestamp | Momento da coleta |
| city_id | uuid | Referência à cidade |
| city_name | text | Nome da cidade |
| temperature | float | Temperatura em °C |
| humidity | int | Umidade relativa (%) |
| description | text | Descrição do clima |
