import flet as ft
import json

#to get data students (json)
def data_get():
   with open("bd\\horario_estudiantes.json", 'r') as file:
      data_ = json.load(file)
   return data_

#update data students(json)
def data_set(data: dict):
   with open("bd\\horario_estudiantes.json", 'w') as file:
      json.dump(data, file, indent=4)

#colum names of DataTable
columns_name: list = ["Documento", "Horario", "# Faltas", "Acciones"]
data_table_style = {
   "expand": True,
   "border": ft.border.all(2, '#009852'),
   "border_radius": 10,
   "horizontal_lines": ft.border.BorderSide(1, '#84db52'),
   "columns": [
               ft.DataColumn(ft.Text(col, size= 16, color= '#000000', weight= 'bold'))
               for col in columns_name
              ]
}

...
class Controller: #rows controller (of table)
   items: dict = data_get()

   @staticmethod
   def update(): #update items
      Controller.items = data_get()

   @staticmethod
   def get_items(): #to get items
      return Controller.items
   
   @staticmethod
   def set_items(data): #unused
      Controller.items = data

   
   @staticmethod #unused
   def add_item(dato, contenido):
      Controller.items[dato] = contenido

...
class Table(ft.DataTable): #DataTable Controller
   def __init__(self, estudiantes):
      super().__init__(**data_table_style)

      self.dt = Controller.get_items()
      self.estudiantes = estudiantes #this is the main class of this .py, is usful pass it for parameters
   
   def update_dt(self): #update datas when you change or created a student in the Table
      Controller.update()
      self.dt = self.estudiantes.data

   def fill_data_table(self): #reload rows with changes in the Table
      self.rows = []
      keys = self.dt.keys()
      self.data_row_min_height = 55
      self.data_row_max_height = 60
      for key in keys:
         data = ft.DataRow([])
         data.cells.append(ft.DataCell(ft.Text(key)))
         horario = ""
         row = ft.Row(spacing= 0, wrap= True,)
         # ft.DataTable()
         for h in self.dt[key]['horario']:
            row.controls.append(ft.Text(value= f"-{h[0]}: ", color= 'black', weight= 'bold'))
            row.controls.append(ft.Text(value= f"{h[1]}; ", color= 'black', weight= 'w400'))
            # horario += f"*{h[0]}: {h[1]}; "
         data.cells.append(ft.DataCell(row))
         # data.cells.append(ft.DataCell(ft.Text(horario)))
         data.cells.append(ft.DataCell(ft.Text(self.dt[key]['faltas'])))
         data.cells.append(ft.DataCell(ft.ElevatedButton(text='Ver', data= key, bgcolor= "#4caf50", color='white',on_click= self.add_estudent)))
         
         self.rows.append(data)
         
   def add_estudent(self, e,): #update the modal view with a form to update data student
      self.estudiantes.content.controls[0].disabled = True #disable all out the modal
      self.estudiantes.dpw_dias.value = None
      self.estudiantes.dpw_horario.value = None

      doc = e.control.data #obtein doc studen, <<e>> is the button and butthon can save info
      self.estudiantes.formulario.offset = ft.transform.Offset(0.58, 0.12) #modal view visible
      #update datas
      self.estudiantes.horario = []
      self.estudiantes.doc = doc
      self.estudiantes.lb_doc.value = doc
      self.estudiantes.lb_doc.read_only= True
      self.estudiantes.horario = self.estudiantes.data[doc]["horario"]

      self.estudiantes.formulario.content.controls[5].content.controls = [
                                             ft.Row(alignment= ft.MainAxisAlignment.SPACE_BETWEEN, controls= [
                                             ft.Row([ft.Text(value= f"{h[0]}:", color= 'black', weight= 'bold'), ft.Text(value= f"{h[1]}", color= 'black', weight= 'w400')]),
                                             ft.IconButton(icon= ft.icons.DELETE, data= [h[0], h[1]], on_click= self.delete_horario), ])
                                             for h in self.estudiantes.horario
                                                      ]
      # print(self.estudiantes.horario)
      self.page.update()

   def delete_horario(self, e): #delete one student horary
      print(e.control.data)
      to_delete = e.control.data
      try:
         index = self.estudiantes.data[self.estudiantes.doc]['horario'].index(to_delete)
         self.estudiantes.data[self.estudiantes.doc]['horario'].pop(index)
         self.estudiantes.update_form()
      except Exception as e:
         print(e)

...
class TableEstudent(ft.Container):
   # ---------------------------------------- CONTROLES ----------------------------------------
   def __init__(self, page):
      super().__init__()
      self.page = page #main page
      self.page.fonts = {
         'Roboto400': 'https://fonts.googleapis.com/css2?family=Eagle+Lake&family=Roboto&display=swap',
      }
      self.page.theme = ft.Theme(font_family= 'Roboto400')
      self.data = data_get()  #data students

      self.table = Table(self) #-> ft.DataTable
      self.table.fill_data_table()

      ## formulario add or update student
      self.doc = None
      self.horario = [] #horary: [[day, morning|afternoon], ...]
      self.lb_doc = ft.TextField(border_radius= 10, color= 'black',) #input for new student
      self.dpw_dias = ft.Dropdown(icon= ft.icons.CALENDAR_MONTH, #options days
                              label= "Dia",
                              width= 235,
                              options= [
                                 ft.dropdown.Option("Lunes"),
                                 ft.dropdown.Option("Martes"),
                                 ft.dropdown.Option("Miercoles"),
                                 ft.dropdown.Option("Jueves"),
                                 ft.dropdown.Option("Viernes"),
                                 ft.dropdown.Option("Sabado"),
      ])

      self.dpw_horario = ft.Dropdown(icon= ft.icons.SUNNY_SNOWING, #options day[morning|afternoon]
                              label= "Horario",
                              width= 235,
                              options=[
                                 ft.dropdown.Option("Mañana"),
                                 ft.dropdown.Option("Tarde"),
      ])
      
      # "modal window"
      self.formulario = ft.Container(width= 500, height= 480, offset= ft.transform.Offset(-2, 0.38),
                                     border_radius= 15, bgcolor= "#ffffff", shadow= ft.BoxShadow(
                                                                  spread_radius=1,
                                                                  blur_radius=30,
                                                                  color= "#049457",
                                                                  offset=ft.Offset(0, 0),
                                                                  blur_style=ft.ShadowBlurStyle.OUTER,
                                                               ), padding= 10, 
                                     content= ft.Column([ft.Row(alignment= 'end', controls=[ft.OutlinedButton(text='Cerrar', style= ft.ButtonStyle(color= 'black',), on_click= self.close_modal),]),
                                                         self.lb_doc,
                                                        ft.Row([self.dpw_dias, self.dpw_horario,], spacing= 5),
                                                        ft.ElevatedButton(text= "Añadir", color= 'white', bgcolor= "#009852", on_click= self.add_horario),
                                                        ft.Divider(1, color= "#363537"),
                                                        ft.Container(content= ft.Column(scroll= ft.ScrollMode.AUTO), height= 170, padding= ft.padding.only(left=10, right= 10)),
                                             ], horizontal_alignment= ft.CrossAxisAlignment.CENTER)
                        )
      self.search_input = ft.TextField(prefix_icon= ft.icons.SEARCH, hint_text= "Buscar un beneficiario",
                                 border_radius= 15, on_change= self.filter_student
                                 )
      #main content, this is what you see when start the code
      self.content = ft.Stack(expand= True,controls=[ft.Column(expand= 1, horizontal_alignment= ft.CrossAxisAlignment.CENTER, offset= ft.transform.Offset(0, 0),
                               controls=[
                                  #search and button new student
                                  ft.Row(expand= True, alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
                                          controls=[
                                             self.search_input,
                                             ft.ElevatedButton(text= "Agregar Beneficiario", on_click= lambda e: self.add_estudent(e, self.doc), bgcolor= "#009852", color= 'white')
                                          ]
                                    ),
                                    #DataTable view
                                    ft.Container(height= 600, #width= 1000,
                                  content= ft.Column(expand= True, scroll= ft.ScrollMode.AUTO,
                                                    controls= [
                                                       self.table
                                                    ]
                                          )
                     )
                               ]), self.formulario,
               ])

   # ---------------------------------------- FUNCIONES ----------------------------------------
   def reload(self):
      self.search_input.value = ""
      self.table.fill_data_table()
      
   def filter_student(self, e): #filter data student in DataTable
      # print(e)
      for data_row in self.table.rows:
         data_cell = data_row.cells[0].content.value
         # print(data_cell)
         data_row.visible = (
            True
            if e.data in data_cell
            else False
         )

         data_row.update()

   def update_form(self): #update data student schedule (to reload the view)
      self.formulario.content.controls[5].content.controls = [
                                             ft.Row(alignment= ft.MainAxisAlignment.SPACE_BETWEEN, controls= [
                                             ft.Row([ft.Text(value= f"{h[0]}:", color= 'black', weight= 'bold'), ft.Text(value= f"{h[1]}", color= 'black', weight= 'w400')]),
                                             ft.IconButton(icon= ft.icons.DELETE, data= [h[0], h[1]], on_click= self.delete_horario), ])
                                             for h in self.horario
                                                      ]
      self.page.update()

   def add_estudent(self, e, doc: str): #add new student at DataTable
      self.content.controls[0].disabled = True
      self.dpw_dias.value = None
      self.dpw_horario.value = None
      self.formulario.offset = ft.transform.Offset(0.58, 0.12)
      self.horario = []

      # print(self.horario)
      self.page.update()

   def close_modal(self, e): #this method close the modal and update data student (json)
      self.content.controls[0].disabled = False
      self.lb_doc.read_only= False
      self.search_input.value = ""
      self.formulario.offset = ft.transform.Offset(-2, 0)
      self.formulario.content.controls[5].content.controls = []
      
      #update student schedule or add a new one
      # print(self.doc, self.horario)
      if self.doc in self.data: #old user student, so update
         print("usuario existente; update")
         self.data[self.doc]['horario'] = self.horario
         data_set(self.data)
         self.data = data_get()

      else: #new student, so add
         if self.lb_doc.value != "" and self.horario != []:
            print("usuario nuevo; add")
            datos = {
               "faltas": 0,
               "horario": self.horario,
               "is_beneficiario": True
            }
            self.data[self.doc] = datos
            data_set(self.data)
            self.data = data_get()
      #update data
      self.lb_doc.value = ""
      self.doc = ""
      self.table.update_dt()
      self.table.fill_data_table()
      self.page.update()

   def add_horario(self, e): #add schedule student with form modal view
      doc = self.lb_doc.value
      dia = self.dpw_dias.value
      horario = self.dpw_horario.value
      
      try:
         dia = dia.lower()
         horario = horario.lower()
      except Exception as e:
         print(e)
      self.doc = doc
      
      # if dia != "" and horario != "" and doc !=:
      if all([dia, horario, doc]):
         # print(self.horario)
         if [dia, horario] not in self.horario: #no allow to repeat schedule student
            self.horario.append([dia, horario])
         else:
            print("Ya está")
         self.update_form()

         self.dpw_dias.value = ""
         self.dpw_horario.value = ""

      self.page.update()

   def delete_horario(self, e): #delete schedule student with form modal view -> buttn trash
      print("delete horario")
      print(e.control.data)
      to_delete = e.control.data
      try:
         # index = self.data[self.doc]['horario'].index(to_delete)
         # self.data[self.doc]['horario'].pop(index)
         index = self.horario.index(to_delete)
         self.horario.pop(index)
         self.update_form()
      except Exception as e:
         print(e)


def main(page: ft.Page):
   # ---------------------------------------- GRAPHICS ----------------------------------------
   table = TableEstudent(page)
   page.window.width = 1100
   page.window.height = 700
   page.window.min_width = 800
   page.window.min_height = 700

   page.add(table)


if __name__ == "__main__":
   ft.app(target=main)  # Run the app