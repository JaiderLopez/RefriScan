import flet as ft
import base64
import time

integrantes = {
   1: {
      "name": "Jaider Jhesit Lopez.",
      "age": 23,
      "email": "jaider_lopez82192@elpoli.edu.co",
      "career": "Ingeniería Informatica",
      "photo": r"imgs\lopezjhesit.png"
   },
   2: {
      "name": "Jazmin Andrea Saenz.",
      "age": 22,
      "email": "jazmin_saenz82202@elpoli.edu.co",
      "career": "Ingeniería Informatica",
      "photo": r"imgs\saenzjazmin.png"
   },
   3: {
      "name": "Kevin Alexander Flores.",
      "age": 21,
      "email": "kevin_florez82202@elpoli.edu.co",
      "career": "Ingeniería Informatica",
      "photo": r"imgs\floreskevin.png"
   },
}

class About_project(ft.Container):
      # ---------------------------------------- CONTROLES ----------------------------------------
   def __init__(self, page):
      super().__init__()
      self.page = page
      self.page.fonts = {
         'Roboto400': 'https://fonts.googleapis.com/css2?family=Eagle+Lake&family=Roboto&display=swap',
      }
      self.page.theme = ft.Theme(font_family= 'Roboto400')
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
      self.descripcion1 = "El proyecto RefrigScan (RSSCRE) tiene como objetivo digitalizar y optimizar el proceso de entrega de refrigerios estudiantiles en la Regional Urabá del Politécnico Jaime Isaza Cadavid. Actualmente, el proceso es manual, lento, y genera largas filas."
      self.descripcion2 = "El sistema propuesto utiliza una cámara para escanear los documentos de los estudiantes, verificando en una base de datos en tiempo real si el estudiante es beneficiario o no. La información generada se almacenará para análisis de datos y generación de reportes, permitiendo evaluar el uso del servicio, los días de mayor demanda, y el comportamiento de los beneficiarios."
      self.descripcion3 = "Se espera que el uso del sistema reduzca los tiempos de espera, mejorare la organización, y permitirá una gestión más eficiente del programa de refrigerios, beneficiando a estudiantes, personal encargado, y la administración."
      self.col_descripcion = ft.Container( expand=1, 
                                          content= ft.Column(expand=1, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                   controls=[ ft.Text(value="Descripción del Projecto", size=16, weight='w900'),
                                                         ft.Container(expand=1, bgcolor="#d9d9d9", border_radius=10, padding= 10,
                                                            content= ft.Column(controls=[
                                                                        ft.Text(value= self.descripcion1, size=14,),
                                                                        ft.Text(value= self.descripcion2, size=14,),
                                                                        ft.Text(value= self.descripcion3, size=14,),
                                                                     ])
                                                         ),
                                                 
                                                   ]),
                              )
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
         bgcolor= "#ffffff",
         content= ft.Column(expand=1, horizontal_alignment= 'center', #scroll=ft.ScrollMode.AUTO,  # Añadir scroll al contenido principal 
                             controls=[ft.Text("Acerca del Projecto", size=37, weight='bold', ),#font_family="san-serif"), 
                                       ft.Divider(height= 3, color= '#d9d9d9'),
                                       ft.Row(expand=1, 
                                              controls=[ self.col_integrantes,
                                                 ft.VerticalDivider(5, color='transparent'),
                                                 self.col_descripcion,
                                              ]),
                                       ft.Divider(15, color="transparent"),])
      )

      self.content = ft.Container(padding= ft.padding.only(top= 15), bgcolor="#ffffff", height= 800,
                                  content= ft.Column(expand= True, horizontal_alignment= ft.CrossAxisAlignment.CENTER, 
                                  scroll= ft.ScrollMode.AUTO,  # Añadir scroll al contenido principal 
                                          controls=[self.logo_poli,
                                                   self.container,
                                                   self.footer],
                                          ))

   # ---------------------------------------- FUNCIONES ----------------------------------------
   def fun_integrantes(self, container: ft.Container):
      global integrantes
      col = ft.Column(expand=1, horizontal_alignment= ft.CrossAxisAlignment.CENTER)
      try:
         for i in integrantes.keys():
            name = integrantes[i]['name']
            age = integrantes[i]['age']
            email = integrantes[i]['email']
            career = integrantes[i]['career']
            photo = integrantes[i]['photo']
            imagen = ft.Image(src_base64= base64.b64encode(open(photo, 'rb').read()).decode("utf-8"), scale= 1)
            integrante = ft.Container(expand=1, bgcolor= "#d9d9d9", padding= 10, border_radius=10,
                                    content= ft.Row(
                                          controls=[
                                             ft.Container(border_radius=50, width= 100, height=100, bgcolor="#989393",
                                                         content= imagen),
                                             # ft.VerticalDivider(1, color='transparent'),
                                             ft.Container(expand=1, border_radius=10, bgcolor="#ffffff", padding=  5,
                                                         content= ft.Column(controls=[
                                                         ft.Row([ft.Text(value=f"Nombre:", weight='w800',), ft.Text(value=f"{name}",),]),
                                                         ft.Row([ft.Text(value=f"Edad:", weight='w800'), ft.Text(value=f"{age}",),]),
                                                         ft.Row([ft.Text(value=f"Correo:", weight='w800'), ft.Text(value=f"{email}",),]),
                                                         ft.Row([ft.Text(value=f"Carrera:", weight='w800'), ft.Text(value=f"{career}",),]),
                                                                  ], spacing= 0)
                                             )
                                             ])
                        )
            col.controls.append(integrante)

         return col
         
      except Exception as e:
         print(f"Error::::::::::: {e}")
         return None
      ...

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