import json

# ADD KEY: "faltas" AL JSON DE HORARIO Y RENOMBRARLO COMO HORARIO_ESTUDIANTES
with open("bd\\horario_estudiantes.json", 'r') as file:
   data = json.load(file)

data_ = data.copy()
keys = data_.keys()

for key in keys:
   data_[key]['is_beneficiario'] = True


with open("bd\\horario_estudiantes.json", 'w') as file:
   json.dump(data_, file, indent=4)



# with open(r"bd\horario_estudiantes.json", 'r') as file:
#    data = json.load(file)

# # print(json.dumps(data, indent=3))
# var = "1001022313"
# print(data[var]['horario'])