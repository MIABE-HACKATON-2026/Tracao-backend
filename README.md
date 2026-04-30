# Tracao-Backend

Pour le test du projet il faudrait taper ces commandes là dans le terminal

### 1- Cloner le projet

Pour cloner,allez dans le dossier que vous voulez utiliser et faire :

```bash
git clone https://github.com/MIABE-HACKATON-2026/Tracao-backend.git
```

### 2- Créer un environnement virtuel ( s'assurer que python est préalablement installé )

Accédez au dossier Tracao-Backend ( ou le dossier où vous verrez le fichier requirements.txt ) et créer le venv

```bash
cd Tracao-backend

python -m venv venv ( Windows )

python3 -m venv venv ( Linux )
```

### 3- Activer le venv

```bash
venv/Scripts/activate ( Windows )

source venv/bin/activate ( Linux )
```

### 4- Installer les dépendances

S'assurer que vous êtes dans le dossier comportant le fichier requirements.txt

```bash
pip install -r requirements.txt
```

### 5- Faire des migrations

Accéder au dossier tracao/ et faire les migrations

```bash
cd tracao

python manage.py makemigrations

python manage.py migrate
```

### 6- Tester

Après les migrations, il faut tester

```bash

python manage.py runserver

```

Si tout a été bien fait,il n'y aura pas d'erreur.
Visiter le lien pour confirmer le fonctionnement ( habituellement **http://127.0.0.1:8000/** )

### 7- créer un compte admin

Pour se faire vous ferez : 

```bash

python manage.py createsuperuser

# on vous demandera de remplir les infos pour le compte

Email: ( mettre ce que vous voulez )
Password : ( mettre ce que vous voulez )

```

NB: En tapant le mot de passe, rien ne s'affiche pour des raisons de sécurité

En créant le super utilisateur, vous pouvez voir et tester toutes les fonctionnalités du site avec tous les droits.

Pour accéder à l'espace admin, allez sur **http://127.0.0.1:8000/admin**, mettez les identifiants et connectez-vous.

# 

Pour toute soumission d'inquiétude,vous pouvez nous joindre sur bchain2026@gmail.com.

Équipe B-chain MBH 2026.

