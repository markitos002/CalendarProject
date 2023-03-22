def error_msg():
    print()
    print("Uso: CursoCalendario2.py <mes> <anio>")
    print("Uso: CursoCalendario2.py <anio>")
    print()
    print("   <mes> Valor entero entre 1 y 12")
    print("   <anio> Valor entero mayor o igual a 1900")
    print()
    print("Ejemplo: CursoCalendario2.py 3 2023")
    print("Ejemplo: CursoCalendario2.py 2023")
    print()
    return None



def dia_mes(dia, mes, anio):
    if mes in [1,2]:
        mes += 12
        anio -= 1
    q, m, y = dia, mes, anio
    h = (q + (13*(m+1)//5) + y + (y//4 )- (y//100) + (y//400)) % 7 #formula de Zeller que identifica el dia de la semana
    return (h - 1) % 7 #retorna el dia de la semana (0:dom, 1:lun, 2:mar, 3:mie, 4:jue, 5:vie, 6:sab)
    # 0: sab -> 6, 
    # 1: dom -> 0, 
    # 2: lun -> 1, 
    # 3: mar -> 2, ...
    #retorna el dia de una mes (mes/anio) 0:Dom, 1 Lun, 2 Mar...

def num_dias_mes(mes, anio):
    #retorna el numero de dias del mes y anio dados (mes/anio)
    if mes == 2:
        if anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0):
            return 29
        else:
            return 28
    elif mes in [4, 6, 9, 11]:
        return 30
    else:
        return 31

def print_calendario_anual(anio, calendario_anual):
    #imprime una lista de calendarios (12 elementos) en formato de calendario anual
    nombre_mes = {0:"ENERO", 1:"FEBRERO", 2:"MARZO", 3:"ABRIL", 
                  4:"MAYO", 5:"JUNIO", 6:"JULIO", 7:"AGOSTO", 
                  8:"SEPTIEMBRE", 9:"OCTUBRE", 10:"NOVIEMBRE", 
                  11:"DICIEMBRE"}
    print(f"{anio:^80}")
    print()
    for mes in range(0,12,3):
        print(f"{nombre_mes[mes]:30}", end='')
        print(f"{nombre_mes[mes+1]:30}", end='')
        print(f"{nombre_mes[mes+2]:30}")

        print(f"{' D  L  M  M  J  V  S':30}", end='')
        print(f"{' D  L  M  M  J  V  S':30}", end='')
        print(f"{' D  L  M  M  J  V  S':30}")

        for i in range(0, 42, 7):
            print("{:2} {:2} {:2} {:2} {:2} {:2} {:2}          ".format(*calendario_anual[mes][i:i+7]), end='')  #funcion splat (*)
            print("{:2} {:2} {:2} {:2} {:2} {:2} {:2}          ".format(*calendario_anual[mes+1][i:i+7]), end='')
            print("{:2} {:2} {:2} {:2} {:2} {:2} {:2}          ".format(*calendario_anual[mes+2][i:i+7]))
        
        print()


def print_calendario(mes, calendario):
    #imprime una lista de dias (42 elementos) en formato de calendario mensual
    nombre_mes = {1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril', 
                  5:'Mayo', 6:'Junio', 7:'Julio', 8:'Agosto', 
                  9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'}
    print(nombre_mes[mes])
    print(" D  L  M  M  J  V  S")
    
    for idx, dia in enumerate(calendario, start=1):
        print(f"{dia:2}", end=" ")
        if idx % 7 == 0:
            print()




"""
    print(nombre_mes[mes])
    print(" D  L  M  M  J  V  S")
    for idx, dia in enumerate(calendario, start=1):
        print(f"{dia:2}", end=" ")
        if idx % 7 == 0:
            print()
"""
