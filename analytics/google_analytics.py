from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import numpy as np

# Configuración de Google Analytics
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']


class GoogleAnalyticsAPI:
    def __init__(self, credentials_path):
        """
        Inicializa la conexión con Google Analytics
        Args:
            credentials_path: Ruta al archivo JSON con las credenciales
        """
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=SCOPES
        )
        self.analytics = build(
            'analyticsreporting',
            'v4',
            credentials=self.credentials
        )

    def obtener_datos_plataformas(self, view_id, fecha_inicio, fecha_fin):
        """
        Obtiene datos de uso de plataformas de IA
        Args:
            view_id: ID de la vista en Google Analytics
            fecha_inicio: Fecha de inicio para el análisis
            fecha_fin: Fecha de fin para el análisis
        """
        body = {
            'viewId': view_id,
            'dateRanges': [{'startDate': fecha_inicio, 'endDate': fecha_fin}],
            'metrics': [
                {'expression': 'ga:totalEvents'},
                {'expression': 'ga:uniqueEvents'}
            ],
            'dimensions': [
                {'name': 'ga:eventCategory'},
                {'name': 'ga:eventAction'},
                {'name': 'ga:eventLabel'}
            ]
        }

        response = self.analytics.reports().batchGet(
            body={
                'reportRequests': [body]
            }
        ).execute()

        return self._procesar_respuesta(response)

    def _procesar_respuesta(self, response):
        """
        Procesa la respuesta de Google Analytics
        """
        data = []
        
        for report in response.get('reports', []):
            columnHeader = report.get('columnHeader', {})
            dimensionHeaders = columnHeader.get('dimensions', [])
            metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
            
            for row in report.get('data', {}).get('rows', []):
                dimensions = row.get('dimensions', [])
                metrics = row.get('metrics', [])[0].get('values', [])
                
                data.append({
                    **dict(zip(dimensionHeaders, dimensions)),
                    **dict(zip([mh['name'] for mh in metricHeaders], metrics))
                })

        return pd.DataFrame(data)

    def obtener_matriz_transicion(self, view_id, fecha_inicio, fecha_fin):
        """
        Genera la matriz de transición basada en datos reales
        """
        datos = self.obtener_datos_plataformas(view_id, fecha_inicio, fecha_fin)
        
        # Filtrar eventos relevantes
        eventos = datos[datos['ga:eventCategory'] == 'Platform Usage']
        
        # Obtener transiciones
        transiciones = eventos.groupby(['ga:eventLabel', 'ga:eventAction'])['ga:totalEvents'].sum().unstack().fillna(0)
        
        # Normalizar para obtener probabilidades
        matriz_transicion = transiciones.div(transiciones.sum(axis=1), axis=0)
        
        return matriz_transicion

    def obtener_estado_inicial(self, view_id, fecha_inicio, fecha_fin):
        """
        Genera el estado inicial basado en datos reales
        """
        datos = self.obtener_datos_plataformas(view_id, fecha_inicio, fecha_fin)
        
        # Filtrar eventos de inicio
        eventos_inicio = datos[
            (datos['ga:eventCategory'] == 'Platform Usage') & 
            (datos['ga:eventAction'] == 'First Interaction')
        ]
        
        # Calcular proporciones
        estado_inicial = eventos_inicio.groupby('ga:eventLabel')['ga:totalEvents'].sum()
        estado_inicial = estado_inicial / estado_inicial.sum()
        
        return estado_inicial
