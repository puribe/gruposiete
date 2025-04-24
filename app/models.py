from django.db import models
from crum import get_current_user
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class ModeloBase(models.Model):
    """
    Clase base abstracta que añade campos de auditoría para registros.
    
    Campos:
    - created_at: Fecha y hora de creación del registro
    - updated_at: Fecha y hora de la última actualización
    - created_by: Usuario que creó el registro
    - updated_by: Usuario que realizó la última modificación
    
    Utiliza la librería 'crum' para obtener el usuario actual de forma automática.
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    # Campo para el usuario que creó el registro
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='%(class)s_created',
        null=True,
        blank=True
    )
    
    # Campo para el usuario que modificó el registro por última vez
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='%(class)s_updated',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
            self.updated_by = user
        super(ModeloBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True  # Indica que esta clase es abstracta

class TipoMedida(ModeloBase):
    """
    Representa un tipo de medida en el sistema. Puede ser regulatoria o no regulatoria.
    
    Atributos:
    - created_at: Fecha y hora de creación del registro
    - updated_at: Fecha y hora de la última actualización
    - created_by: Usuario que creó el registro
    - updated_by: Usuario que realizó la última modificación
    - nombre: Nombre del tipo de medida
    
    """
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Tipo de medida'
        verbose_name_plural = 'Tipos de medidas'

    def __str__(self):
        return f"{self.nombre}"

class Verificacion(ModeloBase):
    """
    Representa una verificación asociada a una medida. Contiene información sobre la
    verificación realizada.
    
    Atributos:
    - created_at: Fecha y hora de creación del registro
    - updated_at: Fecha y hora de la última actualización
    - created_by: Usuario que creó el registro
    - updated_by: Usuario que realizó la última modificación
    - nombre: Nombre de la verificación
    - verificacion: Texto descriptivo de la verificación
    
    """
    nombre = models.CharField(max_length=100, blank=True, null=True)
    verificacion = models.TextField(max_length=2000)

    class Meta:
        verbose_name = 'Verificación'
        verbose_name_plural = 'Verificaciones'

    def __str__(self):
        return f"{self.nombre} - {self.verificacion}"
    

    
    

FRECUENCIA = [
('ANUAL', 'Anual'),
('UNICA', 'Unica'),
('CADA_5_ANIOS', 'Cada 5 años'),
]

class Medida(ModeloBase):
    """
    Representa una medida asociada a un plan. Contiene información sobre la medida, su
    frecuencia de reporte y el organismo sectorial responsable.
    
    Atributos:
    - created_at: Fecha y hora de creación del registro
    - updated_at: Fecha y hora de la última actualización
    - created_by: Usuario que creó el registro
    - updated_by: Usuario que realizó la última modificación
    - referencia_pda: Referencia de la PDA asociada a la medida
    - nombre_corto: Nombre corto de la medida 
    - indicador: Indicador asociado a la medida
    - formula_de_calculo: Fórmula de cálculo asociada a la medida
    - frecuencia_reporte: Frecuencia de reporte de la medida (Anual, Única, Cada 5 años)
    - tipo_de_dato_a_validar: Tipo de dato a validar (opcional)
    - tipo_medida: Tipo de medida (regulatoria o no regulatoria)
    - plan: Plan al que está asociada la medida
    - organismo_sectorial: Organismo sectorial responsable de la medida
    - verificaciones: Verificaciones asociadas a la medida   
    
    """
    referencia_pda = models.CharField(max_length=100)
    nombre_corto = models.CharField(max_length=100) 
    indicador = models.TextField(max_length=2000) 
    formula_de_calculo = models.TextField(max_length=2000) 
    frecuencia_reporte = models.CharField(max_length=30, choices=FRECUENCIA, default='ANUAL')
    tipo_de_dato_a_validar = models.CharField(max_length=100, blank=True, null=True) 
    tipo_medida = models.ForeignKey('TipoMedida', models.CASCADE)
    plan = models.ForeignKey('Plan', models.CASCADE)
    organismo_sectorial = models.ForeignKey('OrganismoSectorial', models.CASCADE)
    verificaciones = models.ManyToManyField(Verificacion, through='VerificacionMedida')

    class Meta:
        verbose_name = 'Medida'
        verbose_name_plural = 'Medidas'

    def __str__(self):
        return f"{self.nombre_corto} - {self.frecuencia_reporte}"
    
class VerificacionMedida(models.Model):
    verificacion = models.ForeignKey('Verificacion', models.CASCADE)
    medida = models.ForeignKey('Medida', models.CASCADE)

    class Meta:
        verbose_name = 'Relación Verificación - medida'
        verbose_name_plural = 'Relación Verificación - medida'

class OrganismoSectorial(ModeloBase):
    """
    Representa un organismo sectorial responsable de la implementación de medidas.
    
    Atributos:
    - created_at: Fecha y hora de creación del registro
    - updated_at: Fecha y hora de la última actualización
    - created_by: Usuario que creó el registro
    - updated_by: Usuario que realizó la última modificación
    - nombre: Nombre del organismo sectorial  
    
    """    
    nombre = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Organismo Sectorial'
        verbose_name_plural = 'Organismos Sectoriales'
    
    def __str__(self):
        return f"{self.nombre}"
    
class Plan(ModeloBase):
    """
    Representa un plan asociado a un organismo sectorial. Contiene información sobre
    el plan, su estado de avance y los organismos sectoriales involucrados.
    
    Atributos:
    - created_at: Fecha y hora de creación del registro
    - updated_at: Fecha y hora de la última actualización
    - created_by: Usuario que creó el registro
    - updated_by: Usuario que realizó la última modificación
    - nombre: Nombre del plan
    - inicio: Fecha de inicio del plan
    - termino: Fecha de término del plan
    - estado_avance: Estado de avance del plan (opcional)
    - organismos: Relación muchos a muchos con los organismos sectoriales 
    
    """    
    nombre = models.CharField(max_length=255)
    inicio = models.DateTimeField(null=True)
    termino = models.DateTimeField(null=True)
    estado_avance = models.CharField(max_length=255, blank=True, null=True)
    organismos = models.ManyToManyField(OrganismoSectorial, through='OrganismoPlan')

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'
   
    def __str__(self):
        return f"{self.nombre}"
    
class OrganismoPlan(models.Model):
    organismo_sectorial = models.ForeignKey('OrganismoSectorial', models.CASCADE)
    plan = models.ForeignKey('Plan', models.CASCADE)

    class Meta:
        verbose_name = 'Relación Organismo - Plan'
        verbose_name_plural = 'Relación Organismo - Plan'
    
    def __str__(self):
        return f"{self.organismo_sectorial} - {self.plan}"


ESTADO_VERIFICACION = [
('VERIFICACION_PENDIENTE', 'Verificación pendiente'),
('VERIFICADA', 'Verificada'),
('RECHAZADA', 'Rechazada'),
]
class MedidaReportada(ModeloBase):
    """
    Representa una medida reportada por un organismo sectorial. Contiene información
    sobre la medida reportada, su estado y el organismo sectorial responsable.
    
    Atributos:
    - created_at: Fecha y hora de creación del registro
    - updated_at: Fecha y hora de la última actualización
    - created_by: Usuario que creó el registro
    - updated_by: Usuario que realizó la última modificación
    - organismo_sectorial: Organismo sectorial responsable de la medida reportada
    - medida: Medida asociada a la medida reportada
    - valor: Valor reportado de la medida
    - estado: Estado de la verificación de la medida reportada (pendiente, verificada, rechazada)
    
    
    """    
    organismo_sectorial = models.ForeignKey('OrganismoSectorial', models.CASCADE, help_text="Id del Organismo Sectorial que está informando.")
    medida = models.ForeignKey('Medida', models.CASCADE, help_text="Id de la medida a resportar.")
    valor = models.TextField(max_length=50, help_text="Resultado de la medida aplicada.")  
    estado = models.CharField(max_length=30, choices=ESTADO_VERIFICACION, default='VERIFICACION_PENDIENTE')

class CustomUser(AbstractUser):
    organismo_sectorial = models.ForeignKey(
        OrganismoSectorial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
