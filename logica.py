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

#FUncion que evalua 2 expresiones, para ver si son logicamente equivalentes 
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



    