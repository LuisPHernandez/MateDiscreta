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

# Función que devuelve False si una expresión tiene mayúsculas, dígitos, símbolos especiales no aceptados o esta vacía
def es_proposicion_valida(expr: str) ->bool:
    # Si la expresión esta vacía, se devuelve False
    if not expr:
        return False

    # Se usa una expresión regular para buscar en el string.
    # Se devuelve False si se encuentra algo que no sea (^) minúscula (a-z), espacio (\s), '=', '(', ')' o '|'
    return not bool(re.search(r"[^a-z=\s\(\)\|]", expr))

# Función que devuelve False si una expresión tiene mayúsculas, símbolos especiales no aceptados, no tiene exactamente un '=' y un 0/1 o esta vacía
def es_expr_de_inferencia_valida(expr: str) ->bool:
    # Si la expresión esta vacía, se devuelve False
    if not expr:
        return False
    expr = expr.strip()

    # 1. Buscar exactamente un '='
    partes = expr.split("=")
    if len(partes) != 2:
        return False
    
    # 2. Buscar exactamente un 0/1 despues del '='
    valor_de_verdad = partes[1].split()
    if (valor_de_verdad != "0" and valor_de_verdad != "1"):
        return False
    
    # 3. Verificar que la parte izquierda de la igualdad sea válida
    return es_proposicion_valida(partes[0])

# Función que itera sobre todos los valores de verdad posibles para un número n de variables (por si no se puede usar itertools)
def producto_binario(n):
    if n == 0:
        yield ()
    else:
        for val in [False, True]:
            for resto in producto_binario(n - 1):
                yield (val,) + resto

# Función que devuelve una lista de listas de valores booleanos que representan la tabla de verdad de una proposición
def tabla_verdad(expr: str) ->list[list[bool]]:
    # 1. Verificar que la proposición cumpla con las restricciones, si no las cumple se termina la ejecución
    if (not es_proposicion_valida(expr)):
        raise ValueError("Proposición inválida: use solo variables en minúscula")

    # 2. Extraer variables usando la función de la plantilla
    var_presentes = extract_variables(expr)
    print(var_presentes)
    
    tabla = []

     # 3. Ciclo para generar todas las combinaciones posibles de valores de verdad
    for valores_de_verdad in itertools.product([False, True], repeat=len(var_presentes)):
        # 4. Crear diccionario que empareja las variables a sus valores de verdad de la iteración actual
        valor_actual = dict(zip(var_presentes, valores_de_verdad))
        
        # 5. Intentar evaluar la proposición para los valores de verdad de la iteración actual
        try:
            resultado = eval(expr, globals(), valor_actual)
        except:
            raise ValueError("Proposición sintácticamente inválida según las reglas de la lógica proposicional")
        
        # 6. Guardar los valores y el resultado en la tabla
        tabla.append(list(valores_de_verdad) + [resultado])
    
    return tabla

# Función que devuelve True si la proposición ingresada es una tautología, False para cualquier otro caso
def tautologia(expr: str) ->bool:
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

# Funcion que evalúa si 2 proposiciones son lógicamente equivalentes 
def equivalentes(expr1: str, expr2: str) ->bool:
    # 1. Verificar que las proposiciones cumplan con las restricciones, si no las cumplen se termina la ejecución
    if (not es_proposicion_valida(expr1) or not es_proposicion_valida(expr2)):
        raise ValueError("Proposición inválida: use solo variables en minúscula")

    # 2. Comprobar que ambas proposiciones tengan las mimas variables para que puedan ser consideradas equivalentes
    variables1 = extract_variables(expr1)
    variables2 = extract_variables(expr2)
    if set(variables1) != set(variables2):
        return False

    # 3. Sacar las tablas de verdad para las proposiciones ingresadas
    tabla1 = tabla_verdad(expr1)
    tabla2 = tabla_verdad(expr2)

    # 4. Verificar si las proposiciones tienen los mismos resultados para las mismas combinaciones de verdad
    contador_true = 0
    for i in range(len(tabla1)):
        if (tabla1[i][-1] == tabla2[i][-1]):
            contador_true += 1

    # 5. Devolver True si las proposiciones tienen los mismos resultados para todos los valores de verdad, False en cualquier otro caso
    return contador_true == len(tabla1)        

# Funcion que devuelve una lista de listas con los valores de verdad de las variables que satisfacen una igualdad ingresada
def inferencia(expr: str) ->list[list[bool]]:
    # 1. Verificar que la expresión cumpla con las restricciones, si no las cumple se termina la ejecución
    if (not es_expr_de_inferencia_valida(expr)):
        raise ValueError("Expresión inválida: use solo variables en minúscula y un único '=' seguido de un 0 o 1.")

    # 2. Asignar True o False al valor esperado dependiendo si la expresión tiene un '= 1' o un '= 0'
    proposicion, valor_str = expr.split("=")
    valor_esperado = True if valor_str.strip() == "1" else False

    # 3. Intentar crear la tabla de verdad de la proposición
    try:
        tabla = tabla_verdad(expr)
    except Exception as e:
        raise e

    # 4. Crear una nueva tabla solo con las combinaciones de valores de verdad que cumplen con la igualdad de la expresión
    resultados = []

    for combinacion in tabla:
        if (combinacion[-1] is valor_esperado):
            resultados.append(list(combinacion[0:-1]))

    return resultados

a = tabla_verdad('not (a |implies| b)')
print(a)
b = equivalentes('p |implies| q', 'not p or q')
print(b)
c = equivalentes('not (a and b)','not a and not b')
print(c)
d = equivalentes('a', 'a and c or (a and not c)')
print(d) 