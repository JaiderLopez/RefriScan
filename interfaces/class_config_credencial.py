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
      self.page.fonts = {
         'Roboto400': 'https://fonts.googleapis.com/css2?family=Eagle+Lake&family=Roboto&display=swap',
      }
      self.page.theme = ft.Theme(font_family= 'Roboto400')

      self.users: dict = data_get()

      self.dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Por favor, Confirme"),
        content=ft.Text("¿Quiere eliminar este usuario?"),
        actions=[
            ft.TextButton("Yes", on_click=self.delete_user),
            ft.TextButton("No", on_click=self.close_dlg),
         ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
      )

      self.table_user = ft.DataTable(columns= [
                                        ft.DataColumn(ft.Text("ID USUARIO")),
                                        ft.DataColumn(ft.Text("NOMBRE")),
                                        ft.DataColumn(ft.Text("    ACCIONES")),
                                     ],
                                     border= ft.border.all(1),
                                     border_radius= 15,
                                     width= self.page.window.width * 0.88,
                                     heading_text_style= ft.TextStyle(size= 16, weight= 'bold', letter_spacing= 5)
                                     )

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
      self.cancel_button = ft.ElevatedButton(text="Cancelar", bgcolor= "#e53935", color= 'white', on_click= self.cancel_save_profile, visible=False)

      # action view
      self.add_user_button = ft.ElevatedButton(text="Agregar Usuario Nuevo", bgcolor= "#009852", color= 'white', on_click=self.show_fields)
      self.error_message = ft.Text("¡Por favor, llena todos los campos!", color="red", visible=False)
      self.user_list = ft.Column(expand= True ,scroll= ft.ScrollMode.AUTO, horizontal_alignment= ft.CrossAxisAlignment.START,
                                 controls= [self.table_user])

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
                                 ft.Row([self.cancel_button, self.save_button], alignment= 'center'),
                                 self.error_message,
                                 ft.Text("Usuarios en el sistema:", size=20),
                                 ft.Container(content= self.user_list, bgcolor= 'transparent', border_radius=15, height= 350, padding= 25),
                                 ft.ElevatedButton(text="GUARDAR CAMBIOS", bgcolor= "#009852", color= 'white', on_click= self.save_changes),
                              ],
                              )
                     )
      

   # ---------------------------------------- FUNCIONES ----------------------------------------
   def reload_inputs(self,): #reload inputs
      self.username_input.value = ""
      self.nameprofile_input.value = ""
      self.password_input.value = ""
      self.type_dropdown.value = None
      
   def hint_imputs(self,): #hint inputs
      self.add_user_button.visible = True
      self.username_input.visible = False
      self.nameprofile_input.visible = False
      self.cancel_button.visible = False
      self.password_input.visible = False
      self.type_dropdown.visible = False
      self.save_button.visible = False
      self.error_message.visible = False

   def show_fields(self, e): #show inputs when click new user
      self.add_user_button.visible = False
      self.username_input.visible = True
      self.nameprofile_input.visible = True
      self.password_input.visible = True
      self.type_dropdown.visible = True
      self.save_button.visible = True
      self.cancel_button.visible = True
      self.error_message.visible = False
      self.page.update()

   def user_existed(self,): #message when user is already exist
      snackbar = ft.SnackBar(ft.Text(f"Id usuario ya existe"))
      self.page.overlay.append(snackbar)
      snackbar.open = True
      self.page.update()

   def cancel_save_profile(self, e): #action when click cancel to add new user
      self.reload_inputs()
      self.hint_imputs()
      self.page.update()

   def save_profile(self, e): #action when click to save new user
      username = self.username_input.value
      nameprofile = self.nameprofile_input.value
      password = self.password_input.value
      user_type = self.type_dropdown.value
      if username in self.users:
         # print("User existente")
         self.user_existed()
         return None
      if username and password and user_type:
         self.users[username] = {"password": password, "type": user_type, "name": nameprofile}
         self.reload_inputs()
         self.hint_imputs()
         self.update_user_list()
      else:
         self.error_message.visible = True
      self.table_user.disabled = False
      self.page.update()

   def close_dlg(self, e): #close windown delete user containt
      self.dlg_modal.open = False
      self.page.update()

   def open_dlg_modal(self, e, username): #open windown delete user containt
      self.dlg_modal.data = username
      self.page.overlay.append(self.dlg_modal)
      self.dlg_modal.data = username
      self.dlg_modal.open = True
      self.page.update()

   def delete_user(self, e): #method to delete an user credentials
      username = self.dlg_modal.data
      del self.users[username]
      self.close_dlg(None)
      self.update_user_list()

   def update_user_list(self): #update view of all users credentials in the system
      rows = []
      for username in self.users.keys():
         data = ft.DataRow([])
         data.cells.append(ft.DataCell(ft.Text(username, color= 'black')))
         data.cells.append(ft.DataCell(ft.Text(self.users[username]['name'])))
         data.cells.append(ft.DataCell(ft.Row(
                  [
                     ft.ElevatedButton(text="Editar", color= 'black', bgcolor= "#81c784", on_click=lambda e, u=username: self.edit_user(u)),
                     ft.ElevatedButton(text="Eliminar", color= 'black', bgcolor= "#ef5350", on_click=lambda e, u=username: self.open_dlg_modal(e, u)),
                  ]
               )))
         rows.append(data)
      self.table_user.rows = rows
      self.page.update()

   def edit_user(self, username): #to edit user credencial with the same inputs to create one
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
      self.table_user.disabled = True
      
      del self.users[username]
      self.page.update()
   
   def save_changes(self, e): #saves the credentials user for the system
      try:
         print(self.users)
         data_set(self.users)
         snackbar = ft.SnackBar(ft.Text(f"Datos Guardados Correctamente"))
         self.page.overlay.append(snackbar)
         snackbar.open = True
         self.page.update()
      except Exception as ee:
         print(f"Error::::::::::::: {ee}")
      

def main(page: ft.Page):
   # ---------------------------------------- GRAPHICS ----------------------------------------
   manager = UserManagerApp(page)
   page.title = "Gestión de Perfiles de Usuario" #title window view


   page.add(manager)
if __name__ == "__main__":
   ft.app(target=main)
