from funcionesCal  import *
import sys


# >> python3 CursoCalendario2.py 1 2019
# sys.argv = ['CursoCalendario2.py', '1', '2019']


if len(sys.argv) == 1 or len(sys.argv) > 3:
   error_msg()
   sys.exit()

if len(sys.argv) == 2:
    try:
        anio = int(sys.argv[1])
        if anio < 1900:
            error_msg()
            sys.exit()
    except ValueError:
        error_msg()
        sys.exit()


    calendario_anual = []
    for mes in range(1, 13):
        calendario = [''] * 42
        idx = dia_mes (1, mes, anio)
        n_dias = num_dias_mes(mes, anio)
        calendario [idx:idx+n_dias] = range (1, n_dias+1)
        calendario_anual.append(calendario)

    print_calendario_anual(anio, calendario_anual)
    sys.exit()

if len(sys.argv) == 3:
    try:
        mes = int(sys.argv[1])
        if not mes >= 1 and mes <= 12:
            error_msg()
            sys.exit()
    except ValueError:
        error_msg()
        sys.exit()

    try:
        anio = int(sys.argv[2])
        if anio < 1900:
            error_msg.msg()
            sys.exit()
    except ValueError:
        error_msg.msg()
        sys.exit()

    calendario = [''] * 42
    idx = dia_mes (1, mes, anio)
    n_dias = num_dias_mes (mes, anio)
    calendario [idx:idx+n_dias] = range (1, n_dias+1)
    print_calendario(mes, calendario)
    sys.exit()



"""

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

if mes_valido and anio_valido:
# mostramos el calendario del mes y del anio
    calendario = [''] * 42
    idx = dia_mes (1, mes, anio)
    n_dias = num_dias_mes (mes, anio)
    calendario [idx:idx+n_dias] = range (1, n_dias+1)
    # idx:0 [1,2,3,4 ....,ndias, '','','',''] (42 elementos)
    # idx:1 ['','','',1,2,3,4 ....,ndias, '','',''] (42 elementos)

    print_calendario(mes, calendario)


#peticion validada del anio
anio_valido = False
while not anio_valido:
    try:
        anio = int(input ("ingrese el anio :"))
        if anio > 1900:
            anio_valido = True
          
        else:
            error_msg()
    except ValueError:
            error_msg()

"""
       