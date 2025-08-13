import re, itertools
from functools import partial

# ********************** COMIENZO PLANTILLA *******************************
class Infix(object):
    def __init__(self, func):
        self.func = func
    def __or__(self, other):
        return self.func(other)
    def __ror__(self, other):
        return Infix(partial(self.func, other))
    def __call__(self, v1, v2):
        return self.func(v1, v2)
    
@Infix
def implies(p, q) :
    return not p or q

@Infix
def iff(p, q) :
    return (p |implies| q) and (q |implies| p)

def extract_variables(expression):
    sorted_variable_set = sorted(set(re.findall(r'\b[a-z]\b', expression)))
    return sorted_variable_set
# ********************** FIN PLANTILLA ************************************

VARIABLES = list(map(chr, range(97, 123)))
PALABRAS_RESERVADAS = {"and", "or", "not", "implies", "iff"}

def es_proposicion_valida(expr: str) ->bool:
    """
    Función que devuelve False si una expresión tiene mayúsculas, dígitos, símbolos especiales no aceptados 
    o esta vacía.
    """
    # Si la expresión esta vacía, se devuelve False
    if not expr:
        return False

    # Se usa una expresión regular para buscar en el string.
    # Se devuelve False si se encuentra algo que no sea (^) minúscula (a-z), espacio (\s), '(', ')' o '|'
    return not bool(re.search(r"[^a-z\s\(\)\|]", expr))

def es_expr_de_inferencia_valida(expr: str) ->bool:
    """
    Función que devuelve False si una expresión tiene mayúsculas, símbolos especiales no aceptados, 
    no tiene exactamente un '=' seguido de un 0/1 o esta vacía.
    """
    # Si la expresión esta vacía, se devuelve False
    if not expr:
        return False
    expr = expr.strip()

    # 1. Buscar exactamente un '='
    partes = expr.split("=")
    if len(partes) != 2:
        return False
    
    # 2. Buscar exactamente un 0/1 despues del '='
    valor_de_verdad = partes[1].strip()
    if (valor_de_verdad != "0" and valor_de_verdad != "1"):
        return False
    
    # 3. Verificar que la parte izquierda de la igualdad sea válida
    return es_proposicion_valida(partes[0])

def producto_binario(n):
    """
    Función que itera sobre todos los valores de verdad posibles para un número n de variables 
    (reemplazo de itertools.product())
    """
    if n == 0:
        yield ()
    else:
        for val in [False, True]:
            for resto in producto_binario(n - 1):
                yield (val,) + resto

def tabla_verdad(expr: str) ->list[list[bool]]:
    """
    Función que devuelve una lista de listas de valores booleanos que representan la tabla de 
    verdad de una proposición
    """
    # 1. Verificar que la proposición cumpla con las restricciones, si no las cumple se termina la ejecución
    if (not es_proposicion_valida(expr)):
        raise ValueError("Proposición inválida: use solo letras minúsculas para variables")

    # 2. Extraer variables usando la función de la plantilla
    var_presentes = extract_variables(expr)
    
    tabla = []

    # 3. Ciclo para generar todas las combinaciones posibles de valores de verdad
    for valores_de_verdad in itertools.product([False, True], repeat=len(var_presentes)):
        # 4. Crear diccionario que empareja las variables a sus valores de verdad de la iteración actual
        valor_actual = dict(zip(var_presentes, valores_de_verdad))
        
        # 5. Intentar evaluar la proposición para los valores de verdad de la iteración actual
        try:
            resultado = eval(expr, globals(), valor_actual)
        except Exception as e:
            raise ValueError("Proposición sintácticamente inválida según las reglas de la lógica proposicional")
        
        # 6. Guardar los valores y el resultado en la tabla
        tabla.append(list(valores_de_verdad) + [resultado])
    
    return tabla

def tautologia(expr: str) ->bool:
    """
    Función que devuelve True si la proposición ingresada es una tautología, False para cualquier 
    otro caso
    """
    # 1. Se verifica que la proposición cumpla con las restricciones, si no las cumple se termina la ejecución
    if (not es_proposicion_valida(expr)):
        raise ValueError("Proposición inválida: use solo variables en minúscula")
    
    # 2. Intentar sacar la tabla de verdad para la proposición ingresada
    try:
        tabla = tabla_verdad(expr)
    except Exception as e:
        raise e

    # 3. Ciclo para verificar si los resultados para todos los valores de verdad son True
    contador_true = 0
    for fila in tabla:
        if (fila[-1] is True):
            contador_true += 1
    
    # 4. Devolver True si la proposición es verdadera para todos los valores de verdad, False en cualquier otro caso
    return contador_true == len(tabla)

def equivalentes(expr1: str, expr2: str) ->bool:
    """
    Funcion que evalúa si 2 proposiciones son lógicamente equivalentes. Devuelve True si lo son,
    False si no lo son.
    """
    # 1. Verificar que las proposiciones cumplan con las restricciones, si no las cumplen se termina la ejecución
    if (not es_proposicion_valida(expr1) or not es_proposicion_valida(expr2)):
        raise ValueError("Proposición inválida: use solo variables en minúscula")

    # 2. Comprobar que ambas proposiciones tengan las mimas variables para que puedan ser consideradas equivalentes
    variables1 = extract_variables(expr1)
    variables2 = extract_variables(expr2)
    if set(variables1) != set(variables2):
        return False

    # 3. Intentar sacar las tablas de verdad para las proposiciones ingresadas
    try:
        tabla1 = tabla_verdad(expr1)
        tabla2 = tabla_verdad(expr2)
    except Exception as e:
        raise e

    # 4. Verificar si las proposiciones tienen los mismos resultados para las mismas combinaciones de verdad
    contador_true = 0
    for i in range(len(tabla1)):
        if (tabla1[i][-1] == tabla2[i][-1]):
            contador_true += 1

    # 5. Devolver True si las proposiciones tienen los mismos resultados para todos los valores de verdad, False en cualquier otro caso
    return contador_true == len(tabla1)        

def inferencia(expr: str) ->list[list[bool]]:
    """
    Funcion que devuelve una lista de listas con los valores de verdad de las variables que 
    satisfacen una igualdad ingresada.
    """
    # 1. Verificar que la expresión cumpla con las restricciones, si no las cumple se termina la ejecución
    if (not es_expr_de_inferencia_valida(expr)):
        raise ValueError("Expresión inválida: use solo variables en minúscula y un único '=' seguido de un 0 o 1.")

    # 2. Asignar True o False al valor esperado dependiendo si la expresión tiene un '= 1' o un '= 0'
    proposicion, valor_str = expr.split("=")
    valor_esperado = True if valor_str.strip() == "1" else False

    # 3. Intentar crear la tabla de verdad de la proposición
    try:
        tabla = tabla_verdad(proposicion)
    except Exception as e:
        raise e

    # 4. Crear una nueva tabla solo con las combinaciones de valores de verdad que cumplen con la igualdad de la expresión
    resultados = []

    for combinacion in tabla:
        if (combinacion[-1] is valor_esperado):
            resultados.append(list(combinacion[0:-1]))

    return resultados

def main():
    """
    Punto de acceso al programa.
    """
    while True:
        print("\n--- Menu Principal ---")
        print("1. Tabla de verdad")
        print("2. Verificar tautologia")
        print("3. Verificar equivalencias")
        print("4. Realizar inferencia")
        print("5. Finalizar")

        opcion = input("Seleccione el numero una opción: ").strip()

        if opcion == "1":
            expr = input("Ingrese la proposición: ").strip()
            try:
                tabla = tabla_verdad(expr)
                for fila in tabla:
                    print(fila)
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "2":
            expr = input("Ingrese la proposición: ").strip()
            try:
                if tautologia(expr):
                    print("La proposición sí es una tautología.")
                else:
                    print("La proposición no es una tautología.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "3":
            expr1 = input("Ingrese la primera proposición: ").strip()
            expr2 = input("Ingrese la segunda proposición: ").strip()
            try:
                if equivalentes(expr1, expr2):
                    print("Las proposiciones son lógicamente equivalentes.")
                else:
                    print("Las proposiciones no son equivalentes.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "4":
            expr = input("Ingrese la expresión con igualdad (ej: a and b = 1): ").strip()
            try:
                resultados = inferencia(expr)
                if resultados:
                    print("Combinaciones que cumplen la inferencia:")
                    for fila in resultados:
                        print(fila)
                else:
                    print("No hay combinaciones que cumplan la inferencia.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "5":
            print("Finalizando el programa...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()