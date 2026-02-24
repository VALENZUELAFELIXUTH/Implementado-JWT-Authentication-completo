from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from allauth.socialaccount.models import SocialAccount

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer personalizado con datos adicionales"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Agregar claims personalizados al token
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['full_name'] = f"{user.first_name} {user.last_name}"
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Agregar datos extra al response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'is_staff': self.user.is_staff,
            'date_joined': str(self.user.date_joined)
        }
        
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """Vista personalizada para obtener JWT"""
    serializer_class = CustomTokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def get_user_tokens(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    
    # Buscamos la cuenta de Google asociada al usuario
    social_account = SocialAccount.objects.filter(user=user, provider='google').first()
    
    # Extraemos la foto de los datos extra (si existen)
    picture_url = None
    if social_account and 'picture' in social_account.extra_data:
        picture_url = social_account.extra_data['picture']
    
    return JsonResponse({
        'message': 'Login exitoso con Google',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'picture': picture_url  # <--- Enviamos la URL al frontend
        }
    })