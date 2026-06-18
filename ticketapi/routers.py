from rest_framework.routers import DefaultRouter
import copy

class AllowUpdateOnListRouter(DefaultRouter):
    def get_routes(self, viewset):
        routes = super().get_routes(viewset)
        # Faz uma cópia profunda para não modificar as rotas globais por engano
        routes = copy.deepcopy(routes)
        
        # Procura a rota de lista (raiz) e adiciona put/patch mapeados para 'update'
        for route in routes:
            if route.name == '{basename}-list':
                route.mapping.update({
                    'put': 'update',
                    'patch': 'partial_update' # O DRF usa partial_update internamente para o PATCH
                })
        return routes