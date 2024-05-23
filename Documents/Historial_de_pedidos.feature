Feature: Historial de Pedidos
  Como usuario registrado,
  Quiero poder ver el historial de mis pedidos,
  Para que pueda realizar un seguimiento de mis compras anteriores.

  Background:
    Given usuario registrado con los siguientes detalles:
      | nombre_usuario | contrasenia |
      | usuario1       | password1  |
    And los siguientes pedidos existen en el historial del usuario:
      | numero_pedido | fecha       | estado   | productos                       |cantidad | precio |
      | 123           | 2024-05-01  | Entregado| Producto A, Producto B          | 1       | 10.00  |
      | 124           | 2024-05-10  | Pendiente| Producto C                      |2        | 20.00  |
      | 125           | 2024-05-10  | Cancelado| Producto C                      |2        | 20.00  |

  Scenario: TC_1 Ver la opción "Historial de Pedidos" en el menu de navegacion
    Given el usuario "usuario1" ha iniciado sesion
    When el usuario accede al menu de navegación
    Then el usuario debe poder ver la opcion "Historial de Pedidos"

  Scenario:TC_2 Ver lista de pedidos anteriores
    Given el usuario "usuario1" ha iniciado sesion
    When el usuario accede a "Historial de Pedidos"
    Then el usuario puede ver una lista de sus pedidos anteriores
    And cada pedido debe mostrar el numero_pedido, fecha y el estado del pedido
    | numero_pedido | fecha       | estado   |
    | 123           | 2024-05-01  | Entregado|
    | 124           | 2024-05-10  | Pendiente|
    | 125           | 2024-05-10  | Cancelado|

  Scenario:TC_3 Ver detalles de un pedido específico
    Given el usuario "usuario1" ha iniciado sesión
    And el usuario está en "Historial de Pedidos"
    When el usuario hace clic en el pedido con número "123"
    Then el usuario debe ver los detalles del pedido con número "123"
    And los detalles deben incluir la lista de productos en el pedido

  Scenario:TC_4 Ver productos en el detalle de un pedido
    Given el usuario "usuario1" ha iniciado sesión
    And el usuario está viendo los detalles del pedido con número "123"
    Then el usuario debe ver los siguientes productos:
    | nombre del producto | cantidad | precio |
    | Producto A          | 1        | 10.00  |
    | Producto B          | 2        | 20.00  |


  Scenario:TC_5 Historial de pedidos vacio
    Given el usuario "usuario2" ha iniciado sesion
    And el usuario "usuario2" no tiene pedidos en su historial
    When el usuario accede a "Historial de Pedidos"
    Then el usuario no tiene historial de productos

  Scenario:TC_6 Ver productos con informacion incompleta
    Given el usuario "usuario1" ha iniciado sesión
    And el pedido con número "124" tiene un producto con información incompleta
    When el usuario hace clic en el pedido con número "124"
    Then el usuario debe ver los productos disponibles y un mensaje indicando que hay información incompleta
    | nombre del producto | cantidad | precio |
    | Producto C          | 1        | N/A    |

  Scenario:TC_7 Número maximo de pedidos
    Given el usuario "usuario3" ha iniciado sesion
    And tiene el numero maximo de pedidos permitidos
    When accede al historial de pedidos
    Then debe ver todos los pedidos mostrados correctamente

  Scenario:TC_8 Pedidos con cantidad maxima de productos
    Given el usuario "usuario3" ha iniciado sesion
    And tiene un pedido con la cantidad maxima de productos permitidos
    When accede al historial de pedidos
    Then debe ver todos los productos del pedido mostrados correctamente

  Scenario:TC_9 Pedidos con fechas limite
    Given el usuario "usuario3" ha iniciado sesion
    And tiene pedidos con fechas límite permitidas
    When accede al historial de pedidos
    Then debe ver los pedidos con las fechas mostradas correctamente
