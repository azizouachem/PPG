from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from .serializers import UtilisateurSerializer
from .models import Annonce,Utilisateur, Categorie, SousCategorie
from .serializers import AnnonceSerializer,LoginSerializer ,UtilisateurSerializer,ResetPasswordSerializer,   ResetPasswordSerializer, CategorieSerializer, SousCategorieSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            return Response({'detail': 'Email ou mot de passe invalide.'}, status=401)

        if not user.check_password(password):
            return Response({'detail': 'Email ou mot de passe invalide.'}, status=401)
        
        refresh = RefreshToken.for_user(user)
        user_serializer = UtilisateurSerializer(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_serializer.data
        })
            
class DashboadView(APIView):
    permission_classes = [IsAuthenticated]
        
    def get(self, request):
        user = request.user
        user_serializer = UtilisateurSerializer(user)
        return Response({
            'message': 'Welcome to dashboard',
            'user' : user_serializer.data
        }, 200)
    
class AnnonceCreateView(APIView):
    #permission_classes = [IsAuthenticated]  

    def post(self, request):
        serializer = AnnonceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vendeur=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]  

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Mot de passe réinitialisé avec succès."}, status=200)
        return Response(serializer.errors, status=400)

class AnnonceCreateView(APIView):
    def get(self, request):
        return Response({"message": "Utilisez POST pour créer une annonce."})

    def post(self, request):
        serializer = AnnonceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            annonce = serializer.save()
            return Response(AnnonceSerializer(annonce).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategorieCreateView(generics.CreateAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    #permission_classes = [IsAuthenticated]

class SousCategorieCreateView(generics.CreateAPIView):
    queryset = SousCategorie.objects.all()
    serializer_class = SousCategorieSerializer
    #permission_classes = [IsAuthenticated]