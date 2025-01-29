import flet as ft
from WhisperSrc.whisper_python import whisperPythonFunction  # Asegúrate de que esta función esté definida correctamente
import time

def main(page: ft.Page):

    page.window.width = 800
    page.window.height = 600
    page.window.resizable = False
    page.title = "Whisper"

    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int(seconds % 3600 // 60)
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:06.3f}"
    

    transcription_done = False  # Variable para saber si la transcripción fue realizada

    Export_Rute = ft.Text(value="Archivo guardado en: Aun no ha transcrito un archivo", color=ft.Colors.BLACK)

    def FileExporter(e):
        # Asumimos que el archivo fue cargado correctamente a través de `pick_files_result`
        # Verifica que se haya seleccionado un archivo antes de intentar exportar
        if selected_files.value != "Cancelled!" and selected_files.value != "":
            try:
                Export_Rute.value = ft.FilePicker.save_file()
                Export_Rute.update()
            except:
                Export_Rute.value = "ERROR"



            
            
        else:
            Export_Rute.value = "No se ha seleccionado un archivo para exportar"
            Export_Rute.update()

    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    def transcribir(e):
        nonlocal transcription_done  # Usamos la variable fuera de la función

        # Obtener el nombre del archivo seleccionado
        file_name = selected_files.value
        try:
            if file_name != "Cancelled!" and file_name != None:
                # Llama a la función de transcripción
                transcription = whisperPythonFunction(file_name)  # Asegúrate de que esta función acepte el nombre del archivo
                # Muestra la transcripción en la interfaz
                transcription_result.value = transcription
                transcription_output.value = "Archivo transcrito con éxito"
                try:
                    for segment in transcription["segments"]:
                        start_time_segment = format_time(segment["start"])
                        end_time_segment = format_time(segment["end"])
                        text = segment["text"]
                        lv.controls.append(ft.Text(f"[{start_time_segment} - {end_time_segment}] {text} \n", color=ft.Colors.BLACK))
                        page.update()
                    transcription_done = True  # Actualizamos la variable cuando se termina la transcripción
                    export_button.disabled = False  # Habilitamos el botón Exportar
                    page.update()  # Actualizamos la página para reflejar el cambio
                except:
                    print("Error procesando los segmentos.")
                transcription_output.update()
                
            else:
                transcription_output.value = "No se seleccionó un archivo"

        except:
            transcription_output.value = "Error, el archivo seleccionado no es válido"
        
        page.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text(color=ft.Colors.BLACK)
    transcription_output = ft.Text(color=ft.Colors.BLACK)  # Para mostrar la transcripción
    transcription_result = ft.Text(color=ft.Colors.BLACK)  # Para mostrar la transcripción
    page.overlay.append(pick_files_dialog)
    



    page.window.width = 500
    page.window.height = 800
    page.window.resizable = True
    page.title = "Whisper"
    page.padding = 0

    # Definir los textos que estarán en los contenedores
    top_r = ft.Column(
        [
            ft.Text(value="Archivo cargado: ", color=ft.Colors.BLACK),
            selected_files,
            ft.ElevatedButton(
                "Pick files",
                icon=ft.Icons.UPLOAD_FILE,
                on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True)
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    mid = ft.Column([lv])

    export_button = ft.ElevatedButton(
        "Exportar",
        icon=ft.Icons.UPLOAD_FILE,
        disabled=True,  # Inicia como deshabilitado
        on_click=FileExporter
    )

    bot = ft.Column(
        [
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Transcribir",
                        icon=ft.Icons.UPLOAD_FILE,
                        on_click=transcribir
                    ),
                    export_button,  # Usamos el botón export_button aquí
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            transcription_output,
            Export_Rute
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )


    #### Contenedores ####

    superior = ft.Container(
        top_r,
        width=450,
        height=150,
        margin=ft.margin.only(top=130),
        border=ft.border.all()
    )
    
    centro = ft.Container(mid, width=450, height=200, margin=ft.margin.only(top=20), border=ft.border.all())
    inferior = ft.Container(bot, width=450, height=130, margin=ft.margin.only(top=20), border=ft.border.all())

    col = ft.Column(
        spacing=20,
        controls=[
            superior,
            centro,
            inferior,
        ]
    )

    contenedor = ft.Container(
        col,
        width=page.window.width,
        height=page.window.height,
        bgcolor=ft.Colors.WHITE,
        alignment=ft.alignment.top_center
    )

    page.add(contenedor)
    page.update()

ft.app(main)
