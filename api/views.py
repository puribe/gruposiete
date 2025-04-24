from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, schema 
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from app.models import OrganismoSectorial, OrganismoPlan, Plan, VerificacionMedida, Medida, Verificacion, TipoMedida , MedidaReportada
from .serializers import OrganismoSectorialSerializer, PlanSerializer, MedidaSerializer, VerificacionSerializer, TipoMedidaSerializer, MedidaReportadaSerializer

from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsOrganizacionSectorial, IsOrganizacionSectorialOrAdmin  # Importa el permiso personalizado


# Create your views here.

"""
viewsets.ModelViewSet:
Una clase predefinida de DRF que simplifica la creación de vistas CRUD (Create, Read,
Update, Delete). Es más eficiente que escribir vistas separadas para cada acción.
Es ideal para operaciones CRUD estándar porque minimiza la cantidad de código, pero permite personalización si es
necesario

queryset = x.objects.all() # Define qué datos se manejarán en los endpoints. Se incluyen todos en este caso
serializer_class = xSerializer #Conecta la vista con el serializer para que los datos se transformen correctamente a JSON y viceversa.
"""



@extend_schema_view(
    list=extend_schema(description='Retorna un listado de Organismos Sectoriales', summary='Lista Organismos'),
    retrieve=extend_schema(description='Retorna un Organismo Sectorial', summary='Obtiene uno en particular'),
    create=extend_schema(description='Crea un Organismo Sectorial',summary='Crear un Organismo'),
    update=extend_schema(description='Actualiza un Organismo Sectorial',summary='Actualiza un Organismo'),
    destroy=extend_schema(description='Elimina un Organismo Sectorial',summary='Elimina un Organismo'),
)
class OrganismoSectorialViewSet(viewsets.ModelViewSet):
    """
    API para gestionar organismos sectoriales. Permite crear, listar, actualizar y eliminar organismos.
    
    Metodos HTTP soportados:
    - GET: Listar todos los organismos o uno específico
    - POST: Crear un nuevo organismo
    - PUT: Actualizar un organismo existente
    - DELETE: Eliminar un organismo

    """    
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post','put','get','delete']
 
    queryset = OrganismoSectorial.objects.all() # Define qué datos se manejarán en los endpoints. Se incluyen todos en este caso
    serializer_class = OrganismoSectorialSerializer #Conecta la vista con el serializer para que los datos se transformen correctamente a JSON y viceversa.
 
 
    @action(detail=False, methods=['get']) #no es un detalle(o si no seria un listado) y responde a get
    def sin_medidas_informadas(self,request):
        return Response(status=status.HTTP_404_NOT_FOUND)
        #stock_minimo = request.query_params.get('stock_minimo',0)
        #productos=self.queryset.filter(stock__gte=stock_minimo)
        #organismos=self.queryset.filter(stock=0)
        #serializer = self.get_serializer(organismos, many=True) #son varios resultados o solo uno
        #return Response(serializer.data)

@extend_schema_view(
    list=extend_schema(description='Retorna un listado de Planes', summary='Lista Planes'),
    retrieve=extend_schema(description='Retorna un Plan', summary='Obtiene uno en particular'),
    create=extend_schema(description='Crea un Plan',summary='Crear un Plan'),
    update=extend_schema(description='Actualiza un Plan',summary='Actualiza un Plan'),
    destroy=extend_schema(description='Elimina un Plan',summary='Elimina un Plan'),
)
class PlanViewSet(viewsets.ModelViewSet):
    """
    API para gestionar planes. Permite crear, listar, actualizar y eliminar planes.
    
    Metodos HTTP soportados:
    - GET: Listar todos los planes o uno específico
    - POST: Crear un nuevo plan
    - PUT: Actualizar un plan existente
    - DELETE: Eliminar un plan

    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]
    http_method_names = ['post','put','get','delete']
    queryset = Plan.objects.all() # Define qué datos se manejarán en los endpoints. Se incluyen todos en este caso
    serializer_class = PlanSerializer #Conecta la vista con el serializer para que los datos se transformen correctamente a JSON y viceversa.


@extend_schema_view(
    list=extend_schema(description='Retorna un listado de Medidas', summary='Lista Medidas'),
    retrieve=extend_schema(description='Retorna una Medida', summary='Obtiene una en particular'),
    create=extend_schema(description='Crea una Medida',summary='Crear una Medida'),
    update=extend_schema(description='Actualiza una Medida',summary='Actualiza una Medida'),
    destroy=extend_schema(description='Elimina una Medida',summary='Elimina una Medida'),
)
class MedidaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar medidad. Permite crear, listar, actualizar y eliminar medidas.
    
    Metodos HTTP soportados:
    - GET: Listar todas las medidas o una específica
    - POST: Crear una nueva medida
    - PUT: Actualizar una medida existente
    - DELETE: Eliminar una medida

    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]
    http_method_names = ['post','put','get','delete']
    queryset = Medida.objects.all() # Define qué datos se manejarán en los endpoints. Se incluyen todos en este caso
    serializer_class = MedidaSerializer #Conecta la vista con el serializer para que los datos se transformen correctamente a JSON y viceversa.

@extend_schema_view(
    list=extend_schema(description='Retorna un listado de Verificaciones', summary='Lista Verificaciones'),
    retrieve=extend_schema(description='Retorna una Verificacion', summary='Obtiene una en particular'),
    create=extend_schema(description='Crea una Verificacion',summary='Crear una Verificacion'),
    update=extend_schema(description='Actualiza una Verificacion',summary='Actualiza una Verificacion'),
    destroy=extend_schema(description='Elimina una Verificacion',summary='Elimina una Verificacion'),
)
class VerificacionViewSet(viewsets.ModelViewSet):
    """
    API para gestionar verificaciones. Permite crear, listar, actualizar y eliminar verificaciones.
    
    Metodos HTTP soportados:
    - GET: Listar todas las verificaciones o una específica
    - POST: Crear una nueva verificacion
    - PUT: Actualizar una verificacion existente
    - DELETE: Eliminar una verificacion

    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]
    http_method_names = ['post','put','get','delete']
    queryset = Verificacion.objects.all() # Define qué datos se manejarán en los endpoints. Se incluyen todos en este caso
    serializer_class = VerificacionSerializer #Conecta la vista con el serializer para que los datos se transformen correctamente a JSON y viceversa.


@extend_schema_view(
    list=extend_schema(description='Retorna un listado de Tipos de Medidas', summary='Lista Tipos de Medidas'),
    retrieve=extend_schema(description='Retorna un Tipo de Medida', summary='Obtiene una en particular'),
    create=extend_schema(description='Crea un Tipo de Medida',summary='Crea un Tipo de Medida'),
    update=extend_schema(description='Actualiza un Tipo de Medida',summary='Actualiza un Tipo de Medida'),
    destroy=extend_schema(description='Elimina un Tipo de Medida',summary='Elimina un Tipo de Medida'),
)
class TipoMedidaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar tipos de medidas. Permite crear, listar, actualizar y eliminar medidas. 
    
    Metodos HTTP soportados:
    - GET: Listar todos los tipos de medidas o uno específico
    - POST: Crear un nuevo tipo de medida
    - PUT: Actualizar un tipo de medida existente
    - DELETE: Eliminar un tipo de medida

    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]
    http_method_names = ['post','put','get','delete']
    queryset = TipoMedida.objects.all() # Define qué datos se manejarán en los endpoints. Se incluyen todos en este caso
    serializer_class = TipoMedidaSerializer #Conecta la vista con el serializer para que los datos se transformen correctamente a JSON y viceversa.




@extend_schema_view(
    list=extend_schema(description='Retorna un listado de Medidas reportadas', summary='Lista Medidas Reportadas'),
    retrieve=extend_schema(description='Retorna una Medida Reportada', summary='Obtiene una en particular'),
    create=extend_schema(description='Permite crear un nuevo registro en la tabal de medidas reportadas',summary='Registra una medida aplicada'),
    update=extend_schema(description='Actualiza una Medida Reportada',summary='Actualiza una Medida Reportada'),
    destroy=extend_schema(description='Elimina una Medida Reportada',summary='Elimina una Medida Reportada'),
)


class MedidaReportadaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar medidas reportadas. Permite crear, listar, actualizar y eliminar medidas reportadas.
    
    metodos HTTP soportados:
    - GET: Listar todas las medidas reportadas o una específica
    - POST: Crear una nueva medida reportada
    - PUT: Actualizar una medida reportada existente
    - DELETE: Eliminar una medida reportada
    
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsOrganizacionSectorialOrAdmin]
    http_method_names = ['post','put','get','delete']
    queryset = MedidaReportada.objects.all() # Define qué datos se manejarán en los endpoints. Se incluyen todos en este caso
    serializer_class = MedidaReportadaSerializer #Conecta la vista con el serializer para que los datos se transformen correctamente a JSON y viceversa.





 