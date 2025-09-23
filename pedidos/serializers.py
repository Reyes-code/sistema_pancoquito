from rest_framework import serializers

class MejorClienteSerializer(serializers.Serializer):
    cliente_id = serializers.IntegerField()
    cliente__nombre = serializers.CharField()
    total = serializers.IntegerField()
    
class StatsSerializer(serializers.Serializer):
    """Serializer principal para las estadísticas"""
    ordenes_hoy = serializers.IntegerField()
    ordenes_recientes = serializers.IntegerField()
    ordenes_mensual = serializers.IntegerField()
    fecha_reciente = serializers.DateField()
    mejores_clientes = MejorClienteSerializer(many=True)
    series_diarias = serializers.ListField()
    
    def get_fecha_reciente(self, obj):
        fecha = obj.get('fecha_reciente')
        return fecha.strftime("%Y-%m-%d") if fecha else None