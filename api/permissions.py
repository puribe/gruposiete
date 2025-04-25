from rest_framework.permissions import BasePermission

class IsOrganizacionSectorial(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user and request.user.groups.filter(name='organizacion_sectorial').exists()
        except AttributeError:
            # Maneja el caso en que request.user sea None o no tenga el atributo 'groups'
            return False
        except Exception as e:
            # Manejo genérico de excepciones (puedes registrar el error si es necesario)
            return False

class IsOrganizacionSectorialOrAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user and (
                request.user.is_staff or request.user.groups.filter(name='organizacion_sectorial').exists()
            )
        except AttributeError:
            # Maneja el caso en que request.user sea None o no tenga el atributo 'groups'
            return False
        except Exception as e:
            # Manejo genérico de excepciones (puedes registrar el error si es necesario)
            return False