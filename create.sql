-- Table: public.atletas

-- DROP TABLE IF EXISTS public.atletas;

CREATE TABLE IF NOT EXISTS public.atletas
(
    id integer NOT NULL DEFAULT nextval('atletas_id_seq'::regclass),
    nome text COLLATE pg_catalog."default" NOT NULL,
    idade integer NOT NULL,
    tempo_treino numeric(4,2),
    categoria1 text COLLATE pg_catalog."default",
    nota1 numeric(4,2),
    classificacao1 text COLLATE pg_catalog."default",
    categoria2 text COLLATE pg_catalog."default",
    nota2 numeric(4,2),
    classificacao2 text COLLATE pg_catalog."default",
    categoria3 text COLLATE pg_catalog."default",
    nota3 numeric(4,2),
    classificacao3 text COLLATE pg_catalog."default",
    categoria4 text COLLATE pg_catalog."default",
    nota4 numeric(4,2),
    classificacao4 text COLLATE pg_catalog."default",
    categoria5 text COLLATE pg_catalog."default",
    nota5 numeric(4,2),
    classificacao5 text COLLATE pg_catalog."default",
    CONSTRAINT atletas_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.atletas
    OWNER to fabio;