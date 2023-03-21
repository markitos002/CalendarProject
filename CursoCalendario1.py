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

# if mes_valido and anio_valido:
# mostramos el calendario


