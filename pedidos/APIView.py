from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Max
from .models import Pedido


class LoginView(APIView):
    authentication_classes = [] 
    permission_classes = []   
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username
            })
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class StatsView(APIView):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
    
        def get(self, request):
            hoy = timezone.now().date()
            
            # 1. Órdenes de la fecha más reciente
            fecha_reciente = Pedido.objects.aggregate(ultima_fecha=Max('fecha_orden'))['ultima_fecha']
            ordenes_recientes = Pedido.objects.filter(
                fecha_orden__date=fecha_reciente
            ).count() if fecha_reciente else 0

            # 2. Total mensual (mes actual)
            inicio_mes = hoy.replace(day=1)
            ordenes_mensual = Pedido.objects.filter(
                fecha_orden__date__gte=inicio_mes
            ).count()

            # 3. Series diarias (últimos 30 días)
            fecha_limite = hoy - timedelta(days=30)
            ordenes_diarias = (Pedido.objects
                .filter(fecha_orden__date__gte=fecha_limite)
                .values('fecha_orden__date')
                .annotate(total=Count('orden_id'))
                .order_by('fecha_orden__date')
            )

            datos_diarios = [
                {
                    'fecha': item['fecha_orden__date'].strftime("%Y-%m-%d"),
                    'total': item['total']
                }
                for item in ordenes_diarias
            ]

            return Response({
                'ordenes_recientes': ordenes_recientes,
                'ordenes_mensual': ordenes_mensual,
                'series_diarias': datos_diarios
            })