import re, itertools

VARIABLES = list(map(chr, range(97, 123)))
PALABRAS_RESERVADAS = {"and", "or", "not", "implies", "iff"}

# Función que devuelve una lista de listas de valores booleanos que representan la tabla de verdad de una proposición
def tabla_de_verdad(proposicion: str):
    # Se encuentran todas las palabras y variables en la proposición usando una expresion regular
    tokens = re.findall(r"[a-z]+", proposicion.lower())

    # Se extraen las variables y se ordenan en forma ascendente
    var_presentes = sorted({i for i in tokens if i in VARIABLES and i not in PALABRAS_RESERVADAS})
    
    # Se prepara la proposicion para ser evaluada
    proposicion = proposicion.replace("|iff|", "==").replace("|implies|", " <= ")

    print(proposicion)

    # Se crea la lista que funcionará como tabla de verdad
    tabla = []

    # Se itera sobre todas las combinaciones posibles de valores de verdad dependiendo del número de variables usando itertools
    for valores_de_verdad in itertools.product([False, True], repeat=len(var_presentes)):
        # Se asigna el valor de verdad correspondiente a la iteración a cada variable usando un diccionario
        valor_actual = dict(zip(var_presentes, valores_de_verdad))

        # Se obtiene el resultado de la proposicion con los valores actuales de verdad
        resultado = eval(proposicion, {}, valor_actual)

        # Se guarda la lista correspondiente a la iteracion en la tabla de verdad
        tabla.append(list(valores_de_verdad) + [resultado])

    return tabla


a = tabla_de_verdad("(not (a and b)) |implies| (c and a)") 
print(a)