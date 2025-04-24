from rest_framework import serializers
from app.models import OrganismoSectorial, OrganismoPlan, Plan, VerificacionMedida, Medida, Verificacion, TipoMedida, MedidaReportada
from django.utils import timezone
from datetime import datetime


class OrganismoSectorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganismoSectorial
        fields = '__all__'
    
    def validate_nombre(self, value): #
        """
        Validar que el nombre del organismo sectorial no esté vacío y tenga un formato adecuado.
        """
        if not value.strip():
            raise serializers.ValidationError("El nombre del organismo no puede estar vacío.")
        
        if len(value) < 3:
            raise serializers.ValidationError("El nombre del organismo debe tener al menos 3 caracteres.")
        
        return value


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
    
    def validate_nombre(self, value):
        """
        Validar que el nombre del plan no esté vacío y tenga un formato adecuado.
        """
        if not value.strip():
            raise serializers.ValidationError("El nombre del plan no puede estar vacío.")
        
        return value
    
    def validate(self, data):
        """
        Validar que la fecha de inicio sea anterior a la fecha de término.
        """
        inicio = data.get('inicio')
        termino = data.get('termino')
        
        if inicio and termino and inicio >= termino:
            raise serializers.ValidationError({"termino": "La fecha de término debe ser posterior a la fecha de inicio."})
        
        return data


class TipoMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMedida
        fields = '__all__'
    
    def validate_nombre(self, value):
        """
        Validar que el nombre del tipo de medida no esté vacío.
        """
        if not value.strip():
            raise serializers.ValidationError("El nombre del tipo de medida no puede estar vacío.")
        
        return value


class VerificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verificacion
        fields = '__all__'
    
    def validate_verificacion(self, value):
        """
        Validar que el texto de verificación no esté vacío y tenga un contenido mínimo.
        """
        if not value.strip():
            raise serializers.ValidationError("El texto de verificación no puede estar vacío.")
        
        if len(value) < 10:
            raise serializers.ValidationError("El texto de verificación debe tener al menos 10 caracteres.")
        
        return value


class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = '__all__'
    
    def validate_referencia_pda(self, value):
        """
        Validar que la referencia PDA tenga un formato adecuado.
        """
        if not value.strip():
            raise serializers.ValidationError("La referencia PDA no puede estar vacía.")
        
        return value
    
    def validate_nombre_corto(self, value):
        """
        Validar que el nombre corto no esté vacío.
        """
        if not value.strip():
            raise serializers.ValidationError("El nombre corto no puede estar vacío.")
        
        return value
    
    def validate_indicador(self, value):
        """
        Validar que el indicador no esté vacío.
        """
        if not value.strip():
            raise serializers.ValidationError("El indicador no puede estar vacío.")
        
        return value
    
    def validate_formula_de_calculo(self, value):
        """
        Validar que la fórmula de cálculo no esté vacía.
        """
        if not value.strip():
            raise serializers.ValidationError("La fórmula de cálculo no puede estar vacía.")
        
        return value
    
    def validate(self, data):
        """
        Validaciones a nivel de objeto para Medida.
        """
        # Verificar que el organismo sectorial corresponda al plan
        plan = data.get('plan')
        organismo = data.get('organismo_sectorial')
        
        if plan and organismo:
            # Verificar si existe la relación entre plan y organismo
            if not OrganismoPlan.objects.filter(plan=plan, organismo_sectorial=organismo).exists():
                raise serializers.ValidationError(
                    {"organismo_sectorial": "El organismo sectorial no está asociado a este plan."}
                )
        
        return data


class MedidaReportadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedidaReportada
        fields = '__all__'
    
    def validate_valor(self, value):
        """
        Validar que el valor reportado no esté vacío.
        """
        if not value.strip():
            raise serializers.ValidationError("El valor reportado no puede estar vacío.")
        
        return value
    
    def validate(self, data):
        """
        Validaciones a nivel de objeto para MedidaReportada.
        """
        medida = data.get('medida')
        organismo = data.get('organismo_sectorial')
        
        # Verificar que la medida reportada corresponda al organismo sectorial asignado
        if medida and organismo and medida.organismo_sectorial.id != organismo.id:
            raise serializers.ValidationError(
                {"medida": "Esta medida no corresponde al organismo sectorial indicado."}
            )
        
        # Si la medida es de frecuencia UNICA, verificar que no existan reportes previos
        if medida and medida.frecuencia_reporte == 'UNICA':
            # Excluir el ID actual en caso de actualización
            instance_id = getattr(self.instance, 'id', None)
            filter_kwargs = {'medida': medida}
            if instance_id:
                filter_kwargs['id__ne'] = instance_id
                
            if MedidaReportada.objects.filter(**filter_kwargs).exists():
                raise serializers.ValidationError(
                    {"medida": "Esta medida es de tipo ÚNICA y ya ha sido reportada anteriormente."}
                )
        
        # Validar el estado de verificación según reglas de negocio
        estado = data.get('estado')
        if estado == 'VERIFICADA' and self.context.get('request') and not self.context['request'].user.is_staff:
            raise serializers.ValidationError(
                {"estado": "Solo los administradores pueden marcar una medida como verificada."}
            )
        
        return data
