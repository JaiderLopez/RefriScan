import json
from datetime import datetime, time

# def registro(index:int, date: str, time: str, doc: str, horario: str, is_beneficiario: bool):
#    modelo = {
#       index: {
#          "fecha": date,
#          "hora": time,
#          "documento": doc,
#          "horario": horario,
#          "is_beneficiario": is_beneficiario
#       }
#    }
#    return modelo[index]

# reclamos = {}

# for i in range(1, 10):
#    reclamos[i] = registro(i, "2024-11-18", "15:42", "1001152975", 'tarde', True)

# fecha = datetime.now()
# dia = fecha.strftime("%A")
# hora = fecha.hour
# minutos = fecha.minute

# print("fecha", dia, "hora: ", hora, "minutos: ", minutos)

reclamos = [1, 2, 3, 4, 5, 6]

if 44 not in reclamos:
   print("ldsf")