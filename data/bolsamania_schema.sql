-- Schema for to-do application examples.

-- Valores diferentes de cada bolsa
create table valores (
    name        text primary key not null,
    description text,
    bolsa	integer
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
    valor        text,
    actualizado	 date
);

insert into bolsa (name, description) values ('^IBEX', 'Bolsa de Madrid');    
insert into valores (name, description, bolsa) values ('SAM.MC', 'Santander', '^IBEX');
insert into cartera (description, acciones,valor) values ('Santander','200','SAM.MC');
