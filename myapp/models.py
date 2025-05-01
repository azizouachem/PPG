
from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------------------------------
# UTILISATEUR PRINCIPAL (Unique) avec un champ role
# -----------------------------------------------------
class Utilisateur(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=100,)

    def __str__(self):
        return self.username


# -----------------------------------------------------
# CATEGORIE ET SOUS-CATEGORIE
# -----------------------------------------------------
class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class SousCategorie(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.categorie.nom} -> {self.nom}"


# -----------------------------------------------------
# ANNONCE
# -----------------------------------------------------
class Annonce(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expiree', 'Expirée'),
        ('supprimee', 'Supprimée'),
    )

    titre = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.FloatField()
    date_publication = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    ville = models.CharField(max_length=100)
    gouvernorat = models.CharField(max_length=100)
    images_urls = models.JSONField(default=list)
    is_premium = models.BooleanField(default=False)
    User = models.ForeignKey(Utilisateur, related_name='annonces', on_delete=models.CASCADE)
    sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre


# -----------------------------------------------------
# MESSAGE (Entre utilisateurs)
# -----------------------------------------------------
class Message(models.Model):
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    expediteur = models.ForeignKey(Utilisateur, related_name='messages_envoyes', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(Utilisateur, related_name='messages_recus', on_delete=models.CASCADE)
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)

    def __str__(self):
        return f"Message de {self.expediteur.username} à {self.destinataire.username}"


# -----------------------------------------------------
# OPTION PREMIUM (Pour mettre en avant une annonce)
# -----------------------------------------------------
class OptionPremium(models.Model):
    OPTION_CHOICES = (
        ('urgent', 'Urgent'),
        ('top', 'Top annonce'),
        ('couleur', 'Couleur mise en avant')
    )

    annonce = models.OneToOneField(Annonce, on_delete=models.CASCADE)
    type_option = models.CharField(max_length=20, choices=OPTION_CHOICES)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()

    def __str__(self):
        return f"{self.type_option} pour {self.annonce.titre}"


# -----------------------------------------------------
# PANIER ET PANIERANNONCE
# -----------------------------------------------------
class Panier(models.Model):
    acheteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=(('en cours', 'En cours'), ('confirme', 'Confirmé'), ('annule', 'Annulé')), default='en cours')

    def __str__(self):
        return f"Panier de {self.acheteur.username} ({self.statut})"


class PanierAnnonce(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.annonce.titre} dans le panier de {self.panier.acheteur.username}"