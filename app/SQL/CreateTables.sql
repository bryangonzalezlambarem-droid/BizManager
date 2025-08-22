USE BizManager;

----- B. G. L. 22/08/2025 Crear tablas relacionales para el proyecto -----

-- B. G. L. 22/08/2025  Crear tabla venderores 
CREATE TABLE Salespeople(
	salesman_id INT PRIMARY KEY IDENTITY(1,1),
	name NVARCHAR(100) NOT NULL,
	email NVARCHAR(100) UNIQUE NOT NULL,
	phone NVARCHAR(100),
	registration_date DATETIME DEFAULT GETDATE()
);

-- B. G. L. 22/08/2025  Crear tabla de clientes
CREATE TABLE Customers (
	customer_id INT PRIMARY KEY IDENTITY (1,1),
	name NVARCHAR(100) NOT NULL,
	email NVARCHAR(100) UNIQUE NOT NULL,
	phone NVARCHAR(20),
	adress NVARCHAR(255)
);

-- B. G. L. 22/08/2025  Crear tabla de productos
CREATE TABLE Products(
	product_id INT PRIMARY KEY IDENTITY (1,1),
	name VARCHAR(100) NOT NULL,
	description NVARCHAR(255),
	price DECIMAL(10,2) NOT NULL,
	stock INT NOT NULL DEFAULT 0,
	salesman_id INT NOT NULL,
	FOREIGN KEY (salesman_id) REFERENCES Salespeople(salesman_id)
);

-- B. G. L. 22/08/2025  Crear tabla de pedidos
CREATE TABLE Orders (
	order_id INT PRIMARY KEY IDENTITY(1,1),
	customer_id INT NOT NULL,
	order_date DATETIME DEFAULT GETDATE(),
	status NVARCHAR(50) DEFAULT 'Pending',
	total_amount DECIMAL(10,2) DEFAULT 0,
	FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- B. G. L. 22/08/2025  Crear tabla de los detalles para los pedidos
CREATE TABLE OrderDetails (
	detail_id INT PRIMARY KEY IDENTITY (1,1),
	order_id INT NOT NULL,
	product_id INT NOT NULL,
	salesman_id INT NOT NULL,
	quantity INT NOT NULL,
	unit_price DECIMAL(10,2) NOT NULL,
	FOREIGN KEY (order_id) REFERENCES Orders(order_id),
	FOREIGN KEY (product_id) REFERENCES Products(product_id),
	FOREIGN KEY (salesman_id1) REFERENCES Salespeople(salesman_id)
);

-- B. G. L. 22/08/2025  Crear tabla de Historial de Estados de Pedido
CREATE TABLE OrderStatusHistory (
	history_id INT PRIMARY KEY IDENTITY(1,1),
	order_id INT NOT NULL,
	old_status NVARCHAR(50),
	new_status NVARCHAR(50) NOT NULL,
	change_date DATETIME DEFAULT GETDATE(),
	changed_by NVARCHAR(100),
	FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);