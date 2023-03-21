mes = input("ingrese el mes [1-12]: ")
anio = int(input("ingrese el año[>=1900]: "))


# peticion validada del mes
mes_valido = False
while not mes_valido:
    try:
        mes = int(input ("ingrese el mes >> [1-12]:"))
        if mes >= 1 and mes <= 12:
            mes_valido = True
            
        else:
            print("El mes debe ser un número entero entre 1 y 12")
    except ValueError:
        print("El mes debe ser un número entero entre 1 y 12")

#peticion validada del anio
anio_valido = False
while not anio_valido:
    try:
        anio = int(input ("ingrese el anio :"))
        if anio > 1900:
            anio_valido = True
          
        else:
            print("El anio debe ser un número entero mayor a 1900")
    except ValueError:
        print("El anio debe ser un número entero mayor a 1900")

if mes_valido and anio_valido:
# mostramos el calendario del mes y del anio
    calendario = [''] * 42
    idx = dia_mes (1, mes,  anio)
    n_dias = num_dias_mes (mes, anio)
    calendario [idx:idx+n_dias] = range (1, n_dias+1)

    print_calendario(mes, calendario)

def dia_mes(dia, mes, anio):
    #retorna el indice del dia en el calendario (mes/anio). 0:Dom, 1:Lun, 2:Mar, 3:Mie, 4:Jue, 5:Vie, 6:Sab
    pass

def num_dias_mes(mes, anio):
    #retorna el numero de dias del mes y anio dados
    pass

def print_calendario(mes, calendario):
    #imprime el calendario del mes y anio dados
    pass
