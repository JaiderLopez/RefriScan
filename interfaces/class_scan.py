import flet as ft
# from colores import dict_colores
import cv2
import threading
import time
import base64
from PIL import Image
import re
import numpy as np
import pytesseract
import requests


dict_colores = {
   "rojo": "#912323",
   "verde_poli": "#009852",
   "verde_selected": "#84db52",
   "gris": "#d9d9d9",
   "fondo": "#d2c3c3",
   "fondo2": "#d7b6b6",
   "blanco": "#ffffff"
}
class ScanDoc(ft.Container):
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
      
      while self.threading_isrunning:
         ret, frame = self.capture.read()
         if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # self.fun_toget_doc(frame)
            _, buffer = cv2.imencode('.png', frame)
            frame_b64 = base64.b64encode(buffer).decode("utf-8")
            self.camera_img.src_base64 = frame_b64
            self.page.update()
         else:
            self.camera_img.src_base64 = base64.b64encode(open(r"imgs\image_not_found.jpg", 'rb').read()).decode("utf-8")
         # time.sleep(0.03)
      print("::::::::: HILO PAUSADO O FINALIZADO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
   ...
   def fun_toget_doc(self, image):
      # Especifica la ruta de Tesseract manualmente para no agregar el PATH como variable de entorno
      pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
      
      # convertimos el contenido de la imagen a str
      extracted_text = pytesseract.image_to_string(image)

      # Filtrar solo los números usando expresiones regulares // PARA CEDULAS VIEJAS
      numbers = re.findall(r'\d+', extracted_text)  # Extrae solo secuencias de dígitos

      # Usar una expresión regular para encontrar la línea que contiene "NUIP"// PARA CEDULAS VIEJAS
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
      ...

   def fun_take_picture(self, e):
      # Detenemos temporalmente la actualización de la cámara
      self.threading_isrunning = False
      # self.date_picture.value = time.strftime("%Y-%m-%d_%H%M%S")
      # self.date_picture.update()

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
         frame = self.frame
         self.fun_toget_doc(frame)
         # Actualizamos la tarjeta con la nueva imagen
         self.card_doc_description.content.controls[0].content = photo
         self.page.update()

         # Reiniciamos la actualización de la cámara
         self.threading_isrunning = True
         self.threading = threading.Thread(target=self.fun_update_frame_camera)
         self.threading.start()
      else:
         print("No se pudo capturar el frame de la cámara")
      self.page.update()
   ...

   def fun_take_picture_ip(self, e):
      frame = self.frame
      self.fun_toget_doc(frame)
      ...

   def fun_validate_doc(self, e):
      print(self.lb_doc.value)
      ...
   ...

   def fun_(self, e):

      ...
   # ---------------------------------------- CONTROLES ----------------------------------------
   def __init__(self, page: ft.Page):
      super().__init__()
      self.page = page
      ##          camara
      self.capture = cv2.VideoCapture(0) #-->pc
      # self.capture = cv2.VideoCapture("http://192.168.101.87:3660/video") #-->ip
      self.frame = None #frame qué se analizará para extraer el doc del estudiante
      self.threading_isrunning = True #controlador de hilo
      self.threading = threading.Thread(target= self.fun_update_frame_camera) #-->pc
      # self.threading = threading.Thread(target= self.fun_update_frame_camera_ip) #-->ip
      self.threading.start()

      self.camera_img = ft.Image(width=345, height=245, src_base64=base64.b64encode(open(r"imgs\image_not_found.jpg", 'rb').read()).decode("utf-8"))
      ...

      ##          logotipo intitucional
      self.logo_path = r"imgs\escudo_institucional.png"
      self.logo = ft.Image(src=self.logo_path, height=150)
      ...

      ##          labels
      self.lb_doc = ft.TextField(read_only=True, width= 200, bgcolor= dict_colores["blanco"], color= dict_colores["verde_poli"],
                                 border= ft.border.all(2, color='green900',), border_radius=10, hint_text="cc:")
      ...

      ##          botones
      self.btn_validate = ft.ElevatedButton(" ",icon=ft.icons.SEND_AND_ARCHIVE_OUTLINED, on_click=self.fun_validate_doc)
      self.btn_take_picture = ft.OutlinedButton(icon=ft.Icon("camera"), on_click=self.fun_take_picture) #-->pc
      # self.btn_take_picture = ft.OutlinedButton(icon=ft.Icon("camera"), on_click=self.fun_take_picture_ip) #-->ip
      ...

      ##          cards
      self.card_cam_view = ft.Card(width= 350, height=300,
                                   content= ft.Row(alignment="center", expand=True,
                                             controls=[ft.Column(expand=True, horizontal_alignment="center",
                                                   controls=[self.camera_img, self.btn_take_picture])]))
                                 #   ft.Row(expand=True, alignment="center", vertical_alignment="center",
                                 #                   controls=[self.camera_img, self.btn_take_picture]))
                                                   # controls=[ft.Text("CAM SCAN")]))
      self.card_doc_description = ft.Card(
         width=420, height=180,
         content=ft.Row(expand=True, alignment="center", vertical_alignment="center",
               controls=[
                  ft.Container(width=100, height=100, bgcolor="blue800"),
                  ft.VerticalDivider(width=1, color=ft.colors.TRANSPARENT),
                  ft.Container(width=270, height=150, bgcolor="blue800",
                               content= ft.Column(expand=True,
                                                  controls=[]))
               ]
         )
      )
      
      

      ##          rows
      self.row_logo = ft.Row(alignment='center', height= 150,
                             controls=[self.logo])
      self.row_container = ft.Row(alignment='center', 
                                  controls=[ft.Container(bgcolor= dict_colores["fondo"], padding=30,
                                                      content=ft.Column(horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                                      controls=[self.card_cam_view, 
                                                                ft.Row(controls=[self.lb_doc, self.btn_validate], alignment='center'), 
                                                                self.card_doc_description]))])
      
      
      self.content = ft.Container(expand=True,
                                  content= ft.Column(expand=True, horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                                     controls=[self.row_logo, self.row_container]))

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

