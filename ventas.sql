
CREATE database venta;
show databases;

use venta;

CREATE TABLE venta (
    id_venta VARCHAR(100) PRIMARY KEY,  -- ID de la venta, entero y clave primaria
    id_producto VARCHAR(100) NOT NULL,           -- ID del producto, entero
    dnicliente VARCHAR(10) NOT NULL,    -- DNI del cliente, cadena de texto
    nomcliente VARCHAR(100) NOT NULL,   -- Nombre del cliente, cadena de texto
    apecliente VARCHAR(100) NOT NULL,   -- Apellido del cliente, cadena de texto
    fecha DATE NOT NULL,                -- Fecha de la venta, tipo fecha
    productovend VARCHAR(255) NOT NULL, -- Nombre del producto vendido, cadena de texto
    precio DECIMAL(10, 2) NOT NULL      -- Precio del producto, número decimal
);

CREATE TABLE ventaLocal (
    id_venta VARCHAR(100) PRIMARY KEY,  -- ID de la venta (referencia a Venta)
    id_producto VARCHAR(100) NOT NULL,           -- ID del producto
    dnicliente VARCHAR(10) NOT NULL,    -- DNI del cliente
    nomcliente VARCHAR(100) NOT NULL,   -- Nombre del cliente
    apecliente VARCHAR(100) NOT NULL,   -- Apellido del cliente
    fecha DATE NOT NULL,                -- Fecha de la venta
    productovend VARCHAR(255) NOT NULL, -- Nombre del producto vendido
    precio DECIMAL(10, 2) NOT NULL,     -- Precio del producto
    dirlocal VARCHAR(255) NOT NULL,     -- Dirección del local
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta) -- Relación con la tabla Venta
);

CREATE TABLE ventaOnline (
    id_venta VARCHAR(100) NOT NULL PRIMARY KEY,  -- ID de la venta (referencia a Venta)
    id_producto VARCHAR(100) NOT NULL,           -- ID del producto
    dnicliente VARCHAR(10) NOT NULL,    -- DNI del cliente
    nomcliente VARCHAR(100) NOT NULL,   -- Nombre del cliente
    apecliente VARCHAR(100) NOT NULL,   -- Apellido del cliente
    fecha DATE NOT NULL,                -- Fecha de la venta
    productovend VARCHAR(255) NOT NULL, -- Nombre del producto vendido
    precio DECIMAL(10, 2) NOT NULL,     -- Precio del producto
    direnvio VARCHAR(255) NOT NULL,     -- Dirección de envío
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta) -- Relación con la tabla Venta
);

alter table ventaOnline 
add campo_prueba varchar(150);

alter table ventaOnline 
drop column campo_prueba;

select * FROM venta;

