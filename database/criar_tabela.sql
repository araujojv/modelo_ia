CREATE TABLE previoses_clientes(
    id SERIAL PRIMARY KEY,
    interacoes INTEGER,
    tempo_como_cliente INTEGER,
    gasto_mensal NUMERIC,
    chamados_suporte INTEGER,
    cancelado BOOLEAN,
    previoses_cliente BOOLEAN
);
