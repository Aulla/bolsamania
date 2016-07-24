-- Schema for to-do application examples.

-- Valores diferentes de cada bolsa
create table valores (
    id          integer primary key autoincrement not null,
    name        text,
    description text,
    bolsa	integer
);

-- Configuracion
create table config (
    name        text primary key not null,
    value	 text
);

-- Diferentes bolsas
create table bolsa (
    id           integer primary key autoincrement not null,
    name      text,
    description text
);

-- Carteras del usuario
create table cartera (
    id		integer primary key autoincrement not null,
    description	 text,
    acciones     integer,
    precioc      integer,
    idvalor      integer
);

insert into bolsa (name, description) values ('^IBEX', 'Bolsa de Madrid');    
insert into valores (name, description, bolsa) values ('SAN.MC', 'Santander', '^IBEX');

insert into config (name, value) values ('timewallet', '5');
