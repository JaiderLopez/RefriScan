import json
credenciales = {
   "1001152975": {"password": "1001.pswd", 
                  "type": 	"admin",
                  "is_activate": True },
   "1040358267": {"password": "1040.pswd", 
                  "type": 	"admin",
                  "is_activate": True },

}

with open(r"bd\credenciales.json", 'w') as file:
   json.dump(credenciales, file, indent=4)

# with open(r"bd\\horario_estudiantes.json", 'w') as file:
#    json.dump(data_, file, indent=4)