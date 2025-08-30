-- B. G. L. 30/08/2025 Insertar un vendedor
INSERT INTO Salespeople (name, email, phone, registration_date)
VALUES ('Carlos Rodríguez', 'carlos.rodriguez@empresa.com', '+34 912 345 678', GETDATE());

-- B. G. L. 30/08/2025 Insertar un cliente
INSERT INTO Customers (name, email, phone, adress)
VALUES ('María González', 'maria.gonzalez@cliente.com', '+34 623 456 789', 'Calle Mayor 123, Madrid');

-- B. G. L. 30/08/2025 Insertar un producto (usando el salesman_id del vendedor insertado)
INSERT INTO Products (name, description, price, stock, salesman_id)
VALUES ('Portátil Gaming', 'Portátil gaming i7, 16GB RAM, RTX 4060', 1299.99, 15, 1);

-- B. G. L. 30/08/2025 Insertar un pedido (usando el customer_id del cliente insertado)
INSERT INTO Orders (customer_id, order_date, status, total_amount)
VALUES (1, GETDATE(), 'Pending', 1299.99);

-- B. G. L. 30/08/2025 Insertar detalle del pedido (usando los IDs de pedido, producto y vendedor)
INSERT INTO OrderDetails (order_id, product_id, salesman_id, quantity, unit_price)
VALUES (1, 1, 1, 1, 1299.99);

-- B. G. L. 30/08/2025 Insertar historial de estado del pedido
INSERT INTO OrderStatusHistory (order_id, old_status, new_status, change_date, changed_by)
VALUES (1, NULL, 'Pending', GETDATE(), 'Sistema');