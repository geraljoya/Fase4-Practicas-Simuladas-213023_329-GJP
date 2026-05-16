# ---------------------------------------------------------
# Fase 4 - Componente Práctico - Prácticas simuladas
# Estudiante: Geraldine Joya Prieto
# Curso: Programación (213023)
# Código Fuente: problema1-sistema_gestion_clientes_reservas-GJP.py
# ---------------------------------------------------------

import tkinter as tk
from abc import ABC, abstractmethod
import logging
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DE LOGS 
# ==========================================
logging.basicConfig(
    filename='sistema_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# ==========================================
# 2. EXCEPCIONES PERSONALIZADAS
# ==========================================
class SistemaFJError(Exception):
    pass

class ClienteInvalidoError(SistemaFJError):
    pass

class ReservaError(SistemaFJError):
    pass

# ==========================================
# 3. CLASES ABSTRACTAS Y ENTIDADES
# ==========================================
class EntidadBase(ABC):
    def __init__(self, identificador):
        self._identificador = identificador
    
    @abstractmethod
    def mostrar_detalles(self):
        pass

class Cliente(EntidadBase):
    def __init__(self, identificador, nombre, correo):
        super().__init__(identificador)
        if not nombre or "@" not in correo:
            raise ClienteInvalidoError(f"Datos de cliente inválidos: {nombre} - {correo}")
        self.__nombre = nombre
        self.__correo = correo

    def mostrar_detalles(self):
        return f"Client: {self.__nombre} | ID: {self._identificador}"

class Servicio(EntidadBase):
    def __init__(self, identificador, nombre_servicio, tarifa_base):
        super().__init__(identificador)
        self.nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0.0):
        pass

class SalaReunion(Servicio):
    def calcular_costo(self, duracion, descuento=0.0):
        costo = (self.tarifa_base * duracion) 
        return costo - (costo * descuento)
    
    def mostrar_detalles(self):
        return f"[Room] {self.nombre_servicio} - ${self.tarifa_base}/hr"

class EquipoComputo(Servicio):
    def calcular_costo(self, duracion, descuento=0.0):
        costo = (self.tarifa_base * duracion) * 1.19 
        return costo - (costo * descuento)

    def mostrar_detalles(self):
        return f"[Equipment] {self.nombre_servicio} - ${self.tarifa_base}/hr (+TAX)"

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, duracion, descuento=0.0):
        costo = (self.tarifa_base * duracion) + 50 
        return costo - (costo * descuento)

    def mostrar_detalles(self):
        return f"[Consulting] {self.nombre_servicio} - ${self.tarifa_base}/hr (+$50 base)"

# ==========================================
# 4. GESTIÓN DE RESERVAS (try/except/else/finally)
# ==========================================
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDING"
        self.costo_total = 0

    def procesar(self):
        logging.info(f"Iniciando procesamiento de reserva para {self.cliente.mostrar_detalles()}")
        try:
            if self.duracion <= 0:
                raise ValueError("La duración debe ser mayor a 0 horas.")
            self.costo_total = self.servicio.calcular_costo(self.duracion)
            
        except ValueError as e:
            logging.error(f"Error de validación: {str(e)}")
            self.estado = "FAILED"
            raise ReservaError("Fallo al crear la reserva debido a datos ilógicos.") from e
            
        except Exception as e:
            logging.critical(f"Error crítico en el sistema: {str(e)}")
            self.estado = "FAILED"
            
        else:
            self.estado = "CONFIRMED"
            logging.info(f"Reserva CONFIRMADA. Costo: ${self.costo_total:.2f}")
            return f"✅ SUCCESS: {self.servicio.nombre_servicio} booked for {self.duracion}h. Total: ${self.costo_total:.2f}"
            
        finally:
            logging.info(f"Finalizado el intento de reserva. Estado final: {self.estado}")

# ==========================================
# 5. INTERFAZ GRÁFICA Y SIMULADOR
# ==========================================
class SoftwareFJApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Reservation Engine")
        self.root.geometry("900x650")
        self.root.configure(bg="#1A1A1A")
        
        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.root, text="SOFTWARE FJ - DIAGNOSTIC & LOGS", font=("Helvetica", 18, "bold"), bg="#1A1A1A", fg="#57CC99").pack(pady=20)
        
        btn_run = tk.Label(self.root, text="▶ RUN 10 SIMULATIONS (TEST SUITE)", bg="#57CC99", fg="#1A1A1A", font=("Helvetica", 12, "bold"), padx=20, pady=10, cursor="hand2")
        btn_run.bind("<Button-1>", lambda e: self.ejecutar_simulaciones())
        btn_run.pack(pady=10)

        frame_console = tk.Frame(self.root, bg="#2C2C2C", padx=2, pady=2)
        frame_console.pack(fill="both", expand=True, padx=30, pady=20)
        
        self.console = tk.Text(frame_console, bg="#0A0A0A", fg="#FFFFFF", font=("Consolas", 10), padx=15, pady=15, highlightthickness=0)
        self.console.pack(fill="both", expand=True)
        
        self.console.tag_config("info", foreground="#A0A0A0")
        self.console.tag_config("success", foreground="#57CC99")
        self.console.tag_config("error", foreground="#FF8383")
        self.console.tag_config("title", foreground="#5D9CEC", font=("Consolas", 11, "bold"))
        
        self.console.insert(tk.END, ">> System Ready. Waiting to execute test suite...\n\n", "info")

    def log_to_ui(self, message, tag="info"):
        self.console.insert(tk.END, message + "\n", tag)
        self.console.see(tk.END)
        self.root.update()

    def ejecutar_simulaciones(self):
        self.console.delete(1.0, tk.END)
        self.log_to_ui(">> INITIATING 10 BATCH OPERATIONS (NO DATABASE MODE)...\n", "title")
        
        servicios_disponibles = [
            SalaReunion("S01", "Boardroom A", 100),
            EquipoComputo("E01", "MacBook Pro M3", 50),
            AsesoriaEspecializada("A01", "Cloud Architecture", 150)
        ]

        casos_prueba = [
            {"desc": "1. Cliente válido y reserva de Sala", "cli": ("C1", "Geraldine", "gery@mail.com"), "srv": servicios_disponibles[0], "dur": 3},
            {"desc": "2. Cliente válido y alquiler equipo", "cli": ("C2", "Andy", "andy@mail.com"), "srv": servicios_disponibles[1], "dur": 24},
            {"desc": "3. ERROR: Correo de cliente inválido", "cli": ("C3", "Juan", "juanmail.com"), "srv": servicios_disponibles[2], "dur": 2},
            {"desc": "4. ERROR: Reserva con duración negativa", "cli": ("C4", "Maria", "maria@mail.com"), "srv": servicios_disponibles[0], "dur": -5},
            {"desc": "5. Cliente válido y asesoría compleja", "cli": ("C5", "Carlos", "car@mail.com"), "srv": servicios_disponibles[2], "dur": 4},
            {"desc": "6. ERROR: Nombre de cliente vacío", "cli": ("C6", "", "test@mail.com"), "srv": servicios_disponibles[1], "dur": 5},
            {"desc": "7. Reserva de Sala (Corta duración)", "cli": ("C7", "Ana", "ana@mail.com"), "srv": servicios_disponibles[0], "dur": 1},
            {"desc": "8. ERROR: Duración en cero", "cli": ("C8", "Luis", "luis@mail.com"), "srv": servicios_disponibles[1], "dur": 0},
            {"desc": "9. Alquiler de equipo prolongado", "cli": ("C9", "Pedro", "pedro@mail.com"), "srv": servicios_disponibles[1], "dur": 48},
            {"desc": "10. Asesoría rápida", "cli": ("C10", "Sofia", "sofia@mail.com"), "srv": servicios_disponibles[2], "dur": 1},
        ]

        for i, caso in enumerate(casos_prueba):
            self.log_to_ui(f"--- Operation {caso['desc']} ---", "info")
            try:
                cliente = Cliente(*caso['cli'])
                reserva = Reserva(cliente, caso['srv'], caso['dur'])
                resultado = reserva.procesar()
                self.log_to_ui(resultado, "success")
                
            except ClienteInvalidoError as e:
                self.log_to_ui(f"❌ CUSTOM ERROR CAUGHT: {str(e)}", "error")
                logging.warning(f"Simulacion {i+1} fallida - Cliente Invalido: {str(e)}")
                
            except ReservaError as e:
                causa_original = e.__cause__
                self.log_to_ui(f"❌ RESERVATION ERROR CAUGHT: {str(e)}", "error")
                self.log_to_ui(f"   ↳ Root cause: {str(causa_original)}", "error")
                
            except Exception as e:
                self.log_to_ui(f"❌ UNEXPECTED CRITICAL ERROR: {str(e)}", "error")
                
            self.log_to_ui("")

        self.log_to_ui(">> BATCH OPERATIONS COMPLETED. ALL ERRORS HANDLED GRACEFULLY.", "title")
        self.log_to_ui(">> System remained stable. Check 'sistema_fj.log' for backend registry.", "info")

if __name__ == "__main__":
    root = tk.Tk()
    app = SoftwareFJApp(root)
    root.mainloop()