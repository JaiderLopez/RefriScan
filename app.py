import flet as ft
from interfaces.class_scan import ScanDoc

class AppMain(ft.Container):
   # ---------------------------------------- FUNCIONES ----------------------------------------
   def change_content(self, e): #cambiar el contenido desde el nav-vertical
      data = int(e.data)
      if data == 0:
         self.cont_main.content = ft.Text("Data Project", size=30, color= ft.colors.RED_700)
      elif data == 1:
         # self.cont_main.content = ft.Text("Scan Containt", size=30, color= ft.colors.RED_700)
         self.cont_main.content = self.container_scan.content
      elif data == 2:
         self.cont_main.content = ft.Text("Table Students Containt", size=30, color= ft.colors.RED_700)
      elif data == 3:
         self.cont_main.content = ft.Text("Analitycs Containt", size=30, color= ft.colors.RED_700)
      else:
         self.cont_main.alignment = ft.alignment.center
         self.cont_main.content = ft.Text("Proximamente ...", size=30, color=ft.colors.ORANGE)
      self.cont_main.update()
   ...
   # ---------------------------------------- CONTROLES ----------------------------------------
   def __init__(self, page: ft.Page):
      super().__init__()
      self.page = page
      self.container_scan = ScanDoc(self.page)
      ...
      #           nav_rail
      self.nav_rail = ft.NavigationRail(
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
               ),
               ft.NavigationRailDestination(
                  icon= ft.icons.TABLE_CHART_OUTLINED,
                  selected_icon= ft.icons.TABLE_CHART,
                  label="Analitycs",
               ),
         ],
         on_change=self.change_content,
      )
      ...
      #           containers
      # self.cont_main = ft.Column(expand= True, horizontal_alignment= ft.CrossAxisAlignment.CENTER, auto_scroll=True,
      #                            controls= [ft.Text("Que quieres hacer???", size=30, color= ft.colors.ORANGE)])
      self.cont_main = ft.Container(
         expand=True,
         alignment=ft.alignment.center,
         padding=5,
         # content= self.clase-objeto.content,
         # content= ft.Text("Que quieres hacer???", size=30, color= ft.colors.ORANGE)
         content= ft.Row(expand= True, auto_scroll=True,
                         controls=[ft.Text("Que quieres hacer???", size=30, color= ft.colors.ORANGE)])
      )
      ...
      #           rows
      self.row_main = ft.Row(
         expand=True,
         auto_scroll=True,
         alignment=ft.MainAxisAlignment.START,
         controls=[self.nav_rail, ft.VerticalDivider(1,), self.cont_main],
      )

   def build(self):
   #           controles generales
      self.page.title = "APP - REFRISCAN"
      self.page.window.min_width = 710
      self.page.window.min_height = 800
      self.page.window.width = 720
      self.page.window.height = 810
   # ---------------------------------------- GRAPHICS ----------------------------------------
      self.page.add(self.row_main)
   ...

def main(page: ft.Page):
   app = AppMain(page)
   app.build()

if __name__ == "__main__":
   ft.app(target=main,)