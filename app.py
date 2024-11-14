import flet as ft
from cv2 import VideoCapture
from interfaces.class_scan import ScanDoc
from interfaces.class_login import Login
from interfaces.class_about import About_project
from interfaces.class_table_estudent import TableEstudent
from interfaces.class_config_credencial import UserManagerApp, data_get
import threading
import time

class AppMain(ft.Container):
   # ---------------------------------------- CONTROLES ----------------------------------------
   def __init__(self, page: ft.Page):
      super().__init__()
      self.page = page
      self.container_scan = ScanDoc(self.page)
      ##user data
      self.user = None
      self.user_name = None
      self.user_type = None
      self.container_login = Login(self, self.page,)
      self.container_about = About_project(self.page)
      self.container_table = TableEstudent(self.page)
      self.container_config = UserManagerApp(self.page)
      ...
      #           nav_rail
      ## nav_user
      self.nav_rail_user = ft.NavigationRail(
         selected_index= 0,
         label_type= ft.NavigationRailLabelType.ALL,
         min_width= 100,
         min_extended_width= 115,
         group_alignment= -1,
         destinations=[
               ft.NavigationRailDestination(
                  icon= ft.icons.CARD_TRAVEL_OUTLINED,
                  selected_icon= ft.icons.CARD_TRAVEL_ROUNDED,
                  label="Data Project",
               ),
               ft.NavigationRailDestination(
                  icon= ft.icons.DOCUMENT_SCANNER_OUTLINED,
                  selected_icon= ft.icons.DOCUMENT_SCANNER,
                  label="Scan",
               ),
               ft.NavigationRailDestination(
                  icon_content= ft.Icon(name= ft.icons.OUTBOX, color='red'),
                  # selected_icon= ft.icons.OUTBOX_OUTLINED,
                  label="Salir",
               ),
         ],
         on_change=self.change_content_user,
      )
      ##admin
      self.nav_rail_admin = ft.NavigationRail(
         selected_index= 0,
         label_type= ft.NavigationRailLabelType.ALL,
         min_width= 100,
         min_extended_width= 115,
         group_alignment= -1,
         destinations=[
               ft.NavigationRailDestination(
                  icon= ft.icons.CARD_TRAVEL_OUTLINED,
                  selected_icon= ft.icons.CARD_TRAVEL_ROUNDED,
                  label="Data Project",
               ),
               ft.NavigationRailDestination(
                  icon= ft.icons.DOCUMENT_SCANNER_OUTLINED,
                  selected_icon= ft.icons.DOCUMENT_SCANNER,
                  label="Scan",
               ),
               ft.NavigationRailDestination(
                  icon= ft.icons.TABLE_ROWS_OUTLINED,
                  selected_icon= ft.icons.TABLE_ROWS,
                  label="Data Students",
                  # disabled= True,
               ),
               ft.NavigationRailDestination(
                  icon= ft.icons.TABLE_CHART_OUTLINED,
                  selected_icon= ft.icons.TABLE_CHART,
                  label="Analitycs",
                  # disabled= True,
               ),
               ft.NavigationRailDestination(
                  icon= ft.cupertino_icons.GEAR_ALT,
                  selected_icon= ft.cupertino_icons.GEAR_ALT_FILL,
                  label= "Configuración",
               ),
               ft.NavigationRailDestination(
                  # icon= ft.icons.OUTBOX,
                  icon_content= ft.Icon(name= ft.icons.OUTBOX, color='red'),
                  # selected_icon= ft.icons.OUTBOX_OUTLINED,
                  label="Salir",
               ),
         ],
         on_change=self.change_content_admin,
      )
      ## login
      self.nav_rail_login = ft.NavigationRail(
         selected_index= 0,
         label_type= ft.NavigationRailLabelType.ALL,
         min_width= 100,
         min_extended_width= 115,
         group_alignment= -1,
         destinations=[
               ft.NavigationRailDestination(
                  icon= ft.icons.CARD_TRAVEL_OUTLINED,
                  selected_icon= ft.icons.CARD_TRAVEL_ROUNDED,
                  label="Data Project",
               ),
               ft.NavigationRailDestination(
                  # icon= ft.icons.OUTBOX,
                  icon_content= ft.Icon(name= ft.icons.OUTBOX, color='red'),
                  # selected_icon= ft.icons.OUTBOX_OUTLINED,
                  label="Salir",
               ),
         ],
         on_change=self.change_content_login,
      )
      ## nav_rail
      self.nav_rail = ft.Container(content= self.nav_rail_login)
      ...

      ##nav_profile
      self.name_profile = ft.Text(value="", color="#107800")
      self.btn_login = ft.ElevatedButton(text="Log in", on_click=self.fun_gologout, icon=ft.cupertino_icons.PERSON_2_FILL, icon_color="#107800", bgcolor='transparet', color="#107800")
      # self.btn_logout = ft.ElevatedButton(text="Log out", on_click=self.fun_gologout, icon=ft.cupertino_icons.PERSON_2_FILL, icon_color="#107800", bgcolor='transparet', color="#107800")
      self.btn_log = self.btn_login
      self.icon_profile = ft.Container(content= self.btn_log,)
      self.nav_profile = ft.Row(alignment='end', height=30,
                                controls=[self.name_profile, self.icon_profile])

      #           containers
      self.cont_main = ft.Container(
         expand=True,
         alignment=ft.alignment.center,
         padding=5,
         content= self.container_login.content,
         # content= ft.Row(expand= True, auto_scroll=True,
         #                 controls=[ft.Text("Que quieres hacer???", size=30, color= ft.colors.ORANGE)])
      )
      ...
      #           rows
      self.row_main = ft.Row(
         expand=True,
         vertical_alignment= ft.MainAxisAlignment.CENTER,
         auto_scroll=True,
         alignment=ft.MainAxisAlignment.START,
         # controls=[self.nav_rail, ft.VerticalDivider(1,), self.cont_main],
         controls=[self.nav_rail, ft.VerticalDivider(1,), ft.Column(expand=True,
                                                                    controls=[self.nav_profile, self.cont_main])],
      )


   # ---------------------------------------- FUNCIONES ----------------------------------------
   def change_content_admin(self, e): #cambiar el contenido desde el nav-vertical
      data = int(e.data)
      if data == 0: #about
         self.cont_main.content = self.container_about.content
         self.container_scan.threading_isrunning = False
         try:
            self.container_scan.capture.release()
         except Exception as e:
            print(f"Error::::::::::::: {e}")

      elif data == 1: #scan
         # self.cont_main.content = ft.Text("Scan Containt", size=30, color= ft.colors.RED_700)
         self.container_scan.capture = VideoCapture(0)
         self.container_scan.threading_isrunning = True
         self.container_scan.threading = threading.Thread(target=self.container_scan.fun_update_frame_camera)
         self.container_scan.threading.start()
         self.cont_main.content = self.container_scan.content

      elif data == 2: #table
         # self.cont_main.content = ft.Text("Table Students Containt", size=30, color= ft.colors.RED_700)
         self.cont_main.content = self.container_table.content
         self.container_scan.threading_isrunning = False
         try:
            self.container_scan.capture.release()
         except Exception as e:
            print(f"Error::::::::::::: {e}")

      elif data == 3: #analitycs
         self.cont_main.content = ft.Text("Analitycs Containt", size=30, color= ft.colors.RED_700)
         self.container_scan.threading_isrunning = False
         try:
            self.container_scan.capture.release()
         except Exception as e:
            print(f"Error::::::::::::: {e}")

      elif data == 4: #credenciales
         self.container_scan.threading_isrunning = False
         self.cont_main.content = self.container_config.content
         try:
            self.container_scan.capture.release()
         except Exception as e:
            print(f"Error::::::::::::: {e}")

      elif data == 5: #salir
         self.container_scan.threading_isrunning = False
         try:
            self.container_scan.capture.release()
            self.container_scan.threading_txt.join()
         except Exception as e:
            print(f"Error al unir hilos: {e}")
         self.page.window.destroy()
      else:
         self.cont_main.alignment = ft.alignment.center
         self.cont_main.content = ft.Text("Proximamente ...", size=30, color=ft.colors.ORANGE)
      self.cont_main.update()
   ...

   def change_content_user(self, e): #cambiar el contenido desde el nav-vertical
      data = int(e.data)
      if data == 0:
         print(self.user)
         print(self.user_name)
         print(self.user_type)
         self.cont_main.content = self.container_about.content
         self.container_scan.threading_isrunning = False
         try:
            self.container_scan.capture.release()
         except Exception as e:
            print(f"Error::::::::::::: {e}")

      elif data == 1:
         # self.cont_main.content = ft.Text("Scan Containt", size=30, color= ft.colors.RED_700)
         self.container_scan.capture = VideoCapture(0)
         self.container_scan.threading_isrunning = True
         self.container_scan.threading = threading.Thread(target=self.container_scan.fun_update_frame_camera)
         self.container_scan.threading.start()
         self.cont_main.content = self.container_scan.content
      elif data == 2:
         self.container_scan.threading_isrunning = False
         try:
            self.container_scan.capture.release()
            self.container_scan.threading_txt.join()
         except Exception as e:
            print(f"Error al unir hilos: {e}")
         self.page.window.destroy()
      else:
         self.cont_main.alignment = ft.alignment.center
         self.cont_main.content = ft.Text("Proximamente ...", size=30, color=ft.colors.ORANGE)
      self.cont_main.update()
   ...

   def change_content_login(self, e): #cambiar el contenido desde el nav-vertical
      data = int(e.data)
      if data == 0:
         print(self.user)
         print(self.user_name)
         print(self.user_type)
         self.cont_main.content = self.container_about.content
         self.container_scan.threading = False
         try:
            self.container_scan.capture.release()
         except Exception as e:
            print(f"Error::::::::::::: {e}")
      elif data == 1:
         self.container_scan.threading_isrunning = False
         try:
            self.container_scan.capture.release()
            self.container_scan.threading_txt.join()
         except Exception as e:
            print(f"Error al unir hilos: {e}")
         self.page.window.destroy()
      else:
         self.cont_main.alignment = ft.alignment.center
         self.cont_main.content = ft.Text("Proximamente ...", size=30, color=ft.colors.ORANGE)
      self.cont_main.update()
   ...

   def fun_gologout(self, e):
      self.name_profile.value = ""
      self.container_login.credenciales = data_get()
      if self.btn_login.text == "Log out":
         self.btn_login.text = "Log in" 
      self.cont_main.content = self.container_login.content
      self.nav_rail.content = self.nav_rail_login
      self.container_scan.threading = False
      try:
         self.container_scan.capture.release()
      except Exception as e:
         print(f"Error::::::::::::: {e}")
      time.sleep(.5)
      self.page.update()

   def build(self):
   #           controles generales
      self.page.title = "APP - REFRISCAN"
      self.page.window.min_width = 1040
      self.page.window.min_height = 800
      self.page.window.width = 1050
      self.page.window.height = 810
      self.page.window.prevent_close = True
   # ---------------------------------------- GRAPHICS ----------------------------------------
      self.page.add(self.row_main)
      # self.page.add(self.nav_profile)
   ...

def main(page: ft.Page):
   app = AppMain(page)
   app.build()

if __name__ == "__main__":
   ft.app(target=main,)