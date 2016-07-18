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

