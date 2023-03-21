from funcionesCal  import dia_mes
from funcionesCal  import num_dias_mes
from funcionesCal  import print_calendario# importamos todas las funciones del modulo funciones_calendario

#mes = input("ingrese el mes [1-12]: ")
#anio = int(input("ingrese el año[>=1900]: "))

# peticion validada del mes, lazo condicionado
mes_valido = False
while not mes_valido:
    try:
        mes = int(input ("ingrese el mes >> [1-12]:"))
        if mes >= 1 and mes <= 12:
            mes_valido = True
            
        else:
            print("ERROR: El mes debe ser un número y debe ser entero entre 1 y 12")
    except ValueError:
        print("ERROR: El mes debe ser un número entero entre 1 y 12")

#peticion validada del anio
anio_valido = False
while not anio_valido:
    try:
        anio = int(input ("ingrese el anio :"))
        if anio > 1900:
            anio_valido = True
          
        else:
            print("ERROR: El anio debe ser un número y debe ser entero mayor a 1900")
    except ValueError:
        print("ERROR: El anio debe ser un número entero mayor a 1900")

if anio_valido:
    calendario_anual = []
    for mes in range(1,13):
        calendario = [''] * 42
        idx = dia_mes (1, mes, anio)
        n_dias = num_dias_mes(mes, anio)
        calendario [idx:idx+n_dias] = range (1, n_dias+1)
        calendario_anual.append(calendario)

    print_calendario_anual(anio, calendario_anual)

"""

if mes_valido and anio_valido:
# mostramos el calendario del mes y del anio
    calendario = [''] * 42
    idx = dia_mes (1, mes, anio)
    n_dias = num_dias_mes (mes, anio)
    calendario [idx:idx+n_dias] = range (1, n_dias+1)
    # idx:0 [1,2,3,4 ....,ndias, '','','',''] (42 elementos)
    # idx:1 ['','','',1,2,3,4 ....,ndias, '','',''] (42 elementos)

    print_calendario(mes, calendario)

"""
       