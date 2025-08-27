#Librerías
import customtkinter as ctk
import os
import json
from PIL import Image
from temas import TemasColores
from colors import COLOR_OPTIONS, COLOR_NAME_TO_HEX, HEX_TO_COLOR_NAME, DEFAULT_COLOR_NAME, contrast_ratio
from i18n import I18N
from ajustes_fuente import DEFAULT_FONT_SIZE, parse_font_size

# Instancia global de temas
temas = TemasColores()
preferencias = {}

# Límites y parser de tamaño de fuente se manejan en settings.py

# Opciones de color y traducciones se importan desde modules colors.py e i18n.py

def _get_lang_code():
    try:
        idioma = preferencias.get("idioma", "Español")
    except NameError:
        idioma = "Español"
    return "en" if str(idioma).lower().startswith("english") else "es"

def t(key):
    return I18N.get(_get_lang_code(), I18N["es"]).get(key, key)

def aplicar_tema_aplicacion(nombre_tema=None):
    if nombre_tema:
        temas.cambiar_tema(nombre_tema)
    
    tema_actual = temas.obtener_tema()
    # Si se está cambiando el tema, sobrescribir preferencias de color con valores del tema
    if nombre_tema:
        try:
            preferencias["tema"] = nombre_tema
            preferencias["color_menu"] = tema_actual.get("bg_frames")
            preferencias["color_fuente"] = tema_actual.get("texto_principal")
            almacenar_preferencias()
            # Actualizar comboboxes si existen
            if 'combobox_cambiar_color_menu' in globals():
                nombre_menu = HEX_TO_COLOR_NAME.get(preferencias["color_menu"].lower(), "Personalizado")
                combobox_cambiar_color_menu.set(nombre_menu)
            if 'combobox_cambiar_fuente' in globals():
                nombre_fuente_color = HEX_TO_COLOR_NAME.get(preferencias["color_fuente"].lower(), "Personalizado")
                combobox_cambiar_fuente.set(nombre_fuente_color)
            if 'combobox_cambiar_tema' in globals():
                try:
                    display_tema = temas.configurador.obtener_nombre_display(nombre_tema)  
                    combobox_cambiar_tema.set(display_tema)
                except Exception:
                    pass
        except Exception:
            pass
    
    color_texto = preferencias.get("color_fuente", tema_actual["texto_principal"])
    try:
        bg = tema_actual["bg_secundario"]
        if contrast_ratio(color_texto, bg) < 1.5:
            color_texto = tema_actual["texto_principal"]
    except Exception:
        pass
    
    # Aplicar colores a la ventana principal
    app.configure(fg_color=tema_actual["bg_principal"])
    
    # Aplicar colores a los frames
    color_menu = preferencias.get("color_menu")
    frame_botones.configure(fg_color=color_menu if color_menu else tema_actual["bg_frames"])
    frame_principal.configure(fg_color=tema_actual["bg_frames"])
    
    # Aplicar colores a los botones principales
    for boton in [button_archivo, button_edicion, button_visualizar, button_settings]:
        boton.configure(
            fg_color=tema_actual["bg_botones"],
            text_color=color_texto,
            hover_color=tema_actual["accent_hover"]
        )
    
    # Aplicar colores a las etiquetas principales
    for label in [label_archivo, label_edicion, label_visualizar, label_settings]:
        label.configure(
            fg_color=tema_actual["bg_secundario"],
            text_color=color_texto
        )
    
    # Aplicar colores a los elementos de configuración
    for name in [
        "label_cambiar_nombre", "label_cambiar_tema", "label_cambiar_idioma",
        "label_cambiar_tamano", "label_cambiar_color_menu", "label_cambiar_color_fuente",
        "label_cambiar_foto", "label_settings", "label_save_hint"
    ]:
        lbl = globals().get(name)
        if lbl:
            try:
                lbl.configure(
                    fg_color=tema_actual["bg_secundario"],
                    text_color=color_texto
                )
            except Exception:
                pass
    
    # Aplicar colores a los controles
    textbox_cambiar_nombre.configure(
        fg_color=tema_actual["bg_secundario"],
        text_color=color_texto,
        border_color=tema_actual["borde"]
    )
    # Asegurar que el entry de tamaño de fuente tome el mismo estilo que el resto
    try:
        entry_tamano_fuente.configure(
            fg_color=tema_actual["bg_secundario"],
            text_color=color_texto,
            border_color=tema_actual["borde"]
        )
    except Exception:
        pass
    
    # Aplicar estilo a botones de acento de forma unificada
    for accent_btn in [button_cambiar_foto, button_guardar_configuracion]:
        try:
            accent_btn.configure(
                fg_color=tema_actual["accent_color"],
                text_color=color_texto,
                hover_color=tema_actual["accent_hover"]
            )
        except Exception:
            pass
    
    for combobox in [combobox_cambiar_idioma, combobox_cambiar_tema, 
                     combobox_cambiar_fuente, combobox_cambiar_color_menu]:
        combobox.configure(
            fg_color=tema_actual["bg_secundario"],
            text_color=color_texto,
            border_color=tema_actual["borde"]
        )
    
    try:
        if 'label_nombre_usuario' in globals():
            label_nombre_usuario.configure(text_color=color_texto)
        # Aplicar la fuente actual a elementos principales
        for w in [button_archivo, button_edicion, button_visualizar, button_settings,
                  label_archivo, label_edicion, label_visualizar, label_settings,
                  label_cambiar_nombre, label_cambiar_tema, label_cambiar_idioma,
                  label_cambiar_tamano, label_cambiar_color_menu, label_cambiar_color_fuente, label_cambiar_foto,
                  label_save_hint, textbox_cambiar_nombre, entry_tamano_fuente, button_cambiar_foto,
                  button_guardar_configuracion, combobox_cambiar_idioma, combobox_cambiar_tema,
                  combobox_cambiar_color_menu, combobox_cambiar_fuente]:
            w.configure(font=ui_font)
    except Exception:
        pass

def cambiar_tema_seleccionado(tema_seleccionado):
    nombre_interno = temas.obtener_tema_por_nombre_display(tema_seleccionado)
    aplicar_tema_aplicacion(nombre_interno)

def _apply_translations():
    try:
        app.title(t("app_title"))
        button_archivo.configure(text=t("btn_open"))
        button_edicion.configure(text=t("btn_edit"))
        button_visualizar.configure(text=t("btn_view"))
        button_settings.configure(text=t("btn_settings"))
        label_archivo.configure(text=t("tab_file"))
        label_edicion.configure(text=t("tab_edit"))
        label_visualizar.configure(text=t("tab_view"))
        label_settings.configure(text=t("tab_settings"))
        label_cambiar_nombre.configure(text=t("settings_name"))
        label_cambiar_tema.configure(text=t("settings_theme"))
        label_cambiar_idioma.configure(text=t("settings_language"))
        label_cambiar_color_menu.configure(text=t("settings_menu_color"))
        label_cambiar_color_fuente.configure(text=t("settings_font_color"))
        label_cambiar_foto.configure(text=t("settings_profile_photo"))
        label_save_hint.configure(text=t("save_hint"))
        button_cambiar_foto.configure(text=t("btn_change_photo"))
        button_guardar_configuracion.configure(text=t("btn_save"))
        combobox_cambiar_idioma.configure(values=[t("lang_es"), t("lang_en")])
    except Exception:
        pass

#Variables
app = ctk.CTk()
app.geometry("600x600")
app.title("Gestión de preferencias")
ui_font = ctk.CTkFont(size=DEFAULT_FONT_SIZE)

#Funciones
def boton_archivo():
    label_archivo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    label_edicion.grid_remove()
    label_visualizar.grid_remove()
    borrar_objetos_frame_edicion()
    
def boton_edicion():
    label_archivo.grid_remove()
    label_edicion.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    label_visualizar.grid_remove()
    borrar_objetos_frame_edicion()

def boton_visualizar():
    label_archivo.grid_remove()
    label_edicion.grid_remove()
    label_visualizar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    borrar_objetos_frame_edicion()

def boton_settings():
    label_archivo.grid_remove()
    label_edicion.grid_remove()
    label_visualizar.grid_remove()
    mostrar_objetos_frame_edicion()

def almacenar_preferencias():
    with open("preferencias.json", "w") as archivo:
        json.dump(preferencias, archivo)

def cargar_preferencias():
    global preferencias
    try:
        with open("preferencias.json", "r") as archivo:
            preferencias = json.load(archivo)
        return True
    except FileNotFoundError:
        print("Archivo de preferencias no encontrado, usando valores por defecto")
        return False
    except json.JSONDecodeError:
        print("Error al leer preferencias, usando valores por defecto")
        return False


def actualizar_cambios():
    global preferencias
    
    # Obtener valores de los controles
    preferencias["nombre_usuario"] = textbox_cambiar_nombre.get("1.0", "end-1c") or "Usuario"
    preferencias["idioma"] = combobox_cambiar_idioma.get()
    preferencias["tema"] = temas.obtener_tema_por_nombre_display(combobox_cambiar_tema.get())
    # Tomar tamaño de fuente desde entry y reflejar en el input si no es válido
    raw_size = entry_tamano_fuente.get()
    parsed_size = parse_font_size(raw_size)
    preferencias["font_size"] = parsed_size
    if str(parsed_size) != str(raw_size).strip():
        try:
            entry_tamano_fuente.delete(0, 'end')
            entry_tamano_fuente.insert(0, str(parsed_size))
        except Exception:
            pass
    # Tamaño de fuente
    selected_color_name = combobox_cambiar_fuente.get()
    preferencias["color_fuente"] = COLOR_NAME_TO_HEX.get(
        selected_color_name,
        preferencias.get("color_fuente", "#ffffff")
    )
    selected_menu_color_name = combobox_cambiar_color_menu.get()
    preferencias["color_menu"] = COLOR_NAME_TO_HEX.get(
        selected_menu_color_name,
        preferencias.get("color_menu")
    )
    
    # Guardar en archivo
    almacenar_preferencias()
    # Actualizar fuente global y aplicar
    try:
        ui_font.configure(size=preferencias["font_size"])
    except Exception:
        ui_font.configure(size=DEFAULT_FONT_SIZE)
    aplicar_tema_aplicacion()
    # Refrescar label de nombre en el UI
    try:
        if 'label_nombre_usuario' in globals():
            label_nombre_usuario.configure(text=preferencias.get("nombre_usuario", "Usuario"))
        # Actualizar textos por cambio de idioma
        _apply_translations()
        # Aplicar tamaño de fuente si hay un control dedicado
        if 'entry_tamano_fuente' in globals():
            pass
    except Exception:
        pass

def cargar_foto_perfil():
    os.makedirs("foto_perfil", exist_ok=True)
    
    ruta_imagen = os.path.join("foto_perfil", "perfil.png")
    if os.path.exists(ruta_imagen):
        imagen = Image.open(ruta_imagen)
        foto_perfil_ctk = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(100, 100))
        return foto_perfil_ctk
    else:
        imagen_default = Image.new('RGB', (100, 100), color='gray')
        foto_perfil_ctk = ctk.CTkImage(light_image=imagen_default, dark_image=imagen_default, size=(100, 100))
        return foto_perfil_ctk

def seleccionar_foto_perfil():
    tipos_archivo = [
        ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
        ("PNG", "*.png"),
        ("JPEG", "*.jpg *.jpeg"),
        ("GIF", "*.gif"),
        ("BMP", "*.bmp"),
        ("Todos los archivos", "*.*")
    ]
    
    # Diálogo de selección 
    ruta_archivo = ctk.filedialog.askopenfilename(
        title=t("file_dialog_title"),
        filetypes=tipos_archivo,
        initialdir=os.getcwd()
    )
    
    if ruta_archivo:
        try:
            # Cargar la imagen seleccionada
            imagen = Image.open(ruta_archivo)
            
            # Guardar copia en el directorio de fotos de perfil
            ruta_destino = os.path.join("foto_perfil", "perfil.png")
            imagen.save(ruta_destino)
            
            # Actualizar la imagen en la interfaz
            global foto_perfil_ctk, label_foto
            foto_perfil_ctk = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(100, 100))
            
            # Actualizar el label si ya existe
            if 'label_foto' in globals():
                label_foto.configure(image=foto_perfil_ctk)
            else:
                # Crear nuevo label si no existe
                label_foto = ctk.CTkLabel(app, image=foto_perfil_ctk, text="")
                label_foto.pack(padx=10, pady=10)
                            
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

def borrar_objetos_frame_edicion():
    widgets = [
        label_cambiar_nombre, textbox_cambiar_nombre,
        label_cambiar_tamano, entry_tamano_fuente,
        label_cambiar_foto, button_cambiar_foto,
        label_cambiar_idioma, combobox_cambiar_idioma,
        label_cambiar_tema, combobox_cambiar_tema,
        label_cambiar_color_menu, combobox_cambiar_color_menu,
        label_cambiar_color_fuente, combobox_cambiar_fuente,
        label_save_hint, button_guardar_configuracion,
    ]
    for w in widgets:
        try:
            w.grid_remove()
        except Exception:
            pass

def mostrar_objetos_frame_edicion():
    frame_principal.grid_columnconfigure(0, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)
    
    for i in range(8): 
        frame_principal.grid_rowconfigure(i, weight=1)
    
    # Fila 0
    label_cambiar_nombre.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    textbox_cambiar_nombre.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    
    # Fila 1
    label_cambiar_tema.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    combobox_cambiar_tema.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Fila 2
    label_cambiar_idioma.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    combobox_cambiar_idioma.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Fila 3
    label_cambiar_tamano.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_tamano_fuente.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
    
    # Fila 4
    label_cambiar_color_menu.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    combobox_cambiar_color_menu.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
    
    # Fila 5
    label_cambiar_color_fuente.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    combobox_cambiar_fuente.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
    
    # Fila 6
    label_cambiar_foto.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    button_cambiar_foto.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

    # Fila 7
    label_save_hint.grid(row=7, column=0, padx=10, pady=5, sticky="w")
    button_guardar_configuracion.grid(row=7, column=1, padx=10, pady=5, sticky="ew")
    # Evitar foco persistente en el entry de tamaño
    try:
        frame_principal.focus_set()
    except Exception:
        pass
#Aplicación
    #Frames
frame_botones = ctk.CTkFrame(app, 550, 40, 10, 0, "transparent", None)
frame_foto = ctk.CTkFrame(app, 100, 100, 10, 0, "transparent", None)
frame_principal = ctk.CTkFrame(app, 550, 550, 10, 0, "transparent", None)

    #Botones Generales
button_archivo = ctk.CTkButton(frame_botones, 20, 20, 5, 0, 3, "transparent", "green", text=t("btn_open"))
button_edicion = ctk.CTkButton(frame_botones, 20, 20, 5, 0, 3, "transparent", "green", text=t("btn_edit"))
button_visualizar = ctk.CTkButton(frame_botones, 20, 20, 5, 0, 3, "transparent", "green", text=t("btn_view"))
button_settings = ctk.CTkButton(frame_botones, 20, 20, 5, 0, 3, "transparent", "green", text=t("btn_settings"))


    #Etiquetas Generales
label_archivo = ctk.CTkLabel(frame_principal, text=t("tab_file"), width=200, height=40, corner_radius=5)
label_edicion = ctk.CTkLabel(frame_principal, text=t("tab_edit"), width=200, height=40, corner_radius=5)
label_visualizar = ctk.CTkLabel(frame_principal, text=t("tab_view"), width=200, height=40, corner_radius=5)
label_settings = ctk.CTkLabel(frame_principal, text=t("tab_settings"), width=200, height=40, corner_radius=5)



    #Objetos Frame Edicion
label_cambiar_nombre = ctk.CTkLabel(frame_principal, text=t("settings_name"), width=200, height=40, corner_radius=5)
label_cambiar_tema = ctk.CTkLabel(frame_principal, text=t("settings_theme"), width=200, height=40, corner_radius=5)
label_cambiar_idioma = ctk.CTkLabel(frame_principal, text=t("settings_language"), width=200, height=40, corner_radius=5)
label_cambiar_tamano = ctk.CTkLabel(frame_principal, text=t("settings_font_size"), width=200, height=40, corner_radius=5)
label_cambiar_color_menu = ctk.CTkLabel(frame_principal, text=t("settings_menu_color"), width=200, height=40, corner_radius=5)
label_cambiar_color_fuente = ctk.CTkLabel(frame_principal, text=t("settings_font_color"), width=200, height=40, corner_radius=5)
label_cambiar_foto = ctk.CTkLabel(frame_principal, text=t("settings_profile_photo"), width=200, height=40, corner_radius=5)
label_save_hint = ctk.CTkLabel(frame_principal, text=t("save_hint"), width=200, height=40, corner_radius=5)

textbox_cambiar_nombre = ctk.CTkTextbox(frame_principal, width=200, height=40, corner_radius=5)
button_cambiar_foto = ctk.CTkButton(frame_principal, width=200, height=40, corner_radius=5, text=t("btn_change_photo"))
combobox_cambiar_idioma = ctk.CTkComboBox(frame_principal, width=200, height=40, corner_radius=5, values=[t("lang_es"), t("lang_en")])
combobox_cambiar_tema = ctk.CTkComboBox(frame_principal, width=200, height=40, corner_radius=5, values=temas.obtener_nombres_temas())
entry_tamano_fuente = ctk.CTkEntry(frame_principal, width=200, height=40, corner_radius=5)
combobox_cambiar_color_menu = ctk.CTkComboBox(
    frame_principal,
    width=200,
    height=40,
    corner_radius=5,
    values=[name for name, _ in COLOR_OPTIONS] + ["Personalizado"]
)
combobox_cambiar_fuente = ctk.CTkComboBox(
    frame_principal,
    width=200,
    height=40,
    corner_radius=5,
    values=[name for name, _ in COLOR_OPTIONS] + ["Personalizado"]
)

# Establecer valores por defecto
combobox_cambiar_idioma.set(t("lang_es"))
entry_tamano_fuente.insert(0, str(DEFAULT_FONT_SIZE))
combobox_cambiar_tema.set("Tema Oscuro")
combobox_cambiar_fuente.set(DEFAULT_COLOR_NAME)
combobox_cambiar_color_menu.set("Personalizado")

button_guardar_configuracion = ctk.CTkButton(frame_principal, width=200, height=40, corner_radius=5, text=t("btn_save"))

    #Establecer objetos
foto_perfil_ctk = cargar_foto_perfil()
# Mostrar foto de perfil y nombre de usuario
frame_foto_panel = ctk.CTkFrame(frame_botones, fg_color="transparent")
frame_foto_panel.pack(padx=10, pady=10, side="left", fill="both", expand=True)
label_foto = ctk.CTkLabel(frame_foto_panel, image=foto_perfil_ctk, text="")
label_foto.pack(padx=5, pady=(5, 0), side="top")
label_nombre_usuario = ctk.CTkLabel(frame_foto_panel, text="Usuario")
label_nombre_usuario.pack(padx=5, pady=(4, 5), side="top")

frame_botones.pack(padx=10, pady=10, fill="both")
frame_principal.pack(padx=10, pady=10, fill="both", expand=True)

frame_principal.grid_columnconfigure(0, weight=1)



button_archivo.pack(padx=10, pady=10, side="left", fill="x", expand=True)
button_edicion.pack(padx=10, pady=10, side="left", fill="x", expand=True)
button_visualizar.pack(padx=10, pady=10, side="left", fill="x", expand=True)
button_settings.pack(padx=10, pady=10, side="left", fill="x", expand=True)

# Configurar eventos
button_archivo.configure(command=boton_archivo)
button_edicion.configure(command=boton_edicion)
button_visualizar.configure(command=boton_visualizar)
button_settings.configure(command=boton_settings)
button_cambiar_foto.configure(command=seleccionar_foto_perfil)
button_guardar_configuracion.configure(command=actualizar_cambios)
combobox_cambiar_tema.configure(command=cambiar_tema_seleccionado)
combobox_cambiar_idioma.configure(command=lambda _: _apply_translations())

# Mostrar la primera etiqueta por defecto
label_archivo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Cargar preferencias guardadas
if cargar_preferencias():
    # Aplicar tema guardado
    if "tema" in preferencias:
        temas.cambiar_tema(preferencias["tema"])
        try:
            display_tema = temas.configurador.obtener_nombre_display(preferencias["tema"])  # tipo: ignore[attr-defined]
            if 'combobox_cambiar_tema' in globals():
                combobox_cambiar_tema.set(display_tema)
        except Exception:
            pass
    aplicar_tema_aplicacion()
    _apply_translations()
    
    # Aplicar otros valores guardados
    if "nombre_usuario" in preferencias:
        textbox_cambiar_nombre.insert("1.0", preferencias["nombre_usuario"])
        try:
            if 'label_nombre_usuario' in globals():
                label_nombre_usuario.configure(text=preferencias.get("nombre_usuario", "Usuario"))
        except Exception:
            pass
    if "idioma" in preferencias:
        combobox_cambiar_idioma.set(preferencias["idioma"])
    # Cargar tamaño de fuente guardado
    if "font_size" in preferencias:
        try:
            size = parse_font_size(preferencias["font_size"])
            entry_tamano_fuente.delete(0, 'end')
            entry_tamano_fuente.insert(0, str(size))
            ui_font.configure(size=size)
            aplicar_tema_aplicacion()
        except Exception:
            pass
    if "color_fuente" in preferencias:
        nombre_color = HEX_TO_COLOR_NAME.get(preferencias["color_fuente"].lower(), "Personalizado")
        combobox_cambiar_fuente.set(nombre_color)
    if "color_menu" in preferencias and preferencias["color_menu"]:
        try:
            nombre_menu = HEX_TO_COLOR_NAME.get(preferencias["color_menu"].lower(), "Personalizado")
            combobox_cambiar_color_menu.set(nombre_menu)
        except Exception:
            pass
else:
    # Aplicar tema por defecto
    aplicar_tema_aplicacion()
    _apply_translations()

app.mainloop()