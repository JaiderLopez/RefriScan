import flet as ft
import json

def data_get():
   with open("bd\\credenciales.json", 'r') as file:
      data_ = json.load(file)
   return data_

#update data students(json)
def data_set(data: dict):
   with open("bd\\credenciales.json", 'w') as file:
      json.dump(data, file, indent=4)

class UserManagerApp(ft.Container):
   def __init__(self, page):
      super().__init__()
   # ---------------------------------------- CONTROLES ----------------------------------------
      self.page = page
      self.users: dict = data_get()
      ## form user add
      self.username_input = ft.TextField(label="ID Usuario", visible=False, prefix_icon= ft.icons.LOGIN)
      self.password_input = ft.TextField(label="Contraseña", password=True, visible=False, can_reveal_password=True, prefix_icon= ft.icons.PASSWORD)
      self.nameprofile_input = ft.TextField(label="Nombre de Usuario", visible=False, prefix_icon= ft.cupertino_icons.PROFILE_CIRCLED)
      self.type_dropdown = ft.Dropdown(
            label="Tipo de Usuario",
            prefix_icon= ft.cupertino_icons.PERSON_3_FILL,
            options=[
                ft.dropdown.Option("admin"), 
                ft.dropdown.Option("user")],
            visible=False
        )
      self.save_button = ft.ElevatedButton(text="Guardar Perfil", bgcolor= "#009852", color= 'white', on_click= self.save_profile, visible=False)

      # action view
      self.add_user_button = ft.ElevatedButton(text="Agregar Usuario Nuevo", bgcolor= "#009852", color= 'white', on_click=self.show_fields)
      self.error_message = ft.Text("¡Por favor, llena todos los campos!", color="red", visible=False)
      self.user_list = ft.Column( scroll= ft.ScrollMode.AUTO, horizontal_alignment= ft.CrossAxisAlignment.START,
                                 controls= [ft.Text("halo moto")])

      self.update_user_list()
      ## content main of this view
      self.content = ft.Container(expand= True, alignment= ft.alignment.center,
                     content= ft.Column( expand= True, horizontal_alignment= ft.CrossAxisAlignment.CENTER, spacing=20,
                              controls= [
                                 ft.Text("Gestión de Perfiles de Usuario", size=30, weight="bold"),
                                 self.add_user_button,
                                 ft.Row(expand= True, alignment= "center"
                                    ,controls=[self.username_input,
                                    self.password_input,]),
                                 ft.Row(expand= True, alignment= "center"
                                    ,controls=[self.nameprofile_input,
                                    self.type_dropdown]),
                                 self.save_button,
                                 self.error_message,
                                 ft.Text("Usuarios en el sistema:", size=20),
                                 ft.Container(content= self.user_list, bgcolor= 'transparent', border_radius=15, height= 350, padding= 25),
                                 ft.ElevatedButton(text="GUARDAR CAMBIOS", bgcolor= "#009852", color= 'white', on_click= self.save_changes),
                              ],
                              )
                     )
      

   # ---------------------------------------- FUNCIONES ----------------------------------------
   def show_fields(self, e):
      self.add_user_button.visible = False
      self.username_input.visible = True
      self.nameprofile_input.visible = True
      self.password_input.visible = True
      self.type_dropdown.visible = True
      self.save_button.visible = True
      self.error_message.visible = False
      self.page.update()

   def save_profile(self, e):
      username = self.username_input.value
      nameprofile = self.nameprofile_input.value
      password = self.password_input.value
      user_type = self.type_dropdown.value
      if username and password and user_type:
         self.users[username] = {"password": password, "type": user_type, "name": nameprofile}
         self.username_input.value = ""
         self.nameprofile_input.value = ""
         self.password_input.value = ""
         self.type_dropdown.value = None
         self.add_user_button.visible = True
         self.username_input.visible = False
         self.nameprofile_input.visible = False
         self.password_input.visible = False
         self.type_dropdown.visible = False
         self.save_button.visible = False
         self.update_user_list()
      else:
         self.error_message.visible = True
      self.page.update()

   def delete_user(self, username):
      del self.users[username]
      self.update_user_list()

   def update_user_list(self):
      self.user_list.controls.clear()
      for username in self.users.keys():
         self.user_list.controls.append(
               ft.Row(
                  [
                     ft.Text(username),
                     ft.ElevatedButton(text="Editar", on_click=lambda e, u=username: self.edit_user(u)),
                     ft.ElevatedButton(text="Eliminar", on_click=lambda e, u=username: self.delete_user(u))
                  ]
               )
         )
      self.page.update()

   def edit_user(self, username):
      user = self.users[username]
      self.username_input.value = username
      self.nameprofile_input.value = user["name"]
      self.password_input.value = user["password"]
      self.type_dropdown.value = user["type"]
      self.username_input.visible = True
      self.nameprofile_input.visible = True
      self.password_input.visible = True
      self.type_dropdown.visible = True
      self.save_button.visible = True
      self.add_user_button.visible = False
      del self.users[username]
      self.page.update()
   
   def save_changes(self, e):
      print(self.users)
      data_set(self.users)
      

def main(page: ft.Page):
   # ---------------------------------------- GRAPHICS ----------------------------------------
   manager = UserManagerApp(page)
   page.title = "Gestión de Perfiles de Usuario" #title window view


   page.add(manager)
if __name__ == "__main__":
   ft.app(target=main)
