import pygame
import time
import random
import os  # Es útil para verificar la existencia de archivos de forma explícita.

# Código de Santiago Restrepo Salazar.

# Como jugar
# Flechas: Mueven la serpiente (Izquierda, Derecha, Arriba, Abajo)
# Comida: Verde +1 punto, Rojo -1 punto, Amarillo +2 puntos
# Extras: Aparece 1 obstáculo cada 10 puntos y cada 5 puntos aumenta tu velocidad de forma permanente.
# Condición de pérdida: Tocar los bordes, tocar un obstáculo, chocarse con sí mismo.

# Inicializar pygame
pygame.init()

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (213, 50, 80)
verde = (0, 255, 0)
amarillo = (255, 215, 0)
gris = (100, 100, 100)  

# Dimensiones de la ventana del juego
ancho = 600
alto = 400

# Configuración de la pantalla del juego
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Juego Snake en Python')

reloj = pygame.time.Clock()

tamaño_bloque = 10
velocidad_inicial = 10  # Velocidad inicial ajustada para una experiencia de juego balanceada

# Fuentes para mostrar texto en la pantalla
fuente = pygame.font.SysFont(None, 35)
fuente_puntaje = pygame.font.SysFont(None, 25)

# Ruta para guardar los mejores puntajes
archivo_puntajes = "mejor_puntaje.txt"

# Clase que representa la comida en el juego
class Comida:
    def __init__(self):
        self.generar_comida()  # Genera una posición inicial para la comida

    def generar_comida(self):
        # Generar una posición aleatoria para la comida y definir su tipo
        self.x = round(random.randrange(0, ancho - tamaño_bloque) / 10.0) * 10.0
        self.y = round(random.randrange(0, alto - tamaño_bloque) / 10.0) * 10.0
        self.tipo = random.choice(['normal', 'roja', 'amarilla'])

    def mostrar(self):
        # Dibujar la comida en la pantalla según su tipo (normal, roja o amarilla)
        if self.tipo == 'normal':
            pygame.draw.rect(pantalla, verde, [self.x, self.y, tamaño_bloque, tamaño_bloque])
        elif self.tipo == 'roja':
            pygame.draw.rect(pantalla, rojo, [self.x, self.y, tamaño_bloque, tamaño_bloque])
        elif self.tipo == 'amarilla':
            pygame.draw.rect(pantalla, amarillo, [self.x, self.y, tamaño_bloque, tamaño_bloque])

# Clase que representa a la serpiente del juego
class Serpiente:
    def __init__(self):
        self.longitud = 1  # Longitud inicial de la serpiente
        self.lista = [[ancho / 2, alto / 2]]  # Lista de posiciones de la serpiente, iniciando en el centro
        self.velocidad = velocidad_inicial  
        self.incremento_velocidad = 0  # Incremento de velocidad basado en el crecimiento

    def mover(self, x_cambio, y_cambio):
        cabeza = [self.lista[0][0] + x_cambio, self.lista[0][1] + y_cambio]
        self.lista.insert(0, cabeza) 
        if len(self.lista) > self.longitud:
            self.lista.pop()  

    def crecer(self, puntos=1):
        # Aumenta la longitud de la serpiente según los puntos obtenidos
        self.longitud = max(1, self.longitud + puntos)  # Asegurar que la longitud mínima sea 1.
        self.incremento_velocidad += puntos

    def dibujar(self):
        # Dibujar cada segmento de la serpiente en la pantalla
        for segmento in self.lista:
            pygame.draw.rect(pantalla, blanco, [segmento[0], segmento[1], tamaño_bloque, tamaño_bloque])

    def colisiona_con(self, x, y):
        # Verificar si la cabeza de la serpiente colisiona con las coordenadas dadas (comida)
        return self.lista[0][0] == x and self.lista[0][1] == y

    def verifica_colision(self, ancho, alto):
        # Verificar colisiones con los bordes de la pantalla o consigo misma
        cabeza = self.lista[0]
        # Colisión con los bordes de la ventana
        if cabeza[0] >= ancho or cabeza[0] < 0 or cabeza[1] >= alto or cabeza[1] < 0:
            return True
        # Colisión con el cuerpo de la serpiente
        return cabeza in self.lista[1:]

# Clase principal 
class Juego:
    def __init__(self):
        self.serpiente = Serpiente()  
        self.comida = Comida()  
        self.comida_extra = None  # Segunda comida para acompañar a la roja
        self.tiempo_comida_roja = 0  # Tiempo de aparición de la comida roja
        self.mejor_puntaje = self.cargar_mejor_puntaje()  # Carga el mejor puntaje desde archivo
        self.game_over = False
        self.game_close = False
        self.x_cambio = 0  
        self.y_cambio = 0  
        self.x_obstaculo, self.y_obstaculo = None, None  # Posición del obstáculo (si existe)
        self.tiempo_obstaculo = 0  # Tiempo de aparición del obstáculo

    def cargar_mejor_puntaje(self):
        # Cargar el mejor puntaje desde un archivo, o devolver 0 si no existe
        if not os.path.exists(archivo_puntajes):
            with open(archivo_puntajes, "w") as f:
                f.write("0")
            return 0

        with open(archivo_puntajes, "r") as f:
            return int(f.read().strip())

    def guardar_mejor_puntaje(self, puntaje):
        # Guardar el puntaje actual como mejor puntaje si es mayor que el guardado
        if puntaje > self.mejor_puntaje:
            with open(archivo_puntajes, "w") as f:
                f.write(str(puntaje))

    def mostrar_puntaje(self):
        # Mostrar el puntaje actual y el mejor puntaje en la pantalla
        texto = fuente_puntaje.render(f"Puntaje: {self.serpiente.longitud - 1}  Mejor puntaje: {self.mejor_puntaje}", True, blanco)
        pantalla.blit(texto, [10, 10])

    def mensaje(self, msg, color, y_offset=0):
        # Mostrar un mensaje en el centro de la pantalla con un desplazamiento vertical opcional
        texto = fuente.render(msg, True, color)
        pantalla.blit(texto, [ancho / 6, alto / 3 + y_offset])

    def incrementar_velocidad(self):
        # Aumentar la velocidad cada 5 crecimientos de la serpiente para hacer el juego más difícil
        if self.serpiente.incremento_velocidad >= 5:
            self.serpiente.velocidad += 1
            self.serpiente.incremento_velocidad = 0

    def procesar_eventos(self):
        # Manejar los eventos de teclado y cerrar ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                # Cambiar la dirección de la serpiente solo si no es la dirección opuesta
                if event.key == pygame.K_LEFT and self.x_cambio == 0:
                    self.x_cambio = -tamaño_bloque
                    self.y_cambio = 0
                elif event.key == pygame.K_RIGHT and self.x_cambio == 0:
                    self.x_cambio = tamaño_bloque
                    self.y_cambio = 0
                elif event.key == pygame.K_UP and self.y_cambio == 0:
                    self.y_cambio = -tamaño_bloque
                    self.x_cambio = 0
                elif event.key == pygame.K_DOWN and self.y_cambio == 0:
                    self.y_cambio = tamaño_bloque
                    self.x_cambio = 0

    def actualizar_juego(self):
        # Actualizar la posición de la serpiente y verificar colisiones
        self.serpiente.mover(self.x_cambio, self.y_cambio)

        # Si la serpiente colisiona con un obstáculo, el juego termina
        if self.x_obstaculo and self.y_obstaculo:
            if self.serpiente.colisiona_con(self.x_obstaculo, self.y_obstaculo):
                self.game_close = True

        # Si la serpiente come la comida
        if self.serpiente.colisiona_con(self.comida.x, self.comida.y):
            puntos = 1 if self.comida.tipo == 'normal' else -1 if self.comida.tipo == 'roja' else 2
            self.serpiente.crecer(puntos)
            self.incrementar_velocidad()  # Ajustar la velocidad si es necesario.
            self.comida.generar_comida()
            
            # Si la comida es roja, generar una comida extra y un temporizador
            if self.comida.tipo == 'roja':
                self.comida_extra = Comida()
                while self.comida_extra.tipo == 'roja':
                    self.comida_extra.generar_comida()  # Asegurarse de que no sea roja
                self.tiempo_comida_roja = time.time()

            # Generar un obstáculo cada 10 puntos para incrementar la dificultad
            if (self.serpiente.longitud - 1) % 10 == 0:
                self.x_obstaculo = round(random.randrange(0, ancho - tamaño_bloque) / 10.0) * 10.0
                self.y_obstaculo = round(random.randrange(0, alto - tamaño_bloque) / 10.0) * 10.0
                self.tiempo_obstaculo = time.time()

        # Controlar la desaparición de la comida roja y su extra tras 5 segundos
        if self.comida.tipo == 'roja' and time.time() - self.tiempo_comida_roja > 5:
            self.comida.generar_comida()
            self.comida_extra = None

        # Si la serpiente come la comida extra
        if self.comida_extra and self.serpiente.colisiona_con(self.comida_extra.x, self.comida_extra.y):
            puntos = 1 if self.comida_extra.tipo == 'normal' else 2
            self.serpiente.crecer(puntos)
            self.incrementar_velocidad()  # Ajustar la velocidad si es necesario.
            self.comida_extra = None

    def dibujar_elementos(self):
        # Dibujar todos los elementos del juego: serpiente, comida, y comida extra si existe
        pantalla.fill(negro)
        self.serpiente.dibujar()
        self.comida.mostrar()
        if self.comida_extra:
            self.comida_extra.mostrar()
        self.mostrar_puntaje()

        # Dibujar el obstáculo si está presente
        if self.x_obstaculo and self.y_obstaculo:
            pygame.draw.rect(pantalla, gris, [self.x_obstaculo, self.y_obstaculo, tamaño_bloque, tamaño_bloque])

        pygame.display.update()

    def ejecutar(self):
        # Ciclo principal del juego
        while not self.game_over:
            self.procesar_eventos()
            self.actualizar_juego()

            # Verificar colisiones y condiciones de fin de juego
            if self.serpiente.verifica_colision(ancho, alto):
                self.game_close = True

            # Mostrar pantalla de fin del juego si la serpiente colisiona
            while self.game_close:
                pantalla.fill(negro)
                self.mensaje(f"Perdiste! Tu puntaje fue: {self.serpiente.longitud - 1}", rojo, -30)
                self.mensaje("Presiona C para continuar o Q para salir", blanco, 30)
                self.mostrar_puntaje()
                pygame.display.update()
                self.guardar_mejor_puntaje(self.serpiente.longitud - 1)

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.game_over = True
                            self.game_close = False
                        if event.key == pygame.K_c:
                            # Reiniciar el juego al presionar "C"
                            self.__init__()
                            self.ejecutar()

            self.dibujar_elementos()
            reloj.tick(self.serpiente.velocidad)  

        pygame.quit()
        quit()

# Iniciar el juego si se ejecuta como script principal
if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()
