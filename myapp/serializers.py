from rest_framework import serializers
from .models import Utilisateur,Annonce, Categorie, SousCategorie
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id','username', 'email', 'password', 'telephone']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
    def create(self, validated_data):
        return Utilisateur.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            telephone=validated_data.get('telephone', ''),
            
        )
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_email(self, value):
        if not Utilisateur.objects.filter(email=value).exists():
            raise serializers.ValidationError("Aucun utilisateur trouvé avec cet email.")
        return value

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        
        user = Utilisateur.objects.get(email=email)
        user.set_password(new_password) 
        user.save()
        return user


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'nom']

class SousCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousCategorie
        fields = ['id', 'nom', 'categorie']

class AnnonceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Annonce
        fields = [
            'id',
            'titre',
            'description',
            'prix',
            'ville',
            'gouvernorat',
            'images_urls',
            'is_premium',
            'statut',
            'sous_categorie',
            'user',
        ]
        extra_kwargs = {
            'titre': {'required': True},
            'description': {'required': True},
            'prix': {'required': True},
            'ville': {'required': True},
            'gouvernorat': {'required': True},
            'images_urls': {'required': False},
            'sous_categorie': {'required': True},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        return Annonce.objects.create(user=user, **validated_data)
