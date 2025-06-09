from django.urls import path
from .views import RegisterView,AnnonceCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name="auth_register"),
    path('auth/login/', LoginView.as_view(), name="auth_login"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/', DashboadView.as_view(), name="dashboard"),
    path('api/auth/reset-password/', ResetPasswordView.as_view(), name='reset_password'),

    # Annonce
    path('annonce/ajouter/', AnnonceCreateView.as_view(), name='ajouter_annonce'),
    path('annonces/', AnnonceListView.as_view(), name='annonce-list'),
    path('annonces/categorie/<int:categorie_id>/', AnnoncesParCategorieView.as_view(), name='annonces-par-categorie'),
    path('annonces/filter/', FilteredAnnoncesView.as_view(), name='filtered-annonces'),

    # Catégorie CRUD
    path('categorie/ajouter/', CategorieCreateView.as_view(), name='ajouter_categorie'),
    path('categories/', CategorieListView.as_view(), name='liste_categories'),
    path('categorie/modifier/<int:pk>/', CategorieUpdateView.as_view(), name='modifier_categorie'),
    path('categorie/supprimer/<int:pk>/', CategorieDeleteView.as_view(), name='supprimer_categorie'),

    # Sous-catégorie CRUD
    path('sous-categorie/ajouter/', SousCategorieCreateView.as_view(), name='ajouter_sous_categorie'),
    path('sous-categories/', SousCategorieListView.as_view(), name='liste_sous_categories'),
    path('sous-categorie/modifier/<int:pk>/', SousCategorieUpdateView.as_view(), name='modifier_sous_categorie'),
    path('sous-categorie/supprimer/<int:pk>/', SousCategorieDeleteView.as_view(), name='supprimer_sous_categorie'),
    path('api/sous-categories/<int:categorie_id>/', SousCategoriesParCategorie.as_view(), name='sous-categories-par-categorie'),

    #panier
    path('panier/ajouter/<int:annonce_id>/', AjouterAnnonceAuPanierView.as_view(), name='ajouter_au_panier'),
    path('panier/', PanierDetailView.as_view(), name='afficher_panier'),


]
