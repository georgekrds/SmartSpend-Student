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

CREATE TABLE public.expenses (
    location character varying(255),
    food numeric,
    transportation numeric,
    entertainment numeric,
    supermarket numeric,
    bills numeric,
    student_restaurant numeric
);

ALTER TABLE public.expenses OWNER TO postgres;

COPY public.expenses (location, food, transportation, entertainment, supermarket, bills, student_restaurant) FROM stdin;
Athens	15	13	54	170	172	68
Piraeus	10	13	46	160	172	68
Thessaloniki	15	8	50	158	184	68
Patras	10	27	44	160	187	70
Heraklion	12	45	51	165	98	45
Larissa	10	30	57	152	80	70
Volos	12	30	48	157	93	70
Ioannina	10	20	52	150	87	70
Chania	12	30	70	170	150	45
Kalamata	13	28	55	135	90	\N
Alexandroupoli	10	28	55	150	90	\N
Xanthi	12	23	50	140	90	\N
Komotini	9	36	55	143	200	\N
Rhodes	10	25	55	134	175	52
Mytilini	11	30	20	165	220	\N
Kerkyra	10	30	55	137	150	72
\.
