import flet as ft
import base64
import time

integrantes = {
   1: {
      "name": "Jaider Jhesit Lopez.",
      "age": 23,
      "email": "jaider_lopez82192@elpoli.edu.co",
      "career": "Ingeniería Informatica",
      "photo": r"imgs\user_picture.jpg"
   },
   2: {
      "name": "Kevin Alexander Flores.",
      "age": 21,
      "email": "kevin_florez82202@elpoli.edu.co",
      "career": "Ingeniería Informatica",
      "photo": r"imgs\user_picture.jpg"
   },
   3: {
      "name": "Jazmin Andrea Saenz.",
      "age": 22,
      "email": "jazmin_saenz82202@elpoli.edu.co",
      "career": "Ingeniería Informatica",
      "photo": r"imgs\user_picture.jpg"
   },
}

class About_project(ft.Container):
   # ---------------------------------------- FUNCIONES ----------------------------------------
   def fun_integrantes(self, container: ft.Container):
      global integrantes
      col = ft.Column(expand=1, alignment='center')
      try:
         for i in integrantes.keys():
            name = integrantes[i]['name']
            age = integrantes[i]['age']
            email = integrantes[i]['email']
            career = integrantes[i]['career']
            photo = integrantes[i]['photo']
            imagen = ft.Image(src_base64= base64.b64encode(open(photo, 'rb').read()).decode("utf-8"), )
            integrante = ft.Container(expand=1, bgcolor= "#d9d9d9", padding= 15, border_radius=10,
                                    content= ft.Row(controls=[
                                       ft.Container(border_radius=50, width= 100, height=100, bgcolor="#989393",
                                                    content= imagen),
                                       ft.VerticalDivider(1, color='transparent'),
                                       ft.Container(expand=1, border_radius=10,
                                                    content= ft.Column(controls=[
                                                       ft.Text(value=f"Nombre: {name}", bgcolor="#ffffff", color='black', weight='w800',),
                                                       ft.Text(value=f"Edad: {age}", bgcolor="#ffffff", color='black', weight='w800'),
                                                       ft.Text(value=f"Correo: {email}", bgcolor="#ffffff", color='black', weight='w800'),
                                                       ft.Text(value=f"Carrera: {career}", bgcolor="#ffffff", color='black', weight='w800'),
                                                    ]))
                                    ]))
            col.controls.append(integrante)

         return col
         
      except Exception as e:
         print(f"Error::::::::::: {e}")
         return None
      ...
   # ---------------------------------------- CONTROLES ----------------------------------------
   def __init__(self, page):
      super().__init__()
      self.page = page
      #           logo
      self.path_log = base64.b64encode(open(r"imgs\escudo_institucional.png", 'rb').read()).decode("utf-8")
      self.logo_poli = ft.Image(src_base64=self.path_log, height= 150, fit='cover')
      
      #           containers
      ## integrantes
      self.col_integrantes = ft.Column(expand=1, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                       controls=[ ft.Text(value="Integrantes del Projecto", size=16, weight='w900'),
                                                self.fun_integrantes(ft.Container)
                                       ])
      ## descripción
      self.descripcion1 = "El proyecto RefrigScan (RSSCRE) tiene como objetivo digitalizar y optimizar el proceso de entrega de refrigerios estudiantiles en la Regional Urabá del Politécnico Jaime Isaza Cadavid. Actualmente, el proceso es manual, lento, y genera largas filas, además de ser vulnerable a irregularidades en el orden de espera. "
      self.descripcion2 = "El sistema propuesto utiliza cámaras para escanear los carnets institucionales, verificando en una base de datos en tiempo real si el estudiante es beneficiario o no. También se implementará una cola virtual, donde los estudiantes serán llamados en orden, evitando filas físicas extensas y desordenadas. La información generada se almacenará en la nube para análisis de datos, permitiendo evaluar el uso del servicio, los días de mayor demanda, y el comportamiento de los beneficiarios."
      self.descripcion3 = "Este sistema reducirá tiempos de espera, mejorará la organización, y permitirá una gestión más eficiente del programa de refrigerios, beneficiando a estudiantes, personal encargado, y la administración."
      self.col_descripcion = ft.Container(content= ft.Column(expand=1, horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                                       controls=[ ft.Text(value="Descripción del Projecto", size=16, weight='w900'),
                                                 ft.Text(value= self.descripcion1, size=12,),
                                                 ft.Text(value= self.descripcion2, size=12,),
                                                 ft.Text(value= self.descripcion3, size=12,),
                                       ]), expand=1, bgcolor="#d9d9d9", border_radius=10, padding= 10,)
      ## footer
      self.footer = ft.Container(expand=True, padding= 10, #bgcolor="#535353",  #width= 800,
                                 content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True,
                                          controls=[ ft.Text("Centro Regional Urabá- Corregimiento El Reposo, Antioquia"), 
                                                      ft.Text("Código Postal: 057840 - Tel: 604 829 6856"), 
                                                      ft.Text("uraba@elpoli.edu.co"), 
                                                      ft.Text("© 2024") ]))

      self.container = ft.Container(
         expand= True,
         # width=900,
         # height=600,
         border_radius = 15,
         padding= ft.padding.only(10, 2, 10, 10),
         # gradient= ft.LinearGradient(['#639548', '#8fa767', "#ffac43"]),
         bgcolor= "#d2c3c3",
         content= ft.Column(expand=1, horizontal_alignment= 'center', #scroll=ft.ScrollMode.AUTO,  # Añadir scroll al contenido principal 
                             controls=[ft.Text("Acerca del Projecto", size=37, weight='w900', font_family="Consolas"), 
                                       ft.Row(expand=1, 
                                              controls=[ self.col_integrantes,
                                                 ft.VerticalDivider(5, color='transparent'),
                                                 self.col_descripcion,
                                              ]),
                                       ft.Divider(15, color="transparent"),])
      )

      self.content = ft.Container(padding= ft.padding.only(top= 50), bgcolor="#ffffff", height= 800,
                                  content= ft.Column(expand= True, horizontal_alignment= ft.CrossAxisAlignment.CENTER, 
                                  scroll= ft.ScrollMode.AUTO,  # Añadir scroll al contenido principal 
                                          controls=[self.logo_poli,
                                                   self.container,
                                                   self.footer],
                                          ))



def main(page: ft.Page):
   app = About_project(page,)

   # ---------------------------------------- GRAPHICS ----------------------------------------
   page.window.width = 1000
   page.window.height= 780
   page.window.min_width = 990
   page.window.min_height = 770
   page.window.max_width = 815
   page.window.max_height = 1010
   page.horizontal_alignment = 'center'

   page.add(app)

if __name__ == "__main__":
   ft.app(target= main)