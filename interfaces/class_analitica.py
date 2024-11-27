import flet as ft
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import pandas as pd
import seaborn as sns
import datetime
import threading
import json

class Analitica(ft.Container):
    def __init__(self, page):
        # Contenido de la pestaña "Gráficas Históricas"
        super().__init__()
        self.page = page

        self.data_frame: pd.DataFrame = self.get_dataframe()

        self.registros: list= self.info_general()
        self.info = ft.Column( horizontal_alignment= ft.CrossAxisAlignment.CENTER, spacing= 10,
            controls= [
                ft.Text(f"El Total de Registros Actuales es de: {self.registros[0]}", size= 22),
                ft.Row([
                ft.Text(f"Total reclamos de Beneficiarios: {self.registros[1][0]}", size= 18),
                ft.Text(f"Total reclamos de No Beneficiarios: {self.registros[1][1]}", size= 18),
                ], alignment= 'center', ),
                ft.Row([ft.Text("Beneficiario con más reclamos",weight= 'bold',size= 12), ft.Text("No-Beneficiario con más reclamos",weight= 'bold',size= 12)], alignment= 'center'),
                ft.Row([
                ft.Column(ft.Container(border_radius= 10, bgcolor= "#73d28f", padding = 5,
                                content= ft.Row([ft.Text(f"{doc[0]}: ", color= 'black', weight= 'bold'), ft.Text(f"{doc[1]}", color= 'black')]))
                                for doc in self.registros[2][0]),
                ft.Column(ft.Container(border_radius= 10, bgcolor= "#73d28f", padding = 5,
                                content= ft.Row([ft.Text(f"{doc[0]}: ", color= 'black', weight= 'bold'), ft.Text(f"{doc[1]}", color= 'black')]))
                                for doc in self.registros[2][1]),
                                
                ], alignment= 'center', spacing= 100,),
            ]
        )
        
        # thread = threading.Thread(target=self.generar_grafico, args=(self.data_frame,)) 
        # thread.start()

        self.figuras_historicas: list = []
        self.figuras_historicas.append(self.grafica_histograma("mañana"))
        self.figuras_historicas.append(self.grafica_histograma("tarde"))
        self.figuras_historicas.append(self.grafica_caja("mañana"))
        self.figuras_historicas.append(self.grafica_caja("tarde"))
        self.figuras_historicas.append(self.grafica_reclamos_horario())
        self.figuras_historicas.append(self.grafica_reclamos_doc())
        
        self.graficas: list = [] 
        self.graficas.append(MatplotlibChart(self.figuras_historicas[0], expand=True))
        self.graficas.append(MatplotlibChart(self.figuras_historicas[1], expand=True))
        self.graficas.append(MatplotlibChart(self.figuras_historicas[2], expand=True))
        self.graficas.append(MatplotlibChart(self.figuras_historicas[3], expand=True))
        self.graficas.append(MatplotlibChart(self.figuras_historicas[4], expand=True))
        self.graficas.append(MatplotlibChart(self.figuras_historicas[5], expand=True))
        
        self.tab_historicas = ft.Container(
            # alignment= ft.alignment.center,
            content=ft.Column([
                ft.Text("Gráficas Históricas", size=30, weight="bold"),
                self.info,
                ft.Row([
                ft.Container(width=self.page.width / 2 - 150, height=self.page.height - 150,bgcolor="#43a047", border_radius=10, content= self.graficas[0]),
                ft.Container(width=self.page.width / 2 - 150, height=self.page.height - 150,bgcolor="#43a047", border_radius=10, content= self.graficas[1]),
                # ft.Container(width=self.page.width / 2 - 150, height=self.page.height - 150,bgcolor="#43a047", border_radius=10, ),
                ], alignment= 'center'),
                ft.Row([
                ft.Container(width=self.page.width / 2 - 150, height=self.page.height - 150,bgcolor="#43a047", border_radius=10, content= self.graficas[2]),
                ft.Container(width=self.page.width / 2 - 150, height=self.page.height - 150,bgcolor="#43a047", border_radius=10, content= self.graficas[3]),
                # ft.Container(width=self.page.width / 2 - 150, height=self.page.height - 150,bgcolor="#43a047", border_radius=10, ),
                ], alignment= 'center'),
                ft.Row([
                ft.Container(width=self.page.width / 2 - 150, height=self.page.height - 150,bgcolor="#43a047", border_radius=10, content= self.graficas[4]),
                ft.Container(width=self.page.width / 2 - 150, height=self.page.height - 150,bgcolor="#43a047", border_radius=10, content= self.graficas[5]),
                # ft.Container(width=self.page.width / 2 - 150, height=self.page.height - 150,bgcolor="#43a047", border_radius=10, ),
                ], alignment= 'center'),
            ], spacing=20, horizontal_alignment= ft.CrossAxisAlignment.CENTER)
        )

        # Contenido de la pestaña "Gráficas del Día"
        self.datepicker = ft.DatePicker(
                    first_date=datetime.datetime(2024, 11, 1),
                    last_date=datetime.datetime(2024, 11, 26),
                    on_change=self.change_date,
                )
        self.selected_date = ft.TextField(read_only= True, width= 150)
        self.btn_update = ft.ElevatedButton(text= "Actualizar", icon= ft.cupertino_icons.RESTART, bgcolor= 'transparent',
                                            visible= False, on_click= self.update_graphics)
        self.btn_date = ft.ElevatedButton(
                        "Pick date",
                        icon=ft.icons.CALENDAR_MONTH,
                        on_click=self.open_date_picker,
                    )
        self.figuras_dia: list = []
        self.figuras_dia.append(self.grafica_dispersion_xdia("2024-11-25", 'mañana'))
        self.figuras_dia.append(self.grafica_dispersion_xdia("2024-11-25", 'tarde'))
        self.graficas_dia: list = []
        self.graficas_dia.append(MatplotlibChart(self.figuras_dia[0], expand=True))
        self.graficas_dia.append(MatplotlibChart(self.figuras_dia[1], expand= True))
        self.tab_dia = ft.Container(
            content=ft.Column([
                ft.Text("Gráficas del Día", size=30, weight="bold"),
                ft.Row([self.selected_date, self.btn_update, self.btn_date], alignment= 'center'),
                ft.Row([
                ft.Container(width=self.page.width / 2 - 150, height=self.page.height - 150, bgcolor=ft.colors.GREEN_200, border_radius=10, content= self.graficas_dia[0]),
                ft.Container(width=self.page.width / 2 - 150, height=self.page.height - 150, bgcolor=ft.colors.GREEN_200, border_radius=10, content= self.graficas_dia[1]),
                ], alignment= 'center'),
            ], spacing=20, horizontal_alignment= ft.CrossAxisAlignment.CENTER)
        )

        # Crear Tabs
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tab_alignment= ft.TabAlignment.CENTER
            ,tabs=[
                ft.Tab(text="Gráficas Históricas", content=self.tab_historicas),
                ft.Tab(text="Gráficas del Día", content=self.tab_dia)
            ]
        )

        # Agregar Tabs al Container principal
        self.content = ft.Container(padding= ft.padding.only(top= 15), bgcolor="#ffffff", height= 800,
                                    content= ft.Column(expand= True, horizontal_alignment= ft.CrossAxisAlignment.CENTER, 
                                    scroll= ft.ScrollMode.AUTO, 
                                            controls=[self.tabs]))

    def generar_grafico(self, df):
        self.figuras_historicas.append(self.grafica_histograma("mañana"))
        self.figuras_historicas.append(self.grafica_histograma("tarde"))

    def get_json(self, dirr: str):
        with open(dirr, 'r') as file:
            data = json.load(file)
        return data

    def get_dataframe(self,):
        path_analitica = 'bd\\analitica.json'
        analitica = self.get_json(path_analitica)

        df = pd.DataFrame.from_dict(analitica['1'], orient= 'index').reset_index(drop=True)
        rango = len(analitica.keys())
        for i in range(2, rango):
            df = pd.concat([df, pd.DataFrame.from_dict(analitica[f'{i}'], orient= 'index')])
        return df

    def grafica_caja(self, horario):
        df = self.data_frame.copy()
        df_ho_ma = df[df['horario']== horario]
        fig = plt.figure(figsize=(8, 8))
        # fig, ax = plt.subplots()
        sns.boxplot(x=df_ho_ma['fecha'], y= df_ho_ma['hora'])
        plt.xlabel('fechas')
        plt.ylabel('horas')
        plt.title('Fechas vs Horas de Reclamo')
        plt.xticks(rotation=90)
        # plt.show()
        return fig

    def grafica_histograma(self, horario):
        df = self.data_frame.copy()
        if horario == "mañana":
            inicio = '11:00'
            fin = '14:00'
        else:
            inicio = '18:00'
            fin = '21:00'
        
        # Convertir la columna 'hora' a tipo datetime
        df['hora'] = pd.to_datetime(df['hora'], format='%H:%M').dt.time
        
        # Filtrar por intervalos de tiempo
        df_horario = df[(df['hora'] >= pd.to_datetime(inicio, format='%H:%M').time()) & 
                            (df['hora'] <= pd.to_datetime(fin, format='%H:%M').time())]

        # Crear intervalos de tiempo cada 5 min
        df_horario['intervalo'] = df_horario['hora'].apply( lambda x: (pd.to_datetime(x, format='%H:%M:%S').floor('5min').time()) )
        
        # Contar los reclamos por intervalo
        histograma = df_horario.groupby('intervalo').size()

        # Crear histogramas
        # fig, axs = plt.subplots(figsize=(10, 8))
        fig = plt.figure(figsize=(8, 8))
        # Graficar el histograma
        plt.bar(histograma.index.astype(str), histograma.values, width= 1)
        plt.title(f'Reclamos entre las {inicio} y las {fin}')
        plt.xlabel('Intervalos de Tiempo')
        plt.ylabel('Número de Reclamos')
        plt.xticks(rotation=90)
        plt.tight_layout()

        return fig

    def grafica_reclamos_horario(self, ):
        df = self.data_frame.copy()
        df_hor = df.groupby('horario').size()
        fig = plt.figure(figsize=(8, 8))
        plt.bar(df_hor.index, df_hor.values)
        plt.xlabel('Horario')
        plt.ylabel('cantidades')
        plt.title('Reclamos de Refrigerios por Horario')
        plt.xticks(rotation=90);

        return fig

    def grafica_reclamos_doc(self, ):
        df = self.data_frame.copy()
        df_doc = df.groupby('documento').size()
        fig = plt.figure(figsize=(8, 8))
        plt.bar(df_doc.index, df_doc.values)
        plt.xlabel('Documento')
        plt.ylabel('cantidades')
        plt.title('Reclamos de Refrigerios por Documento')
        plt.xticks(rotation=90);
        return fig

    def grafica_dispersion_xdia(self, fecha, horario):
        df = self.data_frame.copy()
        # fec = fecha
        df_dia = df[(df['fecha'] == fecha) & (df['horario'] == horario)]
        fig = plt.figure(figsize= (8, 8))
        sns.scatterplot(x=df_dia['documento'], y= df_dia['hora'])
        plt.title(f'Reclamos de Refrigerios el {fecha} en la {horario}')
        plt.xlabel('Documentos')
        plt.ylabel('Horas')
        plt.xticks(rotation= 90);
        return fig

    def info_general(self,):
        try:
            df = self.data_frame.copy()
            df_bene = df[df['is_beneficiario']== True]
            df_nobene = df[df['is_beneficiario']== False]
            registros = int(df.shape[0])
            reclamos_bene = df_bene.shape[0]
            reclamos_nobene = df_nobene.shape[0]
            
            df_doc = df_bene.groupby('documento').size()
            tt= df_doc.sort_values(ascending=False)
            top3 = tt.head(3)
            doc_max = list(top3.index)
            count_max = list(top3.values)
            val = [(doc_max[0], count_max[0]),(doc_max[1], count_max[1]),(doc_max[2], count_max[2]),]
            df_docn = df_nobene.groupby('documento').size()
            ttn= df_docn.sort_values(ascending=False)
            top3n = ttn.head(3)
            doc_not_max = list(top3n.index)
            count_not_max = list(top3n.values)
            valn = [(doc_not_max[0], count_not_max[0]),(doc_not_max[1], count_not_max[1]),(doc_not_max[2], count_not_max[2]),]

            return [registros, [reclamos_bene, reclamos_nobene], [val, valn], [doc_not_max, count_not_max]]
        except Exception as e:
            print(f'Error en info_general: {e}')

    def open_date_picker(self, e):
        self.page.open(self.datepicker)

    def change_date(self, e):
        fecha:str = str(self.datepicker.value)
        fecha = fecha.split(' ')[0]
        self.selected_date.value = fecha
        self.btn_update.visible = True
        e.control.page.update()

    def update_graphics(self, e):
        self.btn_update.visible = False
        figura1 = self.grafica_dispersion_xdia(self.selected_date.value, "mañana")
        self.graficas_dia[0]= MatplotlibChart(figura1, expand=True)
        fig1 = ft.Container(width=self.page.width / 2 - 150, height=self.page.height - 150, bgcolor=ft.colors.GREEN_200, border_radius=10, content= self.graficas_dia[0])
        self.tab_dia.content.controls[2].controls[0] = fig1
        
        figura2 = self.grafica_dispersion_xdia(self.selected_date.value, "tarde")
        self.graficas_dia[1]= MatplotlibChart(figura2, expand=True)
        fig2 = ft.Container(width=self.page.width / 2 - 150, height=self.page.height - 150, bgcolor=ft.colors.GREEN_200, border_radius=10, content= self.graficas_dia[1])
        self.tab_dia.content.controls[2].controls[1] = fig2
        self.tab_dia.update()
        
    def reload_data(self,):
        self.data_frame: pd.DataFrame = self.get_dataframe()
        self.page.update()

    
def main(page: ft.Page):
    app = Analitica(page)
    page.title = "Presentación de Gráficas"
    page.scroll = ft.ScrollMode.AUTO
    # page.window.height = 799
    page.add(app)

# Ejecutar la aplicación Flet
if __name__ == "__main__":
   ft.app(target=main)


