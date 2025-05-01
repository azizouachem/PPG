from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Categorie, SousCategorie, Annonce, Message, OptionPremium, Panier, PanierAnnonce

class UtilisateurAdmin(UserAdmin):
    model = Utilisateur
    list_display = ['username', 'email', 'telephone', 'role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('telephone', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('telephone', 'role')}),
    )

admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Categorie)
admin.site.register(SousCategorie)
admin.site.register(Annonce)
admin.site.register(Message)
admin.site.register(OptionPremium)
admin.site.register(Panier)
admin.site.register(PanierAnnonce)
