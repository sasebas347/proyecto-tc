CREATE TABLE pagos (
    referencia_pago BIGINT PRIMARY KEY,
    medio_pago VARCHAR(50) NOT NULL,
    monto NUMERIC(10, 2) NOT NULL,
    fecha_cancelacion DATE NOT NULL,
    estado VARCHAR(20) CHECK (estado IN ('pago', 'no pago', 'vencido', 'cortado'))
);

CREATE TABLE usuarios (
    nombre VARCHAR(100) NOT NULL,
    cc BIGINT PRIMARY KEY,
    telefono VARCHAR(15) NOT NULL,
    referencia_pago BIGINT REFERENCES pagos(referencia_pago)
);