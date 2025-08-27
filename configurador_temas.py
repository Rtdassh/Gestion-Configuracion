import json
import os
from typing import Dict, List

class ConfiguradorTemas:
    def __init__(self, archivo_temas="temas_colores.json"):
        self.archivo_temas = archivo_temas
        self.temas = self.cargar_temas()
    
    def cargar_temas(self) -> Dict:
        # Cargar temas por defecto desde código
        base = self.crear_temas_por_defecto()
        # Si existe JSON, lo usamos como overrides/añadidos
        if os.path.exists(self.archivo_temas):
            try:
                with open(self.archivo_temas, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return self._merge_temas(base, data)
            except json.JSONDecodeError:
                print(f"Error al leer {self.archivo_temas}, usando temas por defecto del código")
                return base
        else:
            # No hay archivo: trabajar solo con los temas por defecto del código
            return base

    def _merge_temas(self, base: Dict, overrides: Dict) -> Dict:

        resultado = {k: v.copy() for k, v in base.items()}
        for nombre_tema, tema_override in overrides.items():
            if nombre_tema in resultado:
                tema_base = resultado[nombre_tema]
                # Sobrescribir metadatos si existen
                if "nombre" in tema_override:
                    tema_base["nombre"] = tema_override["nombre"]
                if "descripcion" in tema_override:
                    tema_base["descripcion"] = tema_override["descripcion"]
                # Fusionar colores
                colores_base = tema_base.get("colores", {})
                colores_override = tema_override.get("colores", {})
                colores_base.update(colores_override)
                tema_base["colores"] = colores_base
                resultado[nombre_tema] = tema_base
            else:
                # Tema nuevo definido en JSON
                resultado[nombre_tema] = tema_override
        return resultado
    
    def crear_temas_por_defecto(self) -> Dict:
        temas_default = {
            "tema_claro": {
                "nombre": "Tema Claro",
                "descripcion": "Tema claro con colores suaves",
                "colores": {
                    "bg_principal": "#f5f7fa",
                    "bg_secundario": "#ffffff",
                    "bg_botones": "#e6eef7",
                    "bg_frames": "#f0f4f8",
                    "texto_principal": "#111827",
                    "texto_secundario": "#4b5563",
                    "accent_color": "#2563eb",
                    "accent_hover": "#3b82f6",
                    "borde": "#cbd5e1",
                    "error": "#dc2626",
                    "exito": "#16a34a",
                    "advertencia": "#d97706"
                }
            },
            "tema_oscuro": {
                "nombre": "Tema Oscuro",
                "descripcion": "Tema oscuro estándar",
                "colores": {
                    "bg_principal": "#1e1e1e",
                    "bg_secundario": "#2d2d2d",
                    "bg_botones": "#3d3d3d",
                    "bg_frames": "#252525",
                    "texto_principal": "#ffffff",
                    "texto_secundario": "#cccccc",
                    "accent_color": "#007acc",
                    "accent_hover": "#005a9e",
                    "borde": "#404040",
                    "error": "#ff6666",
                    "exito": "#66cc66",
                    "advertencia": "#ffcc00"
                }
            },
            "tema_azul": {
                "nombre": "Tema Azul",
                "descripcion": "Tema con tonos azules y cian",
                "colores": {
                    "bg_principal": "#1a1a2e",
                    "bg_secundario": "#16213e",
                    "bg_botones": "#0f3460",
                    "bg_frames": "#1a1a2e",
                    "texto_principal": "#ffffff",
                    "texto_secundario": "#a8a8a8",
                    "accent_color": "#4ecdc4",
                    "accent_hover": "#45b7aa",
                    "borde": "#2d3748",
                    "error": "#ff6b6b",
                    "exito": "#4ecdc4",
                    "advertencia": "#ffeaa7"
                }
            },
            "tema_verde": {
                "nombre": "Tema Verde",
                "descripcion": "Tema con tonos verdes",
                "colores": {
                    "bg_principal": "#1a1a1a",
                    "bg_secundario": "#2d2d2d",
                    "bg_botones": "#4a6741",
                    "bg_frames": "#252525",
                    "texto_principal": "#ffffff",
                    "texto_secundario": "#cccccc",
                    "accent_color": "#7cb342",
                    "accent_hover": "#689f38",
                    "borde": "#404040",
                    "error": "#f44336",
                    "exito": "#4caf50",
                    "advertencia": "#ff9800"
                }
            }
        }
        return temas_default
    
    def guardar_temas(self):
        try:
            with open(self.archivo_temas, 'w', encoding='utf-8') as f:
                json.dump(self.temas, f, indent=4, ensure_ascii=False)
            print(f"Temas guardados en {self.archivo_temas}")
            return True
        except Exception as e:
            print(f"Error al guardar temas: {e}")
            return False
    
    def obtener_tema(self, nombre_tema: str) -> Dict:
        return self.temas.get(nombre_tema, {})
    
    def obtener_lista_temas(self) -> List[str]:
        return list(self.temas.keys())
    
    def obtener_nombres_display(self) -> List[str]:
        return [self.temas[tema]["nombre"] for tema in self.temas.keys()]
    
    def obtener_tema_por_nombre_display(self, nombre_display: str) -> str:
        for nombre_interno, tema in self.temas.items():
            if tema["nombre"] == nombre_display:
                return nombre_interno
        return "tema_oscuro"  # Tema por defecto
    
    def modificar_color_tema(self, nombre_tema: str, nombre_color: str, nuevo_color: str):
        if nombre_tema in self.temas:
            if nombre_color in self.temas[nombre_tema]["colores"]:
                self.temas[nombre_tema]["colores"][nombre_color] = nuevo_color
                return True
            else:
                return False
        else:
            return False
    
    def crear_nuevo_tema(self, nombre_tema: str, nombre_display: str, descripcion: str, colores: Dict):
        if nombre_tema in self.temas:
            return False
        
        self.temas[nombre_tema] = {
            "nombre": nombre_display,
            "descripcion": descripcion,
            "colores": colores
        }
        return True
    
    def eliminar_tema(self, nombre_tema: str):
        temas_protegidos = ["tema_claro", "tema_oscuro"]
        if nombre_tema in temas_protegidos:
            return False
        
        if nombre_tema in self.temas:
            del self.temas[nombre_tema]
            return True
        else:
            return False
    
    def obtener_colores_tema(self, nombre_tema: str) -> Dict:
        tema = self.obtener_tema(nombre_tema)
        return tema.get("colores", {})
    
    def obtener_nombre_display(self, nombre_tema: str) -> str:
        tema = self.obtener_tema(nombre_tema)
        return tema.get("nombre", nombre_tema)
