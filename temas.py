from configurador_temas import ConfiguradorTemas

class TemasColores:
    def __init__(self):
        self.configurador = ConfiguradorTemas()
        self.tema_actual = "tema_oscuro"
    
    def obtener_tema(self, nombre_tema=None):
        if nombre_tema:
            return self.configurador.obtener_colores_tema(nombre_tema)
        return self.configurador.obtener_colores_tema(self.tema_actual)
    
    def cambiar_tema(self, nombre_tema):
        if nombre_tema in self.configurador.obtener_lista_temas():
            self.tema_actual = nombre_tema
            return True
        return False
    
    def obtener_color(self, nombre_color):
        tema = self.obtener_tema()
        return tema.get(nombre_color, "#000000")
    
    def obtener_nombres_temas(self):
        return self.configurador.obtener_nombres_display()
    
    def obtener_tema_por_nombre_display(self, nombre_display):
        return self.configurador.obtener_tema_por_nombre_display(nombre_display)

