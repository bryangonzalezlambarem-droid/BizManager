<div align="center">
  <h1>Proyecto BizManager</h1>
  <p>Gestión de inventarios, pedidos, clientes y vendedores con Flask</p>
</div>

<div>
  <h2>Tecnologías utilizadas</h2>
  <p>Python 3.x, Flask, SQLAlchemy, JWT, AES, HTML, CSS, JavaScript, SQL Server</p>
</div>

<div>
  <h2>Funcionalidades</h2>
  <p>- CRUD de vendedores con validación de email, teléfono y contraseña.</p>
  <p>- CRUD de clientes con validación de email y teléfono, y sanitización para prevenir XSS.</p>
  <p>- CRUD de productos con validación de precio y stock, y control de acceso mediante JWT.</p>
  <p>- Gestión de pedidos: creación, actualización de estado, historial, vinculación con clientes y vendedores.</p>
  <p>- Seguridad: JWT, prevención de SQL Injection, sanitización de entradas, transacciones y manejo de errores.</p>
</div>

<div>
  <h2>Endpoints principales</h2>
  <p>- <strong>/auth/login</strong> (POST): Iniciar sesión y obtener JWT</p>
  <p>- <strong>/auth/logout</strong> (POST): Cerrar sesión</p>
  <p>- <strong>/customers/</strong> (GET, POST): Consultar o crear clientes</p>
  <p>- <strong>/customers/&lt;id&gt;</strong> (GET, PUT, DELETE): Consultar, actualizar o eliminar cliente</p>
  <p>- <strong>/products/</strong> (GET, POST): Consultar o crear productos</p>
  <p>- <strong>/products/&lt;id&gt;</strong> (GET, PUT, DELETE): Consultar, actualizar o eliminar producto</p>
  <p>- <strong>/orders/</strong> (GET, POST): Consultar o crear pedidos</p>
  <p>- <strong>/orders/&lt;id&gt;</strong> (GET, PUT, DELETE): Consultar, actualizar estado o eliminar pedido</p>
  <p>- <strong>/salespersons/</strong> (GET, POST): Consultar o crear vendedores</p>
  <p>- <strong>/salespersons/&lt;id&gt;</strong> (GET, PUT, DELETE): Consultar, actualizar o eliminar vendedor</p>
</div>

<div>
  <h2>Autor</h2>
  <p>Bryan Gonzalez Lambarem</p>
</div>
