
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from .serializers import UtilisateurSerializer
from .models import Annonce,Utilisateur, Categorie, SousCategorie,Panier,PanierAnnonce
from .serializers import AnnonceSerializer,LoginSerializer ,UtilisateurSerializer,ResetPasswordSerializer,ResetPasswordSerializer, CategorieSerializer, SousCategorieSerializer,PanierSerializer,AnnoncePanierSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

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
    

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Mot de passe réinitialisé avec succès."}, status=200)
        return Response(serializer.errors, status=400)

class AnnonceViewSet(viewsets.ModelViewSet):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE'] and obj.user != request.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à modifier cette annonce.")
        return True

class AnnonceListView(ListAPIView):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer
    permission_classes = [IsAuthenticated]

class AnnonceCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnnonceSerializer

    def get(self, request):
        return Response({"message": "Utilisez POST pour créer une annonce."})

    def post(self, request):
        print("Authentifié :", request.user.is_authenticated)
        print("Type utilisateur :", type(request.user))
        print("Est Utilisateur personnalisé :", isinstance(request.user, Utilisateur))
        serializer = AnnonceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            annonce = serializer.save()
            return Response(AnnonceSerializer(annonce).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnnoncesParCategorieView(APIView):
    def get(self, request, categorie_id):
        annonces = Annonce.objects.filter(sous_categorie__categorie__id=categorie_id)
        serializer = AnnonceSerializer(annonces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategorieCreateView(generics.CreateAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [AllowAny]

class CategorieListView(generics.ListAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [AllowAny]

class CategorieUpdateView(generics.UpdateAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [AllowAny]

class CategorieDeleteView(generics.DestroyAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [AllowAny]

class SousCategorieUpdateView(generics.UpdateAPIView):
    queryset = SousCategorie.objects.all()
    serializer_class = SousCategorieSerializer
    permission_classes = [AllowAny]

class SousCategorieListView(generics.ListAPIView):
    queryset = SousCategorie.objects.all()
    serializer_class = SousCategorieSerializer
    permission_classes = [AllowAny]

class SousCategorieCreateView(generics.CreateAPIView):
    queryset = SousCategorie.objects.all()
    serializer_class = SousCategorieSerializer
    permission_classes = [AllowAny]

class SousCategorieDeleteView(generics.DestroyAPIView):
    queryset = SousCategorie.objects.all()
    serializer_class = SousCategorieSerializer
    permission_classes = [AllowAny]

#une méthode pour filtrer les sous-catégories par catégorie(à utiliser pour ajouter une annonce)
class SousCategoriesParCategorie(APIView):
    def get(self, request, categorie_id):
        sous_categories = SousCategorie.objects.filter(categorie_id=categorie_id)
        serializer = SousCategorieSerializer(sous_categories, many=True)
        return Response(serializer.data)
    
class FilteredAnnoncesView(generics.ListAPIView):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['sous_categorie', 'sous_categorie__categorie']  # filtres exacts
    search_fields = ['titre', 'description']  # recherche texte
    permission_classes = [AllowAny]
    
class AjouterAnnonceAuPanierView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, annonce_id):
        try:
            annonce = Annonce.objects.get(id=annonce_id)
        except Annonce.DoesNotExist:
            return Response({'error': 'Annonce introuvable.'}, status=404)

        # Récupérer ou créer un panier pour l'utilisateur
        panier, created = Panier.objects.get_or_create(
            acheteur=request.user,
            statut='en cours'
        )

        # Vérifier si l'annonce est déjà dans le panier
        if PanierAnnonce.objects.filter(panier=panier, annonce=annonce).exists():
            return Response({'detail': 'Annonce déjà dans le panier.'}, status=400)

        # Ajouter l'annonce au panier
        PanierAnnonce.objects.create(panier=panier, annonce=annonce)

        return Response({'detail': 'Annonce ajoutée au panier.'}, status=201)



class PanierDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Chercher ou créer le panier de l'utilisateur
        panier, created = Panier.objects.get_or_create(acheteur=request.user, statut='en cours')

        # Récupérer les annonces dans le panier
        lignes = PanierAnnonce.objects.filter(panier=panier).select_related('annonce')
        annonces = [ligne.annonce for ligne in lignes]

        # Serializer les annonces
        serialized = AnnoncePanierSerializer(annonces, many=True)

        # Calculer le prix total
        total = sum([annonce.prix for annonce in annonces])

        return Response({
            'annonces': serialized.data,
            'prix_total': total
        })
