# Agro Site

**Projet Django pour l'agronomie**  
Ce site permet de proposer des conseils et formations en agronomie, vendre des matériels d'élevage, installer des incubateurs et des fermes, et offrir divers services liés à l'agriculture.

## Structure du site

1. **Accueil** : Présentation du site et logo.
2. **Conseils & Formations** : Blog éducatif avec articles sur l'agronomie.
3. **Boutique** : E-commerce avec catalogue de produits, panier et paiement.
4. **Services** : Installation de fermes, incubateurs, autres services.
5. **À propos** : Présentation de l’équipe et de la mission.
6. **Contact** : Formulaire de contact pour les visiteurs.

## Utilisateurs et permissions

- **Superadmin** : Accès complet à l’admin Django (`/admin/`).
- **Gestionnaires Agronomie** : Deux utilisateurs seulement, accès à un tableau de bord simplifié (`/dashboard/`) pour ajouter/modifier articles, produits et services.

## Installation

1. Cloner le projet :
```bash
git clone <lien-du-repo>
cd agro_site
