import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



# CONFIGURACIÓN DEL DRIVER


@pytest.fixture
def driver():

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)

    driver.maximize_window()

    yield driver

    driver.quit()



# FUNCIÓN PARA LOGIN


def realizar_login(driver):

    wait = WebDriverWait(driver, 10)

    driver.get("https://www.saucedemo.com/")

    
    usuario = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "user-name")
        )
    )

    usuario.send_keys("standard_user")

    
    password = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "password")
        )
    )

    password.send_keys("secret_sauce")

    
    boton_login = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "login-button")
        )
    )

    boton_login.click()

    
    wait.until(
        EC.url_contains("/inventory.html")
    )



# TEST 01 - LOGIN


def test_01_login(driver):

    realizar_login(driver)

    assert "/inventory.html" in driver.current_url, \
        "ERROR: No se redirigió a inventory.html"



# TEST 02 - VERIFICAR INVENTARIO


def test_02_verificar_inventario(driver):

    realizar_login(driver)

    wait = WebDriverWait(driver, 10)

    
    wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "inventory_list")
        )
    )

    page_title = driver.title

    assert page_title == "Swag Labs", \
        f'ERROR: título de ventana esperado "Swag Labs", obtenido "{page_title}"'



# TEST 03 - PRODUCTOS VISIBLES


def test_03_productos_visibles(driver):

    realizar_login(driver)

    wait = WebDriverWait(driver, 10)

    
    inventory_items = wait.until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "inventory_item")
        )
    )

    assert len(inventory_items) > 0, \
        "ERROR: No se encontraron productos"

    
    productos_visibles = [
        producto
        for producto in inventory_items
        if producto.is_displayed()
    ]

    assert len(productos_visibles) > 0, \
        "ERROR: No hay productos visibles"



# TEST 04 - VALIDAR INTERFAZ


def test_04_validar_interfaz(driver):

    realizar_login(driver)

    wait = WebDriverWait(driver, 10)

    
    menu_button = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "react-burger-menu-btn")
        )
    )

    
    filtro = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "product_sort_container")
        )
    )

    assert menu_button.is_displayed(), \
        "ERROR: El menú no está visible"

    assert filtro.is_displayed(), \
        "ERROR: El filtro no está visible"



# TEST 05 - AÑADIR PRODUCTO AL CARRITO


def test_05_anadir_producto_al_carrito(driver):

    wait = WebDriverWait(driver, 10)

    realizar_login(driver)

    
    boton_agregar = wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".inventory_item:first-child button.btn_inventory"
            )
        )
    )

    
    boton_agregar.click()

    
    wait.until(
        EC.text_to_be_present_in_element(
            (
                By.CSS_SELECTOR,
                ".inventory_item:first-child button.btn_inventory"
            ),
            "Remove"
        )
    )

    
    boton_remove = wait.until(
        EC.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                ".inventory_item:first-child button.btn_inventory"
            )
        )
    )

    
    assert boton_remove.text.strip() == "Remove", \
        f'ERROR: Se esperaba "Remove", obtenido "{boton_remove.text}"'




# TEST 06 - VERIFICAR CONTADOR DEL CARRITO


def test_06_verificar_contador_carrito(driver):

    realizar_login(driver)

    wait = WebDriverWait(driver, 10)

    
    first_item = wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "inventory_item")
        )
    )

    
    boton_agregar = first_item.find_element(
        By.CSS_SELECTOR,
        "button.btn_inventory"
    )

    wait.until(
        lambda d: boton_agregar.is_displayed()
        and boton_agregar.is_enabled()
    )

    boton_agregar.click()

    
    contador_carrito = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "shopping_cart_badge")
        )
    )

    
    wait.until(
        lambda d: contador_carrito.text.strip() == "1"
    )

    assert contador_carrito.text.strip() == "1", \
        f'ERROR: Se esperaba 1, obtuvo "{contador_carrito.text}"'



# TEST 07 - NAVEGAR AL CARRITO


def test_07_navegar_carrito(driver):

    realizar_login(driver)

    wait = WebDriverWait(driver, 10)

    
    first_item = wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "inventory_item")
        )
    )

    boton_agregar = first_item.find_element(
        By.CSS_SELECTOR,
        "button.btn_inventory"
    )

    wait.until(
        lambda d: boton_agregar.is_displayed()
        and boton_agregar.is_enabled()
    )

    boton_agregar.click()

    
    wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "shopping_cart_badge")
        )
    )

    
    carrito = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "shopping_cart_link")
        )
    )

    carrito.click()

    
    wait.until(
        EC.url_contains("/cart.html")
    )

    assert "/cart.html" in driver.current_url, \
        "ERROR: No se redirigió a /cart.html"



# TEST 08 - COMPROBAR PRODUCTO EN EL CARRITO


def test_08_comprobar_producto_en_el_carrito(driver):

    realizar_login(driver)

    wait = WebDriverWait(driver, 10)

    
    first_item = wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "inventory_item")
        )
    )

    
    producto_nombre_inventario = first_item.find_element(
        By.CLASS_NAME,
        "inventory_item_name"
    ).text

    
    boton_agregar = first_item.find_element(
        By.CSS_SELECTOR,
        "button.btn_inventory"
    )

    wait.until(
        lambda d: boton_agregar.is_displayed()
        and boton_agregar.is_enabled()
    )

    boton_agregar.click()

    
    wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "shopping_cart_badge")
        )
    )

    
    carrito = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "shopping_cart_link")
        )
    )

    carrito.click()

    
    wait.until(
        EC.url_contains("/cart.html")
    )

    
    producto_nombre_en_carrito = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "inventory_item_name")
        )
    )

    
    assert producto_nombre_en_carrito.text == producto_nombre_inventario, \
        (
            "ERROR: El producto del carrito no coincide. "
            f"Esperado: {producto_nombre_inventario}, "
            f"Obtenido: {producto_nombre_en_carrito.text}"
        )
