import json
from datetime import datetime

def get_data():
    with open(r'bd/horario_estudiantes.json', 'r') as file:
        data = json.load(file)
    return data
global datos
datos = get_data()

def comprobar(doc: str, dia: str , hora: int):
    # print(doc, dia, hora)
    if doc in datos: #si el doc solicitado está en la bd
        respuesta = False
        # print(datos[doc]['horario'])
        if  13 <= hora <=14 or 20 <= hora <= 21: #para los no beneficiarios, pueden reclamar luego de que acabe la jornada
            return True
        
        for i in datos[doc]['horario']: #recorriendo cada dia de la persona
            if dia == i[0] and datos[doc]['is_beneficiario']: #si el día actual está dentro del horario
                if (hora >= 11 and hora < 13 and i[1] == "mañana") or (hora >= 18 and hora < 20 and i[1] == "tarde"):
                    respuesta = True
                    break
                # else:
                #     print('Fuera de horario')
        return respuesta
    else:
        print('Documento de identidad inválido')
        return False

def validarEntrega(doc: str, hora: int):
    global datos
    datos = get_data() if datos != get_data() else datos
    fecha_actual = datetime.now()
    # hora = int(fecha_actual.strftime("%H"))
    # hora = 19

    match fecha_actual.strftime("%A"): #obtine el dia, pero en ingles
        case "Monday":
            return comprobar(doc,"lunes",hora)
        case "Tuesday":
            return comprobar(doc,"martes",hora)
        case "Wednesday":
            return comprobar(doc,"miercoles",hora)
        case "Thursday":
            return comprobar(doc,"jueves",hora)
        case "Friday":
            return comprobar(doc,"viernes",hora)
        case "Saturday":
            return comprobar(doc,"sabado",hora)


if __name__ == '__main__':
    # print(validarEntrega('1001022313'))
    print(validarEntrega('1001152975', 19))
