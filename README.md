# MateDiscreta

Este programa permite trabajar con proposiciones lógicas usando variables de una letra minúscula, operadores lógicos y paréntesis anidados.
Incluye funciones para generar tablas de verdad, verificar tautologías, comprobar equivalencias y realizar inferencias.

INSTRUCCIONES DE USO:

1. EJECUTAR EL PROGRAMA
2. SELECCIONAR UNA OPCIÓN DEL MENÚ
El programa mostrará las siguientes opciones:
- Tabla de verdad
- Verificar tautología
- Verificar equivalencias
- Realizar inferencia
- Finalizar
Escriba el número de la opción deseada y presione ENTER.
3. INGRESAR LA PROPOSICIÓN
Use variables de una sola letra minúscula (a–z).
Use los operadores lógicos permitidos:
- not
- and
- or
- |implies|
- |iff|
Puede usar paréntesis anidados.

EJEMPLOS:

tabla_verdad:
    a and b             -> [[False, False, False], [False, True, False], [True, False, False], [True, True, True]]
    not (a |implies| b) -> [[False, False, False], [False, True, False], [True, False, True], [True, True, False]]
    a or (b and c)      -> [[False, False, False, False], [False, False, True, False], [False, True, False, False], [False, True, True, True], [True, False, False, True], 
                           [True, False, True, True], [True, True, False, True], [True, True, True, True]]

tautología:
    a or (not a)          -> True
    (a and b) |implies| a -> True
    p |iff| q             -> False

equivalentes
    not (not p), p                    -> True
    p |implies| q, not p or q         -> True
    not (a and b), not a and not b    -> False
    a, b                              -> False 

inferencia
    a or b = 1          -> [[False, True], [True, False], [True, True]]
    a |implies| b = 0   -> [[True, False]]
    a and not a = 1     -> []