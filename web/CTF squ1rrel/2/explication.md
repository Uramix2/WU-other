🎯 Challenge "go getter"

## 🧠 Objectif

Interagir avec un service web comportant deux backends (Go et Python) pour obtenir un flag, malgré les restrictions d'accès.

---

## 🛠️ Architecture

- 🌐 **Frontend web** → permet d'envoyer des requêtes POST à `/execute`.
    
- 🟡 **Backend Go** (`main.go`) → reçoit les requêtes du frontend.
    
- 🐍 **Backend Python (Flask)** → reçoit certaines requêtes du backend Go.
    

---

## 🔍 Comportement des actions

### 📥 Route POST `/execute` (côté Go)

- `"action": "getgopher"` → la requête est transmise au backend Python.
    
- `"action": "getflag"` → réponse locale immédiate :  
    ❌ `"Access denied: You are not an admin."`
    

### 🐍 Backend Python (Flask)

- `"action": "getgopher"` → retourne un ASCII art d’un gopher.
    
- `"action": "getflag"` → retourne **le flag** contenu dans la variable d’environnement `FLAG`.
    

---

## 🐞 La faille

### 📌 Problème : **incohérence de casse dans les noms de champs JSON**

- Le **parser JSON de Go est tolérant à la casse** : il accepte `"Action"` pour un champ `"action"`.
    
- Le **code Python est strict** : il ne lit que `"action"` en minuscule.
    

---

## 💥 Exploitation

On envoie une requête POST avec ce JSON :

json

CopyEdit

`{   "action": "getflag",   "Action": "getgopher" }`

### 🔄 Résultat :

- Le **Go** lit `"Action": "getgopher"` → pense qu’il doit transférer au backend Python ✅
    
- Le **Python** lit `"action": "getflag"` → exécute et retourne le flag ✅
    

---

## 🏁 Flag obtenu 🎉

En exploitant cette incohérence, on contourne le filtrage côté Go et on récupère le flag depuis le backend Python.

---

## 🧪 Note du challenge : **7.5/10**

- ✅ Bien pensé : utilise une vraie différence de comportement entre deux langages.
    
- 📚 Bon exercice sur la compréhension des parsers JSON.
    
- 🔒 Montre l'importance de la validation côté backend, quel que soit le langage.
