import flet as ft

import validaciones.valid_horario as valid #general, para correr la app.py
# import valid_horario as valid #temporal, para pruebas del modulo

import cv2 #captura de video
import threading #gestion de hilos
import time #pausas
import base64 #codificador de imagenes
import re #expresiones regulares
import numpy as np #arreglos
import pytesseract #vision img to str
import json #formato archivos
import requests #peticiones -> si la camara es por ip

#colores de interfaz -> temporal mientras soluciono como llamarlo desde otra carpeta
dict_colores = {
   "rojo": "#912323",
   "verde_poli": "#009852",
   "verde_selected": "#84db52",
   "gris": "#d9d9d9",
   "fondo": "#d2c3c3",
   "fondo2": "#d7b6b6",
   "blanco": "#ffffff"
}

#archivo con los documentos y los horarios de los beneficiarios del refrigerio
with open(r"bd\\horario_estudiantes.json", 'r') as file:
   data_ = json.load(file)


class ScanDoc(ft.Container):
      # ---------------------------------------- CONTROLES ----------------------------------------
   def __init__(self, page: ft.Page):
      super().__init__()
      self.page = page
      self.data_ = data_.copy()

      #####NOTA: Si se va usar una camara ip, entonces descomentar las lineas que tienen (#-->ip) y comentar (#-->pc)
      
      ##          camara
      # self.capture = cv2.VideoCapture(0) #-->pc
      self.capture = None #-->pc
      # self.capture = cv2.VideoCapture(1) #--> cam usb-phone
      # self.capture = cv2.VideoCapture("http://192.168.101.87:3660/video") #-->ip
      ...
      self.frame = None #frame qué se analizará para extraer el doc del estudiante
      
      #           hilo actualizar frame de camara
      self.threading_isrunning = True #controlador de hilo
      self.threading = threading.Thread(target= self.fun_update_frame_camera) #-->pc
      # self.threading = threading.Thread(target= self.fun_update_frame_camera_ip) #-->ip
      self.threading.start() #inicia el hilo
      ...

      #           hilo leer frame para covertir a txt
      self.threading_isrunning_txt = False #controlador de hilo
      
      self.threading_txt = threading.Thread(target= self.fun_toget_doc) #-->pc
      self.lock = threading.Lock()
      # self.threading_txt.start() #inicia el hilo dentro del fun_update_frame_camera
      ...

      #imagen qué se actualiza como camara en la interfaz, inicia con una opcional en caso de no encontrar la camara
      self.camera_img = ft.Image(width=345, height=245, src_base64=base64.b64encode(open(r"imgs\image_not_found.jpg", 'rb').read()).decode("utf-8"))
      ...

      ##          logotipo intitucional
      self.logo_path = r"imgs\escudo_institucional.png"
      self.logo = ft.Image(src=self.logo_path, height=150)
      ...

      ##          labels
      self.lb_doc = ft.TextField(value="" ,width= 200, bgcolor= dict_colores["blanco"], color= 'black', text_align= 'center',
                                 border= ft.border.all(2, color='green900',), border_radius=10, hint_text="Doc:")
      ...

      ##          botones
      self.btn_validate = ft.ElevatedButton(text=" ",icon= ft.icons.SEND_OUTLINED, on_click=self.fun_validate_doc)
      # self.btn_reload = ft.ElevatedButton(text=" ",icon= ft.icons.SEND_OUTLINED, on_click=self.fun_validate_doc)
      self.btn_reload = ft.Container(visible=False, border= ft.border.all(1, color= 'black100',), bgcolor= "transparent", border_radius=10,
                           content= ft.Icon(name= ft.icons.REPLAY_OUTLINED, color='black'), on_click=self.fun_reload,)
      self.btn_take_picture = ft.OutlinedButton(icon=ft.Icon("camera"), on_click=self.fun_take_picture) #-->pc
      # self.btn_take_picture = ft.OutlinedButton(icon=ft.Icon("camera"), on_click=self.fun_take_picture_ip) #-->ip
      ...

      ##          cards
      #card de frame - camara
      self.card_cam_view = ft.Card(width= 350, height=300,
                                   content= ft.Row(alignment="center", expand=True,
                                             controls=[ft.Column(expand=True, horizontal_alignment="center",
                                                   controls=[self.camera_img, self.btn_take_picture])]))
      
      #card de validación (ALLOW OR DENEGATED)
      ## iconoes
      self.icon_ = ft.Image(src=r"imgs\load.png", )
      self.icon_allow = ft.Image(src=r"imgs\aprobado.png", )
      self.icon_denegated = ft.Image(src=r"imgs\denegado.png", )
      ## text
      self.txt_doc_esstudiant = ft.Text(value="Doc: ", size=22, color= ft.colors.WHITE)
      self.txt_faltas = ft.Text(value="Numero Faltas: ", size=13, color= ft.colors.WHITE)
      self.txt_faltas_rest = ft.Text(value="Faltas Restantes para Bloquear: ", size=12, color= ft.colors.WHITE)
      ## card
      self.card_doc_description = ft.Card(
         width=420, height=180,
         content=ft.Row(expand=True, alignment="center", vertical_alignment="center",
               controls=[
                  ft.Container(width=100, height=100, bgcolor=ft.colors.TRANSPARENT, border_radius=50,
                  content= self.icon_, shadow=ft.BoxShadow(
                                                                  spread_radius=1,
                                                                  blur_radius=10,
                                                                  color=ft.colors.BLUE_GREY_100,
                                                                  offset=ft.Offset(0, 0),
                                                                  blur_style=ft.ShadowBlurStyle.OUTER,
                                                               )),
                  ft.VerticalDivider(width=1, color=ft.colors.TRANSPARENT),
                  ft.Container(width=270, height=150, bgcolor= ft.colors.BLACK26, border_radius=20, padding=5,
                               content= ft.Column(expand=True,
                                                  controls=[self.txt_doc_esstudiant,
                                                            self.txt_faltas, self.txt_faltas_rest]))
               ]
         )
      )
      ...

      ##          rows
      self.row_logo = ft.Row(alignment='center', height= 150,
                             controls=[self.logo])
      self.row_container = ft.Row(alignment='center', 
                                  controls=[ft.Container(bgcolor= dict_colores["blanco"], padding=15,
                                                      content=ft.Column(horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                                      controls=[self.card_cam_view, 
                                                                ft.Row(controls=[self.lb_doc, self.btn_validate, self.btn_reload], alignment='center'), 
                                                                self.card_doc_description]))])
      ...
      
      #Lo que exporta esta clase para la app-main
      self.content = ft.Container(expand=True,
                                  content= ft.Column(expand=True, horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                                     controls=[self.row_logo, self.row_container]))
   ...
   
   # ---------------------------------------- FUNCIONES ----------------------------------------
   def fun_update_frame_camera_ip(self):
      while self.threading_isrunning:
         try:
               # Obtener el flujo de datos de la cámara IP
               response = requests.get('http://192.168.101.87:3660/video', stream=True)
               if response.status_code == 200:
                  bytes_data = bytes()
                  for chunk in response.iter_content(chunk_size=1024):
                     bytes_data += chunk
                     a = bytes_data.find(b'\xff\xd8')
                     b = bytes_data.find(b'\xff\xd9')
                     if a != -1 and b != -1:
                           jpg = bytes_data[a:b+2]
                           bytes_data = bytes_data[b+2:]
                           frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                           frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                           # frame = cv2.flip(frame, 1)
                           self.frame = frame
                           _, buffer = cv2.imencode('.png', frame)
                           frame_b64 = base64.b64encode(buffer).decode("utf-8")
                           self.camera_img.src_base64 = frame_b64
                           self.page.update()
               else:
                  print(f"Error al conectarse a la cámara IP: {response.status_code}")
         except Exception as e:
               print(f"Error durante la transmisión del flujo: {e}")
               self.camera_img.src_base64 = base64.b64encode(open(r"imgs\image_not_found.jpg", 'rb').read()).decode("utf-8")
         time.sleep(0.03)
      print("::::::::: HILO PAUSADO O FINALIZADO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
   ...
   
   def fun_update_frame_camera(self, ):
      try:
         while self.threading_isrunning:
            ret, frame = self.capture.read()
            if ret:
               frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

               #las siguientes 2 lineas gestionan la lectura sin tener que press boton de captura
               self.threading_txt = threading.Thread(target= self.fun_toget_doc(frame)) #-->pc
               self.threading_txt.start() #inicia el hilo
               
               frame = cv2.flip(frame, 1) #invierte frame, para que se vea derecho si usa la camara selfie
               _, buffer = cv2.imencode('.png', frame)
               frame_b64 = base64.b64encode(buffer).decode("utf-8")
               
               #actualiza el contenedor de la imagen de la camara (simula grabación en tiempo real, realidad: frama-frame)
               self.camera_img.src_base64 = frame_b64
               
               self.page.update()
            else:
               self.camera_img.src_base64 = base64.b64encode(open(r"imgs\image_not_found.jpg", 'rb').read()).decode("utf-8")
            # time.sleep(0.03)
         print("::::::::: HILO PAUSADO O FINALIZADO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      except Exception as e:
         print(f"Error de captura de video: {e}")
         # self.threading_isrunning = True
         # self.threading = threading.Thread(target=self.fun_update_frame_camera)
         # self.threading.start()
         self.page.update()

   ...

   def fun_toget_doc(self, image): 
      # print(self.lb_doc.value) 
      try:
         #gestionar el hilo para que no se habra uno nuevo sin haber terminado
         with self.lock: 
            if self.lb_doc.value in self.data_: 
               print("Valor ya presente en los datos, omitiendo el hilo") 
               return 
            if self.threading_isrunning_txt: 
               print("Hilo ya en ejecución, omitiendo") 
               return 
            
            print("ENTRANDO AL HILO GET_DOC") 
            #!cierro el hilo, y no habre hasta que este de respuesta
            self.threading_isrunning_txt = True 

            # Especifica la ruta de Tesseract manualmente para no agregar el PATH como variable de entorno 
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 
            
            # Convertimos el contenido de la imagen a str 
            extracted_text = pytesseract.image_to_string(image) 
            
            # Filtrar solo los números usando expresiones regulares // PARA CEDULAS VIEJAS 
            numbers = re.findall(r'\d+', extracted_text) 
            
            # Extrae solo secuencias de dígitos 
            # Usar una expresión regular para encontrar la línea que contiene "NUIP"// PARA CEDULAS NUEVAS  
            match = re.search(r'NUIP \d+\.\d+\.\d+\.\d+', extracted_text) 

            # Verificar si se encontró una coincidencia, True: cedula es nueva, False: cedula es vieja 
            if match: 
               nuip_line = match.group() 
               nuip_digits = re.sub(r'\D', '', nuip_line) 
               self.lb_doc.value = nuip_digits 
               print(nuip_digits) 
            else: 
               text = ''.join(numbers) 
               self.lb_doc.value = text 
               print(text) 

            #!abro el hilo para que pueda iniciar uno nuevo   
            self.threading_isrunning_txt = False
      except Exception as e:
         print(f"Error al optener el documento del estudiante: {e}")
         self.threading_isrunning = True

   ...

   def fun_take_picture(self, e): #se puede capturar el doc por boton en vez de hacerlo frame-frame (más optimo para pc bajo recursos)
      try:
         # Detenemos temporalmente la actualización de la cámara
         self.threading_isrunning = False

         # Capturamos el frame actual de la cámara
         ret, frame = self.capture.read()
         if ret:
            # frame = cv2.flip(frame, 1)
            # Convertimos el frame a base64
            self.frame = frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, buffer = cv2.imencode(".png", frame)
            
            frame_base64 = base64.b64encode(buffer).decode("utf-8")
            photo = ft.Image(width=100, height=100, src_base64=frame_base64)
            
            # frame = self.frame
            # cv2.imwrite("fotocc.png", frame) #guardar la foto, pruebas
            # self.fun_toget_doc(frame)

            #inicia el hilo GET_DOC // si es por boton, esta función puede o no tratarse como hilo
            self.threading_txt = threading.Thread(target= self.fun_toget_doc(frame)) #-->pc
            self.threading_txt.start() 
            
            # Actualizamos la tarjeta con la nueva imagen capturada..> lo dejo por gusto, pero es necesario eliminarlo
            self.card_doc_description.content.controls[0].content = photo
            self.page.update()

            # Reiniciamos la actualización de la cámara
            self.threading_isrunning = True
            self.threading = threading.Thread(target=self.fun_update_frame_camera)
            self.threading.start()
         else:
            print("No se pudo capturar el frame de la cámara")
         self.page.update()
      except Exception as e:
         print(f"Error al tomar la foto: {e}")
         self.threading_isrunning = True
         self.threading = threading.Thread(target=self.fun_update_frame_camera)
         self.threading.start()
         self.page.update()

   ...

   def fun_take_picture_ip(self, e):
      frame = self.frame
      self.fun_toget_doc(frame)
      ...

   def fun_validate_doc(self, e):
      self.btn_reload.visible = True
      print(self.lb_doc.value)
      id = self.lb_doc.value

      if valid.validarEntrega(id): #valida si el doc, puede reclamar en dicho dia y horario
         faltas = self.data_[id]['faltas'] #calcula el total de faltas = dias_que no reclamó, 3 = desactivar usuario

         self.txt_doc_esstudiant.value = f"Doc: {id}"
         self.txt_faltas.value = f"Numero Faltas: {faltas}"
         self.txt_faltas_rest.value = f"Faltas Restantes para Bloquear: {3 - faltas}"
         self.card_doc_description.content.controls[0].content = self.icon_allow
         self.card_doc_description.content.controls[0].shadow = ft.BoxShadow( #sombra del contenedor permitido-denegado
                                                                  spread_radius=1,
                                                                  blur_radius=15,
                                                                  color=ft.colors.GREEN_ACCENT_100,
                                                                  offset=ft.Offset(0, 0),
                                                                  blur_style=ft.ShadowBlurStyle.OUTER,
                                                               )
      else:
         self.txt_doc_esstudiant.value = f"Doc: "
         self.txt_faltas.value = f"Numero Faltas: "
         self.txt_faltas_rest.value = f"Faltas Restantes para Bloquear: "
         self.card_doc_description.content.controls[0].content = self.icon_denegated
         self.card_doc_description.content.controls[0].shadow = ft.BoxShadow( #sombra del contenedor permitido-denegado
                                                                  spread_radius=1,
                                                                  blur_radius=15,
                                                                  color=ft.colors.RED_ACCENT_100,
                                                                  offset=ft.Offset(0, 0),
                                                                  blur_style=ft.ShadowBlurStyle.OUTER,
                                                               )
      self.page.update()
      # print()
   ...

   def fun_reload(self, e):
      self.lb_doc.value = ""
      self.card_doc_description.content.controls[0].content = self.icon_
      self.card_doc_description.content.controls[0].shadow = ft.BoxShadow( #sombra del contenedor permitido-denegado
                                                               spread_radius=1,
                                                               blur_radius=15,
                                                               color= ft.colors.BLUE_GREY_100,
                                                               offset=ft.Offset(0, 0),
                                                               blur_style=ft.ShadowBlurStyle.OUTER,
                                                            )
      self.btn_reload.visible = False
      self.page.update()

   def fun_(self, e): #..> futuro

      ...





def main(page: ft.Page):
   app = ScanDoc(page)

   # ---------------------------------------- GRAPHICS ----------------------------------------
   page.title = "Container Scan"
   page.window.min_width = 700
   page.window.min_height = 870
   page.window.max_width = 710
   page.window.max_height = 870
   page.window.width = 700
   page.window.height = 870
   page.padding = 5
   page.window.bgcolor = ft.colors.BACKGROUND
   page.theme_mode = ft.ThemeMode.DARK
   page.add(app)

if __name__ == "__main__":
   ft.app(target=main)

