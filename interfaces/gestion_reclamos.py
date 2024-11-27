import json
from datetime import datetime
#clase para gestionar el registro de los estudiantes que van reclamando su refrigerio
class Reclamos:
   def __init__(self,):
      # super.__init__()
      self.reclamos: dict = self.get_reclamos_dia()
      self.documentos: list = self.get_documentos()
      self.contador: int = len(self.documentos)+ 1 if len(self.documentos) != 0 else 1
      # self.fecha_dia = None
      self.horario = None

   def get_reclamos_dia(self):
      with open("bd\\reclamos_dia.json", 'r') as file:
         data = json.load(file)
      # array = list(data.keys())
      # self.documetos = array
      return data
   
   def get_documentos(self,):
      keys = list(self.reclamos.keys())
      array = []
      if keys == []:
         return array
      
      for key in keys:
         array.append(self.reclamos[key]['documento'])
      
      return array

   def modelo_registro(self, index:int, date: str, time: str, doc: str, horario: str, is_beneficiario: bool):
      modelo = {
         index: {
            "fecha": date,
            "hora": time,
            "documento": doc,
            "horario": horario,
            "is_beneficiario": is_beneficiario
         }
      }
      return modelo[index]
   def set_reclamos_dia(self,):
      with open("bd\\reclamos_dia.json", 'w') as file:
         json.dump(self.reclamos, file, indent=4)

   def registro(self, date, time, minutos, doc, is_beneficiario):
      if  11 <= time <14:
         horario = "mañana"
      elif 18 <= time < 21:
         horario = "tarde"
      else:
         horario = "mañana" if time < 15 else "tarde"
      if self.horario == None:
         self.horario = horario
      if minutos < 10:
         minutos = "0" + str(minutos)

      hora = ''.join([str(time), ':',str(minutos)])
      
      self.reclamos[self.contador] = self.modelo_registro(self.contador, date, hora, doc, horario, is_beneficiario)
      self.documentos.append(doc)
      self.contador += 1
      self.set_reclamos_dia()
   
   def get_analitica(self,):
      with open("bd\\analitica.json", 'r') as file:
         analitica = json.load(file)
      return analitica
   
   def get_day(self):
      fecha_actual = datetime.now()
      match fecha_actual.strftime("%A"): #obtine el dia, pero en ingles
         case "Monday":
            return "lunes"
         case "Tuesday":
            return "martes"
         case "Wednesday":
            return "miercoles"
         case "Thursday":
            return "jueves"
         case "Friday":
            return "viernes"
         case "Saturday":
            return "sabado"
   def add_faltas(self,):
      dia = self.get_day()
      print(dia)
      print(self.horario)
      with open("bd\\horario_estudiantes.json", 'r') as file:
         estudiantes = json.load(file)
      # estudiantes_evaluar = []
      for key in estudiantes.keys():
         for i in estudiantes[key]['horario']:
            if i[0] == dia and i[1] == self.horario:
               if key not in self.documentos:
                  estudiantes[key]['faltas']+= 1
               break
      with open("bd\\horario_estudiantes.json", 'w') as file:
         json.dump(estudiantes, file, indent=4)


   def terminar_jornada(self,):
      try:
         analitica = self.get_analitica()
         index = len(list(analitica.keys()))+ 1 if len(list(analitica.keys())) != 0 else 1
         
         # añadir el json reclamos_dia al json analitica
         analitica[index] = self.reclamos
         with open("bd\\analitica.json", 'w') as file:
            json.dump(analitica, file, indent= 4)
         
         # añadir las faltas a los estudiantes que debían reclamar y no lo hicieron
         self.add_faltas()
         
         # limpiar json de reclamos_dia
         self.reclamos = {}
         self.documentos = []
         self.set_reclamos_dia()
      except Exception as e:
         print(f"Error: {e}")