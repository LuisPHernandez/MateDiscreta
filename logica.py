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

# Función que devuelve una lista de listas de valores booleanos que representan la tabla de verdad de una proposición
def tabla_verdad(expr: str) ->list[list[bool]]:
    # 1. Extraer variables usando la función de la plantilla
    var_presentes = [v for v in extract_variables(expr) if v not in PALABRAS_RESERVADAS]
    
    tabla = []

     # 2. Ciclo para generar todas las combinaciones posibles de valores de verdad
    for valores_de_verdad in itertools.product([False, True], repeat=len(var_presentes)):
        valor_actual = dict(zip(var_presentes, valores_de_verdad))
        
        # 3. Evaluar la proposición para los valores de verdad de la iteración actual
        resultado = eval(expr, globals(), valor_actual)
        
        # 4. Guardar los valores y el resultado en la tabla
        tabla.append(list(valores_de_verdad) + [resultado])
    
    return tabla

# Función que devuelve True si la proposición ingresada es una tautología, False para cualquier otro caso
def tautologia(expr: str) ->bool:
    # 1. Sacar la tabla de verdad para la proposición ingresada
    tabla = tabla_verdad(expr)

    # 2. Ciclo para verificar si los resultados para todos los valores de verdad son True
    contador_true = 0
    for fila in tabla:
        if (fila[-1] is True):
            contador_true += 1
    
    # 3. Devolver True si la proposición es verdadera para todos los valores de verdad, False en cualquier otro caso
    return contador_true == len(tabla)

# Funcion que evalua 2 expresiones, para ver si son logicamente equivalentes 
def equivalentes(expr1: str, expr2: str):

   # se modifican ambas expresiones, para estar listas para ser evaluadas 
    e1 = expr1.lower().replace("|iff|", "==").replace("|implies|","<=")

    e2= expr2.lower().replace("|iff|", "==").replace("|implies|","<=")
    # se buscan todos los tokens en cada expresion
    tokens1 = re.findall(r"[a-z]+",e1)
    tokens2 = re.findall(r"[a-z]+",e2)

    ##Juntar la lista de variables de ambas expresiones
    tokens_total = tokens1 + tokens2
    #obtener las variables presentes en tokens 1 y 2, se ponene en orden ascendente
    var_presentes = sorted({i for i in tokens_total if i in VARIABLES and i not in PALABRAS_RESERVADAS})
    
    # ciclo que pasa por todas las combinaciones de valores de verdad de las variables
    for valores_Verdad in itertools.product([False, True], repeat = len(var_presentes)):
        #Se empajera la variable con su valor de verdad en un diccionario
        valor_actual = dict(zip(var_presentes,valores_Verdad))

        # se evalua la expresion en base al valor actual
        resultado1 = eval(e1,{},valor_actual)
        resultado2 = eval(e2,{},valor_actual)

        # se compara cada resultado como un boolenado
        if bool(resultado1) != bool(resultado2):
            #Si algun resultado es distinto, se regresa false porque no son equivalentes, no es necesario seguir con el ciclo
            return False
    # una vez se evaluen todos los resultados y sea iguales, se regresa True, porque son equivalentes 
    return True

b = equivalentes('p |implies| q', 'not a or b')
print(b)
c = equivalentes('not (a and b)','not a and not b')
print(c)


def _normaliza(expr: str) -> str:
    # minusculas + reemplazos lógicos
    e = expr.lower()
    e = e.replace("|iff|", "==").replace("|implies|", "<=")
    return e


def tautologia(expr: str) -> bool:
    """
    Retorna True si la proposición 'expr' es una tautología.
    - Variables válidas: letras minúsculas a..z
    - Operadores: not, and, or, |implies|, |iff|
    """
    # Normalizar (lower + reemplazos)
    e = _normaliza(expr)

    # se buscan los tokens
    tokens = re.findall(r"[a-z]+", e)
    invalidos = [t for t in tokens if t not in VARIABLES and t not in PALABRAS_RESERVADAS]
    if invalidos:
        raise ValueError(f"Token(s) inválido(s): {sorted(set(invalidos))}")

    # Variables presentes (orden ascendente)
    var_presentes = sorted({t for t in tokens if t in VARIABLES})

    # Generar 2^n combinaciones en orden binario convencional
    for valores in itertools.product([False, True], repeat=len(var_presentes)):
        asignacion = dict(zip(var_presentes, valores))
        # Evaluar con entorno seguro: sin globals, solo las variables
        try:
            valor = eval(e, {}, asignacion)
        except NameError as ex:
            # Si hubiera algo raro sin definir
            raise ValueError(f"Variable no definida en la expresión: {ex}") from ex
        # Si alguna fila da False, no es tautología
        if not bool(valor):
            return False
    return True


print(tautologia('(a and b) |implies| a'))  
print(tautologia('p |iff| q'))              

def inferencia(expr: str) -> list[list[bool]]:
    expr = expr.lower().strip()

    # Separa la posicion y el valor que se espera.
    if "=" not in expr:
        raise ValueError("La proposición debe contener un '=' seguido de 0 o 1.") # si no hay un '=' en la expresion tira error.
    proposicion, valor_str = expr.split("=")
    valor_esperado = True if valor_str.strip() == "1" else False # si el valor esperado es 1 es Verdadero y si es 0 es falso.

    # Encuentra las variables presentes.
    tokens = re.findall(r"[a-z]+", proposicion)
    # hace una revision para asegurarse de que t no sea una palabra reservada.
    var_presentes = sorted({t for t in tokens if t in VARIABLES and t not in PALABRAS_RESERVADAS})

    # convierte los operadores para poder usarlos.
    proposicion = proposicion.replace("|iff|", "==").replace("|implies|", "<=")

    resultados = []

    # Prueba todas las combinaciones posibles.
    for combinacion in itertools.product([False, True], repeat=len(var_presentes)):
        # Hace parejas de los valores y las posibles combinaciones en el diccionario.
        valores = dict(zip(var_presentes, combinacion))
        try:
            resultado = eval(proposicion, {}, valores)
        except Exception as e:
            raise ValueError(f"Error al evaluar la proposición: {e}")

        if resultado == valor_esperado:
            resultados.append(list(combinacion))

    return resultados