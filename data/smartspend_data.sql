--SmartSpend Student Database

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

SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE public.alexandroupoli_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.alexandroupoli_expenses OWNER TO postgres;


CREATE TABLE public.athens_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.athens_expenses OWNER TO postgres;


CREATE TABLE public.chania_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.chania_expenses OWNER TO postgres;


CREATE TABLE public.heraklion_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.heraklion_expenses OWNER TO postgres;


CREATE TABLE public.ioannina_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.ioannina_expenses OWNER TO postgres;


CREATE TABLE public.kalamata_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.kalamata_expenses OWNER TO postgres;


CREATE TABLE public.kerkyra_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.kerkyra_expenses OWNER TO postgres;


CREATE TABLE public.komotini_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.komotini_expenses OWNER TO postgres;


CREATE TABLE public.larissa_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.larissa_expenses OWNER TO postgres;


CREATE TABLE public.mytilini_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.mytilini_expenses OWNER TO postgres;


CREATE TABLE public.patras_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.patras_expenses OWNER TO postgres;


CREATE TABLE public.piraeus_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.piraeus_expenses OWNER TO postgres;


CREATE TABLE public.rhodes_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.rhodes_expenses OWNER TO postgres;


CREATE TABLE public.thessaloniki_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.thessaloniki_expenses OWNER TO postgres;


CREATE TABLE public.volos_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.volos_expenses OWNER TO postgres;


CREATE TABLE public.xanthi_expenses (
    category character varying(50) NOT NULL,
    min_expense numeric,
    avg_expense numeric,
    max_expense numeric
);


ALTER TABLE public.xanthi_expenses OWNER TO postgres;


CREATE VIEW public.city_expenses_comparison AS
 SELECT 'Alexandroupoli'::text AS city,
    alexandroupoli_expenses.category,
    alexandroupoli_expenses.min_expense,
    alexandroupoli_expenses.avg_expense,
    alexandroupoli_expenses.max_expense
   FROM public.alexandroupoli_expenses
UNION ALL
 SELECT 'Athens'::text AS city,
    athens_expenses.category,
    athens_expenses.min_expense,
    athens_expenses.avg_expense,
    athens_expenses.max_expense
   FROM public.athens_expenses
UNION ALL
 SELECT 'Chania'::text AS city,
    chania_expenses.category,
    chania_expenses.min_expense,
    chania_expenses.avg_expense,
    chania_expenses.max_expense
   FROM public.chania_expenses
UNION ALL
 SELECT 'Heraklion'::text AS city,
    heraklion_expenses.category,
    heraklion_expenses.min_expense,
    heraklion_expenses.avg_expense,
    heraklion_expenses.max_expense
   FROM public.heraklion_expenses
UNION ALL
 SELECT 'Ioannina'::text AS city,
    ioannina_expenses.category,
    ioannina_expenses.min_expense,
    ioannina_expenses.avg_expense,
    ioannina_expenses.max_expense
   FROM public.ioannina_expenses
UNION ALL
 SELECT 'Kalamata'::text AS city,
    kalamata_expenses.category,
    kalamata_expenses.min_expense,
    kalamata_expenses.avg_expense,
    kalamata_expenses.max_expense
   FROM public.kalamata_expenses
UNION ALL
 SELECT 'Kerkyra'::text AS city,
    kerkyra_expenses.category,
    kerkyra_expenses.min_expense,
    kerkyra_expenses.avg_expense,
    kerkyra_expenses.max_expense
   FROM public.kerkyra_expenses
UNION ALL
 SELECT 'Komotini'::text AS city,
    komotini_expenses.category,
    komotini_expenses.min_expense,
    komotini_expenses.avg_expense,
    komotini_expenses.max_expense
   FROM public.komotini_expenses
UNION ALL
 SELECT 'Larissa'::text AS city,
    larissa_expenses.category,
    larissa_expenses.min_expense,
    larissa_expenses.avg_expense,
    larissa_expenses.max_expense
   FROM public.larissa_expenses
UNION ALL
 SELECT 'Mytilini'::text AS city,
    mytilini_expenses.category,
    mytilini_expenses.min_expense,
    mytilini_expenses.avg_expense,
    mytilini_expenses.max_expense
   FROM public.mytilini_expenses
UNION ALL
 SELECT 'Patras'::text AS city,
    patras_expenses.category,
    patras_expenses.min_expense,
    patras_expenses.avg_expense,
    patras_expenses.max_expense
   FROM public.patras_expenses
UNION ALL
 SELECT 'Piraeus'::text AS city,
    piraeus_expenses.category,
    piraeus_expenses.min_expense,
    piraeus_expenses.avg_expense,
    piraeus_expenses.max_expense
   FROM public.piraeus_expenses
UNION ALL
 SELECT 'Rhodes'::text AS city,
    rhodes_expenses.category,
    rhodes_expenses.min_expense,
    rhodes_expenses.avg_expense,
    rhodes_expenses.max_expense
   FROM public.rhodes_expenses
UNION ALL
 SELECT 'Thessaloniki'::text AS city,
    thessaloniki_expenses.category,
    thessaloniki_expenses.min_expense,
    thessaloniki_expenses.avg_expense,
    thessaloniki_expenses.max_expense
   FROM public.thessaloniki_expenses
UNION ALL
 SELECT 'Volos'::text AS city,
    volos_expenses.category,
    volos_expenses.min_expense,
    volos_expenses.avg_expense,
    volos_expenses.max_expense
   FROM public.volos_expenses
UNION ALL
 SELECT 'Xanthi'::text AS city,
    xanthi_expenses.category,
    xanthi_expenses.min_expense,
    xanthi_expenses.avg_expense,
    xanthi_expenses.max_expense
   FROM public.xanthi_expenses;


ALTER VIEW public.city_expenses_comparison OWNER TO postgres;


COPY public.alexandroupoli_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	8	9	10
transportation	22	25	28
entertainment	44	49.5	55
supermarket	130	140	150
bills	72	81	90
student_restaurant	\N	\N	\N
\.



COPY public.athens_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	12	13.5	15
transportation	10	11.5	13
entertainment	43	48.5	54
supermarket	150	160	170
bills	142	157	172
student_restaurant	54	61	68
\.



COPY public.chania_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	9	10.5	12
transportation	24	27	30
entertainment	56	63	70
supermarket	150	160	170
bills	120	135	150
student_restaurant	36	40.5	45
\.


COPY public.heraklion_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	9	10.5	12
transportation	36	40.5	45
entertainment	41	46	51
supermarket	145	155	165
bills	78	88	98
student_restaurant	36	40.5	45
\.



COPY public.ioannina_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	8	9	10
transportation	16	18	20
entertainment	42	47	52
supermarket	130	140	150
bills	70	78.5	87
student_restaurant	56	63	70
\.



COPY public.kalamata_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	10	11.5	13
transportation	22	25	28
entertainment	44	49.5	55
supermarket	115	125	135
bills	72	81	90
student_restaurant	\N	\N	\N
\.



COPY public.kerkyra_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	8	9	10
transportation	24	27	30
entertainment	44	49.5	55
supermarket	117	127	137
bills	120	135	150
student_restaurant	58	65	72
\.



COPY public.komotini_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	7	8	9
transportation	29	32.5	36
entertainment	44	49.5	55
supermarket	123	133	143
bills	160	180	200
student_restaurant	\N	\N	\N
\.



COPY public.larissa_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	8	9	10
transportation	24	27	30
entertainment	46	51.5	57
supermarket	132	142	152
bills	64	72	80
student_restaurant	56	63	70
\.



COPY public.mytilini_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	9	10	11
transportation	24	27	30
entertainment	16	18	20
supermarket	145	155	165
bills	176	198	220
student_restaurant	\N	\N	\N
\.



COPY public.patras_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	8	9	10
transportation	22	24.5	27
entertainment	35	39.5	44
supermarket	140	150	160
bills	157	172	187
student_restaurant	56	63	70
\.



COPY public.piraeus_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	8	9	10
transportation	10	11.5	13
entertainment	37	41.5	46
supermarket	140	150	160
bills	142	157	172
student_restaurant	54	61	68
\.



COPY public.rhodes_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	8	9	10
transportation	20	22.5	25
entertainment	44	49.5	55
supermarket	114	124	134
bills	140	157.5	175
student_restaurant	42	47	52
\.



COPY public.thessaloniki_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	12	13.5	15
transportation	6	7	8
entertainment	40	45	50
supermarket	138	148	158
bills	154	169	184
student_restaurant	54	61	68
\.



COPY public.volos_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	9	10.5	12
transportation	24	27	30
entertainment	38	43	48
supermarket	137	147	157
bills	74	83.5	93
student_restaurant	56	63	70
\.



COPY public.xanthi_expenses (category, min_expense, avg_expense, max_expense) FROM stdin;
food	9	10.5	12
transportation	18	20.5	23
entertainment	40	45	50
supermarket	120	130	140
bills	72	81	90
student_restaurant	\N	\N	\N
\.



ALTER TABLE ONLY public.alexandroupoli_expenses
    ADD CONSTRAINT alexandroupoli_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.athens_expenses
    ADD CONSTRAINT athens_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.chania_expenses
    ADD CONSTRAINT chania_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.heraklion_expenses
    ADD CONSTRAINT heraklion_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.ioannina_expenses
    ADD CONSTRAINT ioannina_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.kalamata_expenses
    ADD CONSTRAINT kalamata_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.kerkyra_expenses
    ADD CONSTRAINT kerkyra_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.komotini_expenses
    ADD CONSTRAINT komotini_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.larissa_expenses
    ADD CONSTRAINT larissa_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.mytilini_expenses
    ADD CONSTRAINT mytilini_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.patras_expenses
    ADD CONSTRAINT patras_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.piraeus_expenses
    ADD CONSTRAINT piraeus_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.rhodes_expenses
    ADD CONSTRAINT rhodes_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.thessaloniki_expenses
    ADD CONSTRAINT thessaloniki_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.volos_expenses
    ADD CONSTRAINT volos_expenses_pkey PRIMARY KEY (category);



ALTER TABLE ONLY public.xanthi_expenses
    ADD CONSTRAINT xanthi_expenses_pkey PRIMARY KEY (category);
