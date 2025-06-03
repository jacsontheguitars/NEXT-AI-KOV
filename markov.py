# markov/modelo.py

import numpy as np


class CadenasDeMarkov:
    def __init__(self, num_usuarios=100, num_usos=20):
        self.num_usuarios = num_usuarios
        self.num_usos = num_usos
        self.num_plataformas = 5
        self.plataformas = ['A', 'B', 'C', 'D', 'Otros']
        self.simulacion = np.empty((self.num_usuarios, self.num_usos), dtype='<U10')
        self.conteo_transiciones = np.zeros((self.num_plataformas, self.num_plataformas), dtype=int)

    def simular(self):
        np.random.seed()
        for i in range(self.num_usuarios):
            plataforma_anterior = np.random.randint(0, self.num_plataformas)
            for j in range(self.num_usos):
                plataforma_nueva = np.random.randint(0, self.num_plataformas)
                self.simulacion[i, j] = self.plataformas[plataforma_nueva]
                self.conteo_transiciones[plataforma_anterior, plataforma_nueva] += 1
                plataforma_anterior = plataforma_nueva

    def calcular_matriz_transicion(self):
        matriz_transicion = np.zeros((self.num_plataformas, self.num_plataformas), dtype=float)
        for i in range(self.num_plataformas):
            total = np.sum(self.conteo_transiciones[i])
            if total > 0:
                matriz_transicion[i] = self.conteo_transiciones[i] / total
        return matriz_transicion

    def calcular_estado_inicial(self):
        conteo_estado_inicial = np.zeros(self.num_plataformas, dtype=float)
        for i in range(self.num_usuarios):
            primer_estado = self.simulacion[i, 0]
            indice = self.plataformas.index(primer_estado)
            conteo_estado_inicial[indice] += 1
        return conteo_estado_inicial / self.num_usuarios

    def potencia_matriz(self, matriz, exponente):
        return np.linalg.matrix_power(matriz, exponente)

    def calcular_estado_largo_plazo(self, estado_inicial, matriz_transicion):
        matriz_potencia = self.potencia_matriz(matriz_transicion, self.num_usos)
        return np.dot(estado_inicial, matriz_potencia)
