Automatización de pruebas - SauceDemo
Propósito del proyecto

Este proyecto tiene como objetivo automatizar pruebas funcionales sobre la aplicación web SauceDemo utilizando Python, Pytest y Selenium WebDriver.

Las pruebas verifican diferentes funcionalidades principales de la aplicación, entre ellas:

Inicio de sesión con un usuario válido.

Redirección a la página de inventario.

Verificación del título de la aplicación.

Visualización de productos.

Verificación de elementos de la interfaz.

Agregado de productos al carrito.

Verificación del contador del carrito.

Navegación hacia el carrito.

Verificación del producto agregado al carrito.

El proyecto utiliza esperas explícitas para sincronizar las pruebas con el comportamiento de la aplicación y evitar errores producidos por tiempos de carga o actualizaciones dinámicas del DOM.



Tecnologías utilizadas

Python 3

Lenguaje principal utilizado para desarrollar las pruebas.

Pytest

Framework utilizado para organizar y ejecutar los casos de prueba.

Selenium WebDriver

Herramienta utilizada para automatizar la interacción con el navegador.

webdriver-manager

Permite gestionar automáticamente la instalación del ChromeDriver compatible con el navegador.

Google Chrome

Navegador utilizado para ejecutar las pruebas automatizadas.






Usuario utilizado para las pruebas

Las pruebas utilizan el usuario estándar proporcionado por SauceDemo:

Usuario: standard_user
Password: secret_sauce


La aplicación utilizada para las pruebas es:

https://www.saucedemo.com/

Consideraciones

Cada prueba realiza su propio login y utiliza una instancia independiente del navegador.

Esto permite que las pruebas sean independientes entre sí y puedan ejecutarse individualmente sin depender del resultado o del estado dejado por otra prueba.


