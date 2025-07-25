--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: colormuestra; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.colormuestra AS ENUM (
    'blanco',
    'amarillento',
    'transparente',
    'verde',
    'rosada_roja'
);


ALTER TYPE public.colormuestra OWNER TO postgres;

--
-- Name: olormuestra; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.olormuestra AS ENUM (
    'dulce',
    'agrio',
    'rancio',
    'quimico_metalico',
    'sin_olor'
);


ALTER TYPE public.olormuestra OWNER TO postgres;

--
-- Name: presenciasuciedades; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.presenciasuciedades AS ENUM (
    'si',
    'no'
);


ALTER TYPE public.presenciasuciedades OWNER TO postgres;

--
-- Name: tipodeleche; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tipodeleche AS ENUM (
    'calostro',
    'transicional',
    'madura'
);


ALTER TYPE public.tipodeleche OWNER TO postgres;

--
-- Name: tiporecipiente; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tiporecipiente AS ENUM (
    'vidrio',
    'plastico_sin_bpa',
    'bolsa'
);


ALTER TYPE public.tiporecipiente OWNER TO postgres;

--
-- Name: ubicacionmuestra; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.ubicacionmuestra AS ENUM (
    'refrigerador',
    'congelador',
    'banco_de_leche'
);


ALTER TYPE public.ubicacionmuestra OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: analisis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.analisis (
    id_analisis integer NOT NULL,
    id_usuario integer NOT NULL,
    id_f_ingreso integer NOT NULL,
    id_muestra integer NOT NULL,
    ph double precision NOT NULL,
    conductividad double precision NOT NULL,
    temperatura double precision NOT NULL,
    mensaje_temp character varying NOT NULL,
    tipo_de_leche public.tipodeleche NOT NULL
);


ALTER TABLE public.analisis OWNER TO postgres;

--
-- Name: analisis_id_analisis_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.analisis_id_analisis_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.analisis_id_analisis_seq OWNER TO postgres;

--
-- Name: analisis_id_analisis_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.analisis_id_analisis_seq OWNED BY public.analisis.id_analisis;


--
-- Name: formularios_ingreso; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formularios_ingreso (
    id_f_ingreso integer NOT NULL,
    id_usuario integer NOT NULL,
    nombre_mama character varying NOT NULL,
    nombre_bebe character varying NOT NULL,
    sexo_bebe character varying NOT NULL,
    edad_mama integer NOT NULL,
    fecha_nacimiento date NOT NULL,
    semanas_del_parto integer NOT NULL,
    prematuro boolean NOT NULL,
    numero_de_parto integer NOT NULL,
    peso integer NOT NULL,
    "tama├▒o" integer NOT NULL
);


ALTER TABLE public.formularios_ingreso OWNER TO postgres;

--
-- Name: formularios_ingreso_id_f_ingreso_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.formularios_ingreso_id_f_ingreso_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.formularios_ingreso_id_f_ingreso_seq OWNER TO postgres;

--
-- Name: formularios_ingreso_id_f_ingreso_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.formularios_ingreso_id_f_ingreso_seq OWNED BY public.formularios_ingreso.id_f_ingreso;


--
-- Name: muestras; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.muestras (
    id_muestra integer NOT NULL,
    id_usuario integer NOT NULL,
    id_f_ingreso integer NOT NULL,
    nombre_muestra character varying NOT NULL,
    fecha_de_extraccion date NOT NULL,
    hora_de_extraccion time without time zone NOT NULL,
    volumen double precision NOT NULL,
    pecho character varying NOT NULL,
    color public.colormuestra NOT NULL,
    ubicacion public.ubicacionmuestra NOT NULL,
    observacion character varying,
    foto_de_muestra character varying,
    olor public.olormuestra NOT NULL,
    presencia_de_suciedades public.presenciasuciedades NOT NULL,
    tipo_de_recipiente public.tiporecipiente NOT NULL
);


ALTER TABLE public.muestras OWNER TO postgres;

--
-- Name: muestras_id_muestra_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.muestras_id_muestra_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.muestras_id_muestra_seq OWNER TO postgres;

--
-- Name: muestras_id_muestra_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.muestras_id_muestra_seq OWNED BY public.muestras.id_muestra;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    full_name character varying NOT NULL,
    password_history character varying
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_usuario_seq OWNER TO postgres;

--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_usuario_seq OWNED BY public.usuarios.id_usuario;


--
-- Name: analisis id_analisis; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.analisis ALTER COLUMN id_analisis SET DEFAULT nextval('public.analisis_id_analisis_seq'::regclass);


--
-- Name: formularios_ingreso id_f_ingreso; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formularios_ingreso ALTER COLUMN id_f_ingreso SET DEFAULT nextval('public.formularios_ingreso_id_f_ingreso_seq'::regclass);


--
-- Name: muestras id_muestra; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.muestras ALTER COLUMN id_muestra SET DEFAULT nextval('public.muestras_id_muestra_seq'::regclass);


--
-- Name: usuarios id_usuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuarios_id_usuario_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
860ff917a0c6
\.


--
-- Data for Name: analisis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.analisis (id_analisis, id_usuario, id_f_ingreso, id_muestra, ph, conductividad, temperatura, mensaje_temp, tipo_de_leche) FROM stdin;
\.


--
-- Data for Name: formularios_ingreso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formularios_ingreso (id_f_ingreso, id_usuario, nombre_mama, nombre_bebe, sexo_bebe, edad_mama, fecha_nacimiento, semanas_del_parto, prematuro, numero_de_parto, peso, "tama├▒o") FROM stdin;
\.


--
-- Data for Name: muestras; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.muestras (id_muestra, id_usuario, id_f_ingreso, nombre_muestra, fecha_de_extraccion, hora_de_extraccion, volumen, pecho, color, ubicacion, observacion, foto_de_muestra, olor, presencia_de_suciedades, tipo_de_recipiente) FROM stdin;
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id_usuario, email, hashed_password, full_name, password_history) FROM stdin;
22	andres@example.com	$2b$12$9rtyX7Yzwh8ntA9PTo1IROL6.iHlsGGW2aGDFjVfZ2x4P1XSFN0km	andres rodriguez 	\N
23	josue@example.com	$2b$12$987mKWbCe/qdibL2IPtkYu6M6NxTmKKeVKO.INSYXnaDjVU8gzw.u	josue alvarez	\N
24	androd9002@gmail.com	$2b$12$lcGViHfev.LxcbcHylMHb.rv0c.pc.zI7Li3HhZfmjB9CVxuwrWcy	andres rodriguez 	\N
25	androd2000x@gmail.com	$2b$12$Lan5lsdqLolAvYJvJs/Tsup30YRLbu53mhyl.G8gNjvHh1hTl8OmO	andres rodriguez 	\N
\.


--
-- Name: analisis_id_analisis_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.analisis_id_analisis_seq', 1, true);


--
-- Name: formularios_ingreso_id_f_ingreso_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formularios_ingreso_id_f_ingreso_seq', 14, true);


--
-- Name: muestras_id_muestra_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.muestras_id_muestra_seq', 13, true);


--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_usuario_seq', 25, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: analisis analisis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.analisis
    ADD CONSTRAINT analisis_pkey PRIMARY KEY (id_analisis);


--
-- Name: formularios_ingreso formularios_ingreso_id_usuario_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formularios_ingreso
    ADD CONSTRAINT formularios_ingreso_id_usuario_key UNIQUE (id_usuario);


--
-- Name: formularios_ingreso formularios_ingreso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formularios_ingreso
    ADD CONSTRAINT formularios_ingreso_pkey PRIMARY KEY (id_f_ingreso);


--
-- Name: muestras muestras_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.muestras
    ADD CONSTRAINT muestras_pkey PRIMARY KEY (id_muestra);


--
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- Name: ix_analisis_id_analisis; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_analisis_id_analisis ON public.analisis USING btree (id_analisis);


--
-- Name: ix_formularios_ingreso_id_f_ingreso; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_formularios_ingreso_id_f_ingreso ON public.formularios_ingreso USING btree (id_f_ingreso);


--
-- Name: ix_muestras_id_muestra; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_muestras_id_muestra ON public.muestras USING btree (id_muestra);


--
-- Name: ix_usuarios_id_usuario; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_usuarios_id_usuario ON public.usuarios USING btree (id_usuario);


--
-- Name: analisis analisis_id_f_ingreso_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.analisis
    ADD CONSTRAINT analisis_id_f_ingreso_fkey FOREIGN KEY (id_f_ingreso) REFERENCES public.formularios_ingreso(id_f_ingreso);


--
-- Name: analisis analisis_id_muestra_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.analisis
    ADD CONSTRAINT analisis_id_muestra_fkey FOREIGN KEY (id_muestra) REFERENCES public.muestras(id_muestra);


--
-- Name: analisis analisis_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.analisis
    ADD CONSTRAINT analisis_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- Name: formularios_ingreso formularios_ingreso_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formularios_ingreso
    ADD CONSTRAINT formularios_ingreso_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- Name: muestras muestras_id_f_ingreso_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.muestras
    ADD CONSTRAINT muestras_id_f_ingreso_fkey FOREIGN KEY (id_f_ingreso) REFERENCES public.formularios_ingreso(id_f_ingreso);


--
-- Name: muestras muestras_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.muestras
    ADD CONSTRAINT muestras_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- PostgreSQL database dump complete
--

