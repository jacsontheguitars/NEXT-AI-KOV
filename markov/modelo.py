import numpy as np
import pandas as pd

class CadenasDeMarkovIA:
    def __init__(self, num_usuarios=100, num_usos=20):
        """
        Inicializa el modelo de cadenas de Markov para plataformas de IA
        
        Args:
            num_usuarios (int): Número de usuarios a simular
            num_usos (int): Número de interacciones por usuario
        """
        self.num_usuarios = num_usuarios
        self.num_usos = num_usos

        # Plataformas de IA
        self.plataformas = [
            'Anthropic',
            'Bard',
            'ChatGPT',
            'Claude',
            'Gemini'
        ]

        self.num_plataformas = len(self.plataformas)
        self.simulacion = np.empty(
            (self.num_usuarios, self.num_usos),
            dtype='<U10'
        )
        self.conteo_transiciones = np.zeros(
            (self.num_plataformas, self.num_plataformas),
            dtype=int
        )

        # Matrices calculadas
        self._matriz_transicion = None
        self._estado_inicial = None
        self._estado_largo_plazo = None

    def calcular_matriz_transicion(self):
        """
        Calcula la matriz de transición
        """
        matriz_transicion = np.zeros(
            (self.num_plataformas, self.num_plataformas),
            dtype=float
        )
        
        for i in range(self.num_plataformas):
            total = np.sum(self.conteo_transiciones[i])
            if total > 0:
                matriz_transicion[i] = self.conteo_transiciones[i] / total
        
        return matriz_transicion

    def calcular_estado_inicial(self):
        """
        Calcula el estado inicial
        """
        conteo_estado_inicial = np.zeros(self.num_plataformas, dtype=float)
        for i in range(self.num_usuarios):
            primer_estado = self.simulacion[i, 0]
            indice = self.plataformas.index(primer_estado)
            conteo_estado_inicial[indice] += 1
        return conteo_estado_inicial / self.num_usuarios

    def calcular_estado_largo_plazo(self):
        """
        Calcula el estado a largo plazo
        """
        matriz_transicion = self.calcular_matriz_transicion()
        estado_inicial = self.calcular_estado_inicial()
        
        # Usamos una potencia alta para representar "largo plazo"
        matriz_potencia = np.linalg.matrix_power(matriz_transicion, 100)
        return np.dot(estado_inicial, matriz_potencia)

    def generar_conclusion(self):
        """
        Genera una conclusión basada en las matrices
        """
        if self._matriz_transicion is None or self._estado_largo_plazo is None:
            raise ValueError("Debe simular datos primero")

        matriz_transicion = self._matriz_transicion
        estado_largo_plazo = self._estado_largo_plazo

        # Plataforma más popular a largo plazo
        plataforma_popular = self.plataformas[np.argmax(estado_largo_plazo)]
        probabilidad = estado_largo_plazo.max()

        conclusion = (
            f"Basado en el análisis, la plataforma más utilizada a largo plazo es {plataforma_popular} "
            f"con una probabilidad de {probabilidad:.2f}. Las transiciones más comunes son:"
        )

        # Transiciones más comunes
        for i in range(self.num_plataformas):
            for j in range(self.num_plataformas):
                if matriz_transicion[i, j] > 0.2:
                    conclusion += (
                        f"\n- De {self.plataformas[i]} a {self.plataformas[j]}: "
                        f"{matriz_transicion[i, j]:.2f}"
                    )

        return conclusion

    def formatear_matriz(self, matriz, tipo='transicion'):
        """
        Formatea la matriz para mejor visualización
        """
        if tipo == 'transicion':
            return pd.DataFrame(
                np.round(matriz, 2),
                index=self.plataformas,
                columns=self.plataformas
            ).style.format("{:.2f}")
        elif tipo == 'inicial' or tipo == 'largo':
            return pd.DataFrame(
                [np.round(matriz, 2)],
                columns=self.plataformas
            ).style.format("{:.2f}")

    def _calcular_probabilidades_transicion(self, plataforma_actual):
        """
        Calcula las probabilidades de transición desde la plataforma actual
        """
        # Probabilidades base
        probabilidades = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
        
        # Aumenta la probabilidad de quedarse en la misma plataforma
        probabilidades[plataforma_actual] += 0.3
        
        # Aumenta la probabilidad de transición entre plataformas similares
        if plataforma_actual in [0, 1]:  # Anthropic o Bard
            probabilidades[[0, 1]] += 0.1
        elif plataforma_actual in [2, 3, 4]:  # ChatGPT, Claude o Gemini
            probabilidades[[2, 3, 4]] += 0.1
        
        # Normaliza las probabilidades
        return probabilidades / np.sum(probabilidades)

    def simular(self):
        """
        Simula el comportamiento de usuarios entre diferentes plataformas de IA
        """
        np.random.seed()
        for i in range(self.num_usuarios):
            # Elige la primera plataforma
            plataforma_anterior = np.random.choice(range(self.num_plataformas))

            for j in range(self.num_usos):
                # Simula la transición a la siguiente plataforma
                # Las transiciones son más probables entre plataformas similares
                probabilidades = self._calcular_probabilidades_transicion(plataforma_anterior)
                plataforma_nueva = np.random.choice(
                    range(self.num_plataformas),
                    p=probabilidades
                )

                self.simulacion[i, j] = self.plataformas[plataforma_nueva]
                self.conteo_transiciones[plataforma_anterior, plataforma_nueva] += 1
                plataforma_anterior = plataforma_nueva

        # Recalcular las matrices después de la simulación
        self._recalcular_matrices()

    def _recalcular_matrices(self):
        """
        Recalcula todas las matrices después de la simulación
        """
        self._matriz_transicion = self.calcular_matriz_transicion()
        self._estado_inicial = self.calcular_estado_inicial()
        self._estado_largo_plazo = self.calcular_estado_largo_plazo()


