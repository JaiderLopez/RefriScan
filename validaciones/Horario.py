import json
from datetime import datetime

def comprobar(id,dia,hora):
    with open('bd/horario.json', 'r') as file:
        datos = json.load(file)
        
        if id in datos: #si el id solicitado está en el horario
            respuesta = False
            for i in datos[id]: #recorriendo cada dia de la persona
                if dia in i: #si el corresponde
                    if (hora >= 11 and hora < 13 and i[1] == "mañana") or (hora >= 18 and hora < 20 and i[1] == "tarde"): 
                        respuesta = True
                        break
                    else:
                        print('Fuera de horario')
            return respuesta
        else:
            print('Documento de identidad inválido')
            return False

def validarEntrega(id):
    fecha_hora_actual = datetime.now()
    hora = int(fecha_hora_actual.strftime("%H"))

    match fecha_hora_actual.strftime("%A"):
        case "Monday":
            return comprobar(id,"lunes",hora)
        case "Tuesday":
            return comprobar(id,"martes",hora)
        case "Wednesday":
            return comprobar(id,"miercoles",hora)
        case "Thursday":
            return comprobar(id,"jueves",hora)
        case "Friday":
            return comprobar(id,"viernes",hora)
        case "Saturday":
            return comprobar(id,"sabado",hora)


"""
if __name__ == '__main__':
    print(validarEntrega('1193048051'))
""" 