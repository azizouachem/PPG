from django.urls import path
from .views import RegisterView,AnnonceCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from myapp.views import RegisterView,LoginView,DashboadView,ResetPasswordView,  AnnonceCreateView,CategorieCreateView, SousCategorieCreateView
from rest_framework.routers import DefaultRouter
from .views import AnnonceViewSet

router = DefaultRouter()
router.register(r'annonces', AnnonceViewSet, basename='annonce')

urlpatterns = [
 path('annonce/ajouter/', AnnonceCreateView.as_view(), name='ajouter_annonce'),
 ] + router.urls

urlpatterns = [
    path('auth/register/',RegisterView.as_view(),name="auth_register"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/login/',LoginView.as_view(),name="auth_login"),
    path('api/dashboard/',DashboadView.as_view(),name="dashboard"),
    path('api/auth/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('annonce/ajouter/', AnnonceCreateView.as_view(), name='ajouter_annonce'),
    path('categorie/ajouter/', CategorieCreateView.as_view(), name='ajouter_categorie'),
    path('sous-categorie/ajouter/', SousCategorieCreateView.as_view(), name='ajouter_sous_categorie'),

]
