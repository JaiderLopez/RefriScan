import flet as ft
import base64
import json
import time

def data_get():
   with open("bd\\credenciales.json", 'r') as file:
      credenciales = json.load(file)
   return credenciales

class Login(ft.Container):
   # ---------------------------------------- CONTROLES ----------------------------------------
   def __init__(self, app_main, page):
      super().__init__()
      self.page = page
      self.app_main = app_main
      self.page.fonts = {
         'Roboto400': 'https://fonts.googleapis.com/css2?family=Eagle+Lake&family=Roboto&display=swap',
         'Roboto500': 'https://fonts.googleapis.com/css2?family=Eagle+Lake&family=Roboto:ital,wght@1,500&display=swap'

      }
      self.page.theme = ft.Theme(font_family= 'Roboto500')
      self.credenciales = data_get()
      #           logo
      self.path_log = base64.b64encode(open(r"imgs\escudo_institucional.png", 'rb').read()).decode("utf-8")
      self.logo_poli = ft.Image(src_base64=self.path_log, height= 300)
      #           labels
      self.lb_usuario = ft.TextField(border=10, width=277, label="Usuario:", text_align='center')
      self.lb_password = ft.TextField(password=True, can_reveal_password=True, border=10, width=277, label="Contraseña:", text_align='center')
      self.txt_message = ft.Text(value="", color='white', weight= 'w100')
      #           buttons
      self.btn_login = ft.ElevatedButton(text="Iniciar Sesión", on_click=self.fun_validar_usuario)
      
      #           containers
      self.container = ft.Container(
         # expand= True,
         width=400,
         height=600,
         border_radius = 15,
         padding= ft.padding.only(10, 2, 10, 15),
         gradient= ft.LinearGradient(['#639548', '#8fa767', "#ffac43"]),
         content= ft.Column(expand=1, horizontal_alignment= 'center', 
                             controls=[self.logo_poli, self.lb_usuario, self.lb_password,
                                       self.txt_message,
                                       ft.Divider(15, color="transparent"),
                                       self.btn_login])
      )

      self.content = ft.Container(padding= ft.padding.only(top= 10),
                                  content=ft.Column(expand= True, horizontal_alignment= ft.CrossAxisAlignment.CENTER, spacing= 5,
                                          controls=[ft.Text("Login to RefriScan", size=30, weight='w900', font_family= 'san-serif', color= 'black', italic= True), 
                                                   self.container],
                                          ))
   ...
   # ---------------------------------------- FUNCIONES ----------------------------------------
   def fun_validar_usuario(self, e):
      print("validando...")
      usuario = self.lb_usuario.value
      contraseña = self.lb_password.value
      if usuario in self.credenciales:
         if self.credenciales[usuario]['password'] == contraseña:
            # self.page.clean()
            # self.page.add(ft.Text(f"Welcome: {usuario}"))
            # print(self.credenciales[usuario]["type"])
            name = self.credenciales[usuario]["name"]
            typee = self.credenciales[usuario]["type"]
            try:
               self.app_main.user = usuario
               self.app_main.user_name = name
               self.app_main.user_type = typee
               if typee == "user":
                  time.sleep(1.2)
                  self.app_main.nav_rail.content = self.app_main.nav_rail_user
                  self.app_main.cont_main.content = self.app_main.container_about.content
                  self.app_main.name_profile.value = name
                  self.app_main.btn_login.text = "Log out"
                  print(usuario, name, typee)
                  self.lb_usuario.value = ""
                  self.lb_password.value = ""
                  self.page.update()
               elif typee == "admin":
                  time.sleep(1.1)
                  self.app_main.nav_rail.content = self.app_main.nav_rail_admin
                  self.app_main.cont_main.content = self.app_main.container_about.content
                  self.app_main.name_profile.value = name
                  self.app_main.btn_login.text = "Log out"
                  print(usuario, name, typee)
                  self.lb_usuario.value = ""
                  self.lb_password.value = ""
                  self.page.update()
               
               # self.app_main.nav_rail.update()
            except Exception as e:
               print(f"Error:::::::::::::::::: {e}")
         
         else:
            self.txt_message.value = "Contraseña Invalida"
            self.txt_message.update()
            time.sleep(2)
            self.txt_message.value = ""
            self.txt_message.update()
      else:
         self.txt_message.value = "Usario no encontrado"
         self.txt_message.update()
         time.sleep(2)
         self.txt_message.value = ""
         self.txt_message.update()
                  
      # self.app_main.icon_profile.update()
      self.page.update()
   ...

def main(page: ft.Page):
   app = Login(None, page,)

   # ---------------------------------------- GRAPHICS ----------------------------------------
   page.window.width = 510
   page.window.height= 780
   page.window.min_width = 500
   page.window.min_height = 770
   page.window.max_width = 515
   page.window.max_height = 788
   page.horizontal_alignment = 'center'

   page.add(app)

if __name__ == "__main__":
   ft.app(target= main)