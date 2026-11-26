<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: MIT
-->

# hostcensus

[![CI](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/ci.yml)
[![Docker](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/docker-build.yml/badge.svg)](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/docker-build.yml)
[![Release workflow](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/release.yml/badge.svg)](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/release.yml)
[![Latest published release](https://img.shields.io/github/v/release/somethingwithproof/python-network-discovery-tool?label=published%20release)](https://github.com/somethingwithproof/python-network-discovery-tool/releases)
[![Bandit](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/bandit.yml/badge.svg)](https://github.com/somethingwithproof/python-network-discovery-tool/actions/workflows/bandit.yml)
[![Python compatibility](https://img.shields.io/badge/Python-3.12%E2%80%933.14-blue)](./.github/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/python-network-discovery-tool/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/15324/badge)](https://www.bestpractices.dev/en/projects/15324)
[![Strict typing](https://img.shields.io/badge/mypy-strict-blue)](./pyproject.toml)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · **Français (Maroc)** · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus est un outil CLI en Python dédié à l'inventaire reproductible des services sur les réseaux que vous administrez.
Il enregistre ce que les équipements exposent, compare les observations dans le temps et génère
des scripts d'importation Kadupul. Le backend par défaut utilise des sockets asyncio sans privilèges root ;
la découverte Nmap optionnelle permet d'identifier des hôtes au-delà des ports de services configurés.

## Pourquoi hostcensus

Un rapport de ports ponctuel ne permet pas de savoir si l'observation suivante a changé ou
a simplement échoué. hostcensus combine des états de service explicites, des sondes bornées, des profils
de scan réutilisables et un historique local. Les opérateurs peuvent répéter le même périmètre, inspecter
les erreurs et distinguer les observations incertaines des changements confirmés.

- **Preuves de service :** identification SSH, bannières d'accueil MySQL, en-têtes HTTP,
  observations de certificats TLS, ainsi que la découverte SNMP ou des requêtes authentifiées sur la MIB système.
- **Périmètre reproductible :** profils TOML nommés, exclusions cumulatives, services
  configurables, plafonds d'hôtes/de sondes et workers bornés.
- **Vérifications avant tout trafic :** le contrôle préalable local valide les cibles, les outils, l'accès
  aux destinations, le schéma d'historique et les bundles CA TLS configurés.
- **Historique d'inventaire :** les instantanés SQLite transactionnels conservent toutes les observations ;
  les comparaisons gardent visibles les échecs du scanner et les états inconnus.
- **Sorties interopérables :** rapports terminal, JSON et CSV, instantanés de fichiers versionnés
  et scripts d'importation Kadupul.

La CI couvre Python 3.12, 3.13 et 3.14 sous Linux et macOS, ainsi qu'un laboratoire d'intégration
Compose maîtrisé. Le code utilise des alias de types modernes, des résultats de contrôle préalable typés,
des profils à slots avec arguments nommés uniquement et un nettoyage asynchrone structuré tout en conservant ces
versions d'exécution. Consultez [Gestion des versions et publications](../../../docs/releasing.md) pour le contrat
de compatibilité SemVer et le processus de publication GitHub. Le badge de version décrit
les artefacts publiés et non la copie de travail : le dernier tag publié est actuellement
`v0.3.0`, tandis que cette copie de travail utilise la version de paquet `3.0.0`. Installez depuis la copie
de travail pour profiter des fonctionnalités d'inventaire documentées ici.

Commencez par [l'installation](#install), puis par [les profils et l'historique](#inventory-profiles-preflight-and-local-history).
Pour les détails d'intégration, consultez [les empreintes de services](#fingerprints),
[les comparaisons de fichiers](#inventory-diff) et [l'export Kadupul](#kadupul-export).

## Installation

Python 3.12 ou une version ultérieure est requis ; la matrice testée couvre Python 3.12 à 3.14. Depuis cette
copie de travail, installez les dépendances d'exécution verrouillées :

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Pour la découverte d'hôtes optionnelle avec Nmap, installez l'exécutable Nmap via le gestionnaire de paquets
de votre plateforme ; aucun paquet Python supplémentaire n'est nécessaire. La sortie XML de Nmap est analysée
avec defusedxml, une dépendance principale, ce qui bloque l'expansion d'entités. hostcensus lance
directement le binaire `nmap` présent dans `PATH` avec une liste d'arguments fixe, une échéance qui évolue
selon la taille du préfixe et une limite de sortie de 64 Mio. Nmap n'est pas nécessaire pour le backend par défaut.

## Migration depuis netprobe

hostcensus est le nouveau nom de netprobe, publié en version 3.0.0. Le projet n'a jamais été
publié sur PyPI sous aucun des deux noms ; les installations proviennent donc d'une copie de travail ou d'une
release GitHub. Le dépôt GitHub conserve son nom.

| Auparavant | Maintenant | Compatibilité |
| --- | --- | --- |
| Distribution `netprobe` | `hostcensus` | Réinstallez depuis la copie de travail ; il n'existe pas de paquet sous l'ancien nom. |
| Commande `netprobe` | `hostcensus` | `netprobe` fonctionne toujours et affiche une ligne de dépréciation sur stderr. Les codes de sortie et stdout restent inchangés. Suppression prévue dans la prochaine version majeure. |
| Variables d'environnement `NETPROBE_*` | `HOSTCENSUS_*` | Une variable `NETPROBE_*` est utilisée lorsque son équivalent `HOSTCENSUS_*` n'est pas défini, avec un avertissement sur stderr citant les noms des variables et jamais leurs valeurs. `HOSTCENSUS_*` prévaut lorsque les deux sont définies. Suppression prévue dans la prochaine version majeure. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Rupture de compatibilité.** Aucune couche de compatibilité d'import n'est installée ; mettez à jour vos imports. |
| Tag d'image Docker `network-discovery:test` (CI uniquement) et utilisateur de conteneur `netprobe` | `hostcensus:test`, utilisateur `hostcensus` | Aucune image n'a jamais été publiée sur un registre. Reconstruisez l'image et utilisez le point d'entrée `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Un fichier existant portant l'ancien nom par défaut continue d'être utilisé, avec un avertissement, tant que le nouveau nom n'existe pas. Les chemins explicites `--config` et `--history` ne sont pas affectés. |
| Rapports et instantanés avec `"format": "netprobe-report"` ou `"netprobe-snapshot"`, ainsi que le champ `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` et `export` chargent toujours les fichiers générés sous l'ancien nom, et les schémas JSON publiés acceptent les deux graphies. Les nouveaux fichiers utilisent les nouveaux noms. Les bases d'historique SQLite sont inchangées et se chargent comme avant. |
| Scripts Kadupul issus de `netprobe export` | Scripts issus de `hostcensus export` | Les anciens scripts continuent de fonctionner et lisent toujours `NETPROBE_SNMP_*` à l'exécution. Les nouveaux scripts lisent `HOSTCENSUS_SNMP_*`. |

## Exemple rapide

Exécuté depuis le conteneur de test du laboratoire d'intégration décrit dans la section Développement ; sortie abrégée :

```console
$ hostcensus scan 172.30.57.8/29 --services ssh,http,snmp --save-snapshot after.json
┃ IP Address   ┃ Hostname       ┃ SSH ┃ SNMP ┃ MySQL ┃ Open services  ┃ Status ┃
│ 172.30.57.10 │ hostcensus-it-s… │ ✅  │  ❌  │  ❌   │ ssh:22         │ UP     │
│              │                │     │      │       │ OpenSSH_10.0   │        │
│ 172.30.57.13 │ hostcensus-it-w… │ ❌  │  ❌  │  ❌   │ http:80        │ UP     │
│              │                │     │      │       │ nginx/1.28.3   │        │

$ hostcensus diff before.json after.json; echo "exit=$?"
Warning: targets differ: 172.30.57.10 vs 172.30.57.8/29
│ new host │ 172.30.57.13 │ http:80/tcp  │ hostcensus-it-web-1.hostcensus-it_lab   │
exit=3

$ hostcensus export after.json -o kadupul-import.sh --template 1
$ grep 57.13 kadupul-import.sh
add --description=hostcensus-it-web-1.hostcensus-it_lab --ip=172.30.57.13 --template=1 --version=0 --avail=ping --ping_method=tcp --ping_port=80 '--notes=hostcensus: http:80/tcp nginx/1.28.3'
```

## Codes de sortie

| Commande | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | observations/rapport enregistrés | échec du contrôle préalable/backend, de l'historique ou de l'écriture du rapport/instantané | cible, options, configuration ou limites invalides | - | `--deadline` atteint ; rapport partiel écrit, historique et instantané ignorés |
| `preflight` | vérifications réussies | échec d'une vérification locale | cible/configuration invalide ou destinations en conflit | - | - |
| `profiles` | profils validés listés | - | configuration ou sélection illisible/invalide | - | - |
| `history` | résumés listés | historique manquant, invalide ou non pris en charge | options CLI invalides | - | - |
| `compare` | comparaison générée, y compris en cas de changements | historique illisible, périmètre/ordre incompatible ou échec d'écriture | options CLI invalides | - | - |
| `diff` | aucun changement | impossible d'écrire le fichier `-o` | entrée manquante, illisible ou non prise en charge, ou scan incomplet sans `--allow-partial` | changements détectés, observations non confirmées ou scan incomplet | - |
| `export` | script généré | impossible d'écrire le script | entrée illisible, scan incomplet sans `--allow-partial` ou données ne pouvant pas être exportées de manière sûre | - | - |

## Organisation du code

| Module | Responsabilité |
| --- | --- |
| `cli.py` | Options de commande, résolution des profils, contrôle préalable, scan et génération des rapports |
| `scanner.py`, `probes.py` | Expansion des cibles, workers bornés, découverte d'hôtes et observations de services |
| `config.py`, `profiles.py` | Définitions de services et profils d'inventaire validés |
| `models.py`, `output.py` | Types de résultats et rendu terminal/JSON/CSV |
| `history.py`, `diff.py` | Historique SQLite et comparaisons d'instantanés de fichiers versionnés |
| `preflight.py` | Vérifications locales et détection bornée de la version de Nmap |
| `export.py` | Scripts d'importation Kadupul validés et échappés pour le shell |

Chaque observation de service enregistre son état séparément de l'identité annoncée.
Les lectures et échéances sont bornées ; les exceptions de sonde restent consignées dans les erreurs par hôte. L'historique
SQLite utilise des transactions, une fermeture explicite des connexions et des accès en lecture seule pour le listage et
la comparaison. Les secrets SNMP ne transitent que par variables d'environnement ou fichiers de
secrets ; l'historique d'inventaire stocke les paramètres effectifs non secrets. Consultez
[Architecture](../../../docs/architecture.md) pour le pipeline de scan, ses limites et ses frontières
de confiance, ainsi que [SECURITY.md](../../../SECURITY.md#authorized-use) pour l'usage autorisé.


## Utilisation

Ne scannez que les réseaux que vous administrez.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Option | Signification |
| --- | --- |
| `NETWORK` | CIDR, adresse IP ou nom d'hôte ; optionnel avec `--profile`. Les identifiants de portée IPv6 sont rejetés. |
| `-o, --output PATH` | Écrit un rapport. Le format dépend de l'extension (`.json`, `.csv`) ; les autres extensions utilisent JSON par défaut. |
| `-f, --format json\|csv\|kadupul\|auto` | Force le format du rapport. Sans effet sans `--output`. `.sh` sélectionne `kadupul`. |
| `-v, --verbose` | Journalisation en mode débogage. |
| `-q, --quiet` | Supprime les résultats, la progression et les journaux d'information ; les avertissements et erreurs restent affichés sur stderr. |
| `--backend asyncio\|nmap` | Découverte d'hôtes. `asyncio` (par défaut) sonde directement les ports de services ; `nmap` lance d'abord un balayage ping nmap et nécessite l'exécutable `nmap` dans `PATH`. |
| `--timeout SECONDS` | Délai d'attente pour les sondes qui ne définissent pas leur propre budget (par défaut 1,0). Les sondes de connexion intégrées utilisent 0,3 s sauf si la table des services définit `timeout`. |
| `--concurrency N` | Nombre de sondes simultanées en cours (par défaut 256). |
| `--deadline SECONDS` | Arrête l'ensemble du scan, balayage nmap inclus, au bout de cette durée (par défaut 3600, maximum 604800 ; variable `HOSTCENSUS_DEADLINE`). Les hôtes terminés sont écrits dans le rapport avec `"complete": false`, aucun historique ni instantané n'est enregistré et `scan` retourne le code 4. |
| `--config PATH` | Définitions de services TOML et section optionnelle de profils nommés `[profiles]`. |
| `--profile NAME` | Utilise un profil nommé ; pointe par défaut vers `hostcensus.toml` si `--config` est omis. |
| `--exclude IP/CIDR` | Ajoute une exclusion ; répétable au besoin. Un hôte IPv4 exclu exclut aussi les adresses IPv6 qui y mènent : IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) et 6to4. Les cibles et exclusions IPv4-mapped sont traitées comme les adresses IPv4 qu'elles représentent. |
| `--max-hosts N` | Limite d'adresses vérifiée avant exclusions (valeur par défaut et maximum strict : 65 536). |
| `--history PATH` | Enregistre le scan terminé dans une base d'historique SQLite optionnelle. |
| `--services NAMES` | Liste de noms de services séparés par des virgules à vérifier, dans cet ordre (par défaut : tous). |
| `--ports SPEC` | Liste séparée par des virgules de `NAME=PORT` (déplacer un service) ou `PORT` (ajouter une vérification TCP simple nommée `tcp-PORT`). |
| `--snmp-community-file PATH` | Fichier contenant la communauté SNMPv2c pour la requête MIB système. Variable d'environnement : `HOSTCENSUS_SNMP_COMMUNITY` (la valeur) ou `HOSTCENSUS_SNMP_COMMUNITY_FILE` (le chemin). |
| `--snmp-user` | Utilisateur SNMPv3. Variable d'environnement : `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (par défaut), `SHA224`, `SHA256`, `SHA384`, `SHA512` et un fichier contenant la phrase secrète. Variables d'environnement : `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` ou `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (par défaut), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` et un fichier contenant la phrase secrète. Variables d'environnement : `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` ou `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Enregistre également un instantané versionné pour `hostcensus diff`. |
| `--tls-ca-file PATH` | Vérifie les certificats HTTPS à l'aide de ce bundle PEM au lieu du magasin système. Variable d'environnement : `HOSTCENSUS_TLS_CA_FILE`. |

Par défaut, chaque hôte est vérifié pour SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) et HTTPS (TCP 443). Les ports TCP sont testés via une connexion complète. SNMP est testé par une requête de découverte de moteur SNMPv3, à laquelle tout agent SNMPv3 doit répondre sans identifiants ; les agents qui ne parlent que v1/v2c ne sont pas détectés par cette sonde. Avec le backend asyncio, un hôte est considéré comme actif dès qu'une sonde reçoit une réponse, y compris un refus de connexion ; un hôte qui rejette silencieusement toutes les sondes obtient donc `alive=false` avec l'erreur "Host is down", ce qui ne prouve pas qu'il est physiquement éteint. Avec `--backend nmap`, c'est nmap qui détermine les hôtes actifs (ICMP en root, TCP 80/443 sinon).

### Empreintes de services

Chaque service ouvert est identifié par empreinte à partir de ce qu'il renvoie avant toute authentification. Rien ne s'authentifie, à l'exception de la requête SNMP, et uniquement lorsque vous fournissez des identifiants.

| Sonde | Lit | `version` | Clés de `details` |
| --- | --- | --- | --- |
| `ssh` | Ligne d'identification RFC 4253 | logiciel, par ex. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Poignée de main initiale MySQL/MariaDB | version du serveur | `server_version`, `flavor`, `auth_plugin`, ou `error_code`/`error` |
| `http` | Réponse `HEAD /` | en-tête `Server` | `status`, `server` |
| `https` | Négociation TLS, certificat, `HEAD /` | en-tête `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | Découverte SNMPv3 ; avec identifiants, GET de sysDescr, sysObjectID, sysName | sysDescr | `engine_id` ; avec identifiants `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, ou `snmp_error` |

Un nom d'hôte cible est résolu une seule fois par hôte et chaque sonde se connecte à cette adresse, enregistrée sous `address` dans les résultats ; le nom n'est utilisé que pour le SNI TLS, la vérification du certificat et l'en-tête HTTP `Host`. Un nom qui ne peut pas être résolu produit des états `unknown` et une erreur `Cannot resolve`. Les noms DNS inverses ne sont conservés que s'ils contiennent des caractères valides de nom d'hôte, avec au maximum 16 résolutions simultanées. HTTPS vérifie le certificat et le nom d'hôte par rapport au magasin système ou à `--tls-ca-file`. Le magasin de confiance est chargé une seule fois pour le scan et réutilisé par chaque sonde HTTPS. La connexion TCP et la négociation TLS sont chronométrées séparément : un port qui accepte les connexions mais bloque lors de la négociation apparaît donc comme `open` avec `tls_error`, et non comme `filtered`. Si la vérification échoue, le résultat enregistre `cert_verified: false` et `cert_verify_error` ; aucune nouvelle tentative avec des paramètres moins stricts n'est effectuée et aucune requête HTTP n'est envoyée. Les détails du certificat et les en-têtes HTTP ne sont collectés qu'après réussite de la vérification. Fournissez le bundle CA approprié pour les services utilisant une autorité de certification privée. Les anciens rapports peuvent contenir `cert_read_unverified`, que les sondes actuelles ne produisent plus.

Les secrets SNMP sont lus uniquement depuis des variables d'environnement ou des fichiers (`--snmp-*-file`, ou la variable correspondante `HOSTCENSUS_SNMP_*_FILE`), jamais depuis des valeurs passées en ligne de commande, visibles par d'autres utilisateurs locaux dans la liste des processus. Les options `--snmp-community`, `--snmp-auth-key` et `--snmp-priv-key` accompagnées d'une valeur quittent avec le code 2 en indiquant l'alternative à utiliser. Un fichier de secret doit être en UTF-8 non vide et ne pas dépasser 4096 octets ; un saut de ligne final unique est ignoré, et définir à la fois une variable et un fichier pour le même secret provoque une erreur. Les messages d'erreur mentionnent le nom du fichier sans jamais afficher son contenu. Les rapports de scan et l'historique n'incluent pas intentionnellement les valeurs d'identifiants. L'exportateur dispose d'une option explicite distincte `--include-credentials` décrite ci-dessous. Une communauté sélectionne SNMPv2c ; un utilisateur sélectionne SNMPv3, avec authentification lorsqu'une clé d'authentification est fournie et chiffrement lorsque les deux clés sont fournies (`snmp_security_level` indique le niveau retenu). hostcensus refuse, avec le code de sortie 2, de combiner une communauté avec un utilisateur v3, d'utiliser une clé de chiffrement sans clé d'authentification ou d'utiliser des clés sans utilisateur, et ne retente jamais une requête v3 échouée en v2c ni à un niveau de sécurité inférieur. Les agents qui ne parlent que v1/v2c ignorent la découverte v3 sans identifiants et n'apparaissent donc comme ouverts que lorsqu'une communauté est fournie.

Le texte des bannières est limité aux caractères imprimables et tronqué à 256 caractères avant stockage ou affichage. Les lectures sont également bornées : 4 Kio par ligne, 4 Kio pour une bannière d'accueil MySQL, 16 Kio d'en-têtes HTTP. Un identifiant de moteur SNMP de plus de 32 octets est tronqué avant stockage. HTTP et HTTPS envoient un en-tête Host contenant l'adresse IPv6 entre crochets ainsi que le port lorsqu'il est différent de 80 ou 443. Les cellules CSV qui commencent par un caractère déclencheur de formule de tableur sont préfixées afin de rester interprétées comme du texte.

### Limites

Une exécution accepte au maximum 65 536 adresses, 64 services et 524 288 sondes (hôtes multipliés par services) ; toute demande dépassant ces plafonds quitte avec le code 2 avant l'envoi du moindre paquet. `--concurrency` est plafonné à 4096 sockets. Chaque sonde dispose d'une échéance stricte égale à quatre fois son propre budget. Les sondes de connexion (`tcp`, `ssh`, `mysql`, `http`) utilisent 0,3 seconde sauf si le service définit `timeout`. SNMP et HTTPS utilisent `--timeout` (1,0 par défaut) lorsqu'aucun délai spécifique n'est défini. Une sonde qui atteint son échéance est rapportée comme `unknown` avec "probe timed out" dans `errors`. Les erreurs locales de socket (par exemple l'épuisement des descripteurs de fichiers) donnent également `unknown` avec l'erreur enregistrée ; elles ne sont jamais comptées comme un port filtré ni comme un hôte inactif. Avant de sonder, hostcensus relève la limite logicielle de fichiers ouverts vers la limite matérielle pour couvrir `--concurrency` plus 64 descripteurs ; en cas d'échec, la vérification préalable `open files` échoue et `scan` quitte avec le code 1 avant d'émettre le moindre trafic. La découverte Nmap utilise un délai d'attente de 30 secondes par hôte. Un préfixe est transmis à nmap au format CIDR, et un balayage échoue avec le code 1 lorsque nmap renvoie moins d'adresses qu'il n'en a reçu (par exemple un nom qu'il ne peut pas résoudre) au lieu de marquer les hôtes comme inactifs. Un nom d'hôte cible est résolu une seule fois et c'est cette adresse qui est transmise à nmap, afin que la découverte et les sondes ciblent la même machine. Un préfixe complet correspond à un seul processus nmap dont l'échéance de sous-processus est de 35 secondes par tranche de 256 adresses, arrondie au supérieur. Les balayages avec exclusions utilisent des lots de 256 hôtes avec une échéance de 35 secondes par lot. La création de workers est bornée indépendamment de la taille de la plage. Le DNS inverse et la résolution de noms d'hôtes ont une échéance distincte de deux secondes ; un appel de résolution qui ne répond jamais est abandonné dans son propre thread, afin de ne pas retenir hostcensus au-delà de ces limites. Au maximum 16 résolutions s'exécutent simultanément, et un appel abandonné conserve son emplacement jusqu'à son retour, ce qui borne le nombre de threads bloqués ; si les 16 se bloquent, les résolutions suivantes attendent un emplacement libre hors du délai de deux secondes (qui ne démarre qu'une fois un emplacement libéré) jusqu'à ce que `--deadline` arrête le scan. Utilisé comme bibliothèque sans `deadline`, `NetworkScanner` peut attendre un tel emplacement indéfiniment. `--deadline` (une heure par défaut) borne l'ensemble de l'exécution en plus de ces limites.

### Configuration des services

Les services peuvent être modifiés via un fichier TOML :

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` prend l'une des valeurs `tcp`, `ssh`, `mysql`, `http`, `https` ou `snmp`, et vaut par défaut le nom du service lorsque celui-ci correspond à une sonde, sinon `tcp`. Seul `snmp` utilise UDP. Les noms de services se composent de lettres minuscules, de chiffres, de `-` et de `_`. Deux services ne peuvent pas partager le même port et le même protocole ; l'historique enregistre un seul état pour cette paire. `timeout` est optionnel, exprimé en secondes, et vaut au minimum 0,05. Les sondes de type connexion (`tcp`, `ssh`, `mysql`, `http`) utilisent 0,3 seconde par défaut. `snmp` et `https` utilisent l'option `--timeout` du scan lorsque le service ne définit pas `timeout`. `--timeout` ne remplace pas un budget déjà fixé sur le service.

Les rapports JSON sont des documents versionnés (`"format": "hostcensus-report"`, `"version": 1`) qui enregistrent la cible, les services sondés et les paramètres à côté de `devices` ; `--format json` sans `-o` écrit le rapport sur stdout au lieu du tableau. Chaque sortie JSON dispose d'un schéma publié ; voir [Sortie JSON](../../../docs/json-output.md). Les équipements conservent les champs d'origine `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` et `errors`, et ajoutent une liste `services` contenant pour chaque sonde `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, ou `unknown` lorsque la sonde a échoué localement ou atteint son échéance), `version` et `details`. La sortie CSV ajoute en fin de ligne les colonnes `services` et `versions` pour les services ouverts. Les booléens `ssh`, `snmp` et `mysql` correspondent aux services portant exactement ces noms.


## Profils d'inventaire, contrôle préalable et historique local

Les profils nommés partagent un fichier TOML avec les définitions `[services]` existantes. Copiez
[hostcensus.example.toml](../../../hostcensus.example.toml) vers `hostcensus.toml` et renseignez les réseaux
que vous administrez :

```toml
[profiles.office]
network = "192.168.1.0/24"
exclusions = ["192.168.1.1"]
services = "ssh,http,https,mysql"
concurrency = 32
timeout = 1.0
max_hosts = 256
backend = "asyncio"
```

```bash
hostcensus profiles --config hostcensus.toml
hostcensus preflight --profile office --config hostcensus.toml
hostcensus scan --profile office --config hostcensus.toml -o report.json
```

`preflight` résout les options et les profils exactement comme `scan`, y compris
`--concurrency` pour la vérification des fichiers ouverts : un contrôle préalable réussi garantit donc que `scan`
démarrera avec le même plan d'exécution.

Les profils acceptent `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency` et `max_hosts`. `services` et `ports` utilisent la syntaxe existante en liste séparée par des virgules.
Les options CLI explicites surchargent les paramètres du profil ; les options `--exclude` répétées
s'ajoutent aux exclusions du profil. Un réseau indiqué explicitement avec `--profile` doit être
inclus dans le périmètre IP/CIDR de ce profil. Les noms d'hôtes restent pris en charge pour les scans
directs, mais ne peuvent pas être combinés avec des exclusions IP. Les limites d'hôtes s'appliquent avant
les exclusions ; le plafond total de sondes s'applique ensuite. Les hôtes exclus sont
écartés aussi bien des vérifications de services que de la découverte Nmap optionnelle.

Chaque scan effectue des vérifications préalables locales avant d'envoyer le moindre trafic vers les cibles : limites
de cibles/sondes, accès aux destinations, disponibilité optionnelle de l'exécutable/wrapper Nmap, schéma
de l'historique et bundle CA TLS configuré. `preflight` renvoie un rapport JSON et ne scanne aucune
cible ni ne crée de base d'historique. Il écrit temporairement un fichier voisin pour tester
l'accès en écriture sans modifier le contenu existant. Le backend asyncio par défaut
ne nécessite toujours ni Nmap ni les droits root. Les chemins de destination doivent être distincts les uns des
autres ainsi que du fichier de configuration en entrée, liens matériels inclus ; les liens symboliques en destination sont
rejetés. Les vérifications échouées retournent 1 ; un périmètre ou une configuration invalide retourne 2.

L'écriture des rapports et des exports requiert la prise en charge de `O_NOFOLLOW`. Sur les plateformes qui ne le supportent pas,
y compris Windows, ces écritures échouent sans ouvrir ni tronquer la destination.
Les nouveaux rapports et scripts d'export sont accessibles uniquement au propriétaire (mode 0600) ; le remplacement d'un fichier existant préserve ses
permissions. L'écriture dans un tube nommé sans lecteur échoue immédiatement au lieu de bloquer. Une nouvelle base `--history` est également créée avec accès réservé au propriétaire ; une base existante conserve son mode. Les messages de journalisation vont toujours sur stderr afin que stdout ne contienne que les résultats. Les exports contenant des identifiants forcent systématiquement le mode 0600.

L'historique est optionnel et complète les instantanés JSON existants ainsi que la commande `diff` :

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Utilisez les identifiants renvoyés par `history` ; l'exemple suppose une base nouvellement créée. Les instantanés sont stockés
de façon transactionnelle avec les horodatages UTC de début/fin, la version du paquet, les paramètres effectifs
non secrets, les résumés et l'ensemble des observations hôtes/services, y compris les erreurs par hôte.
Les observations partielles d'hôtes sont conservées. Les exécutions annulées ne sont pas enregistrées. Les contrats
existants pour les rapports, instantanés, exports et codes de sortie de scan sont préservés.

`history` liste les résumés JSON sans lire l'intégralité des données historiques des équipements.
`compare` lit deux scans enregistrés, exige des cibles et des ports sélectionnés identiques,
et signale les évolutions de réactivité, de statut et d'état des ports. L'identifiant du scan le plus ancien
doit précéder celui du plus récent. Lorsque les deux scans ont enregistré `timeout` ou `backend`
et que ces valeurs diffèrent, le rapport affiche un avertissement tout en comparant les
observations. Un délai d'attente différent peut faire apparaître un port filtré comme ouvert. Les erreurs du scanner
et les observations de ports inconnus sont marquées comme incertaines plutôt que traitées comme une
disparition ou une fermeture confirmée : les hôtes en erreur figurent dans `uncertain_hosts`, et
chaque transition de port impliquant `unknown` (y compris inconnu dans les deux scans) est listée
dans `unconfirmed_ports` au lieu de `port_changes`, sauf pour un port ouvert lors du
scan ultérieur, qui constitue bien un changement de port. `compare` et `diff` classent les ports selon la même règle.
`no_longer_responding` signifie une absence de réponse, et non la preuve que l'équipement a été retiré.
Un code de sortie 0 du scan ne garantit pas que tous les hôtes ont répondu : vérifiez les erreurs par hôte. Une comparaison réussie retourne 0 qu'il y ait ou non des changements ; la commande `diff` sur fichiers
conserve son contrat de code de sortie 3. Un historique non pris en charge ou corrompu retourne 1.

L'historique stocke des données d'inventaire : choisissez donc un répertoire local convenablement protégé.
Les fichiers de profil et les paramètres stockés ne contiennent pas d'identifiants SNMP ;
la gestion des identifiants reste assurée par les options d'exécution et variables d'environnement existantes.

## Comparaison d'inventaire (diff)

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Un instantané est un fichier JSON contenant `format: "hostcensus-snapshot"`, `version: 1`, la version de hostcensus, la date de création UTC, la cible, le `timeout` et le `backend` du scan lorsqu'ils ont été enregistrés, les services sondés ainsi que les hôtes actifs dans la même structure que le rapport `-o`. Les hôtes inactifs ne sont pas inclus. `diff` accepte également les rapports JSON standards issus de `scan -o`, y compris ceux générés avant l'introduction du champ `services`.

`diff` signale les hôtes apparus et disparus, les ports ouverts ou fermés sur les hôtes présents dans les deux fichiers, ainsi que les services dont le champ `version` a changé. Les ports sondés dans un seul des deux scans ne sont pas comparés, ce qui est signalé par un avertissement. Les observations en échec ne sont jamais interprétées comme une absence de changement : un port ayant l'état `unknown` dans l'un ou l'autre scan et qui n'est pas ouvert dans le second est listé sous `unconfirmed`, et non sous `closed`, avec `before` valant `open`, `unknown` ou `not-open` (sondé et fermé ou filtré) et `after` valant `unknown` ou `not-open` ; un port désormais ouvert est rapporté sous `opened` même si la sonde précédente avait échoué. Un hôte dont toutes les sondes ont échoué sans réponse dans l'un des deux scans est listé sous `unsettled_hosts` (avec `before`/`after` valant `up`, `uncertain` ou `absent`, y compris s'il a échoué dans les deux scans ou s'il est absent de l'autre fichier) au lieu de `vanished_hosts` ; s'il répond lors du scan ultérieur, il est également signalé comme nouvel hôte avec ses ports ouverts. Les instantanés conservent ces hôtes en échec pour cette raison. Un avertissement s'affiche aussi lorsque les cibles diffèrent, ainsi que lorsque les deux fichiers enregistrent un délai d'attente ou un backend différent. `-o PATH` permet également d'écrire la sortie JSON dans un fichier.

Un rapport issu d'un scan interrompu par `--deadline` (`"complete": false`) ne liste que les hôtes atteints ; `diff` et `export` le refusent donc avec le code de sortie 2. `--allow-partial` permet de l'accepter avec un avertissement sur stderr : `diff` classe alors les hôtes totalement absents du scan incomplet sous `unsettled_hosts` avec le statut `unscanned` au lieu de disparus (un hôte marqué comme inactif reste toutefois considéré comme disparu), positionne `partial` à true et ne renvoie jamais « aucun changement », tandis que `export` ajoute un avertissement dans l'en-tête du script.

Codes de sortie de `diff` : `0` aucun changement, `3` changements détectés, observations impossibles à confirmer ou entrée incomplète (`changed` vaut true dès qu'une liste, y compris `unsettled_hosts` et `unconfirmed`, est non vide ou que `partial` vaut true), `2` fichier manquant, illisible, instantané non pris en charge ou incomplet sans `--allow-partial`, `1` impossible d'écrire le fichier `-o`.

## Export Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (un fork de Cacti 1.2.31) ne propose pas d'import en masse d'équipements par fichier. La méthode prise en charge pour ajouter des équipements par script passe par `cli/add_device.php`, un équipement par appel, avec des arguments `--option=value`. `hostcensus export` génère un script POSIX `sh` contenant ces appels :

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Chaque hôte actif devient `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...` :

- Les hôtes pour lesquels la requête SNMP du scan a réussi reçoivent `--version=2 --community=...` ou `--version=3 --username=... --authproto=... --password=...` (plus `--privproto`/`--privpass` pour authPriv), `--port` et `--avail=snmp`. L'export SNMPv3 nécessite `--snmp-user`, et le mode noAuthNoPriv est refusé car `add_device.php` exige un mot de passe v3.
- Les autres hôtes reçoivent `--version=0 --avail=ping`, avec `--ping_method=tcp --ping_port=` pointant sur le premier port TCP ouvert, ou ICMP s'il n'y en a aucun.
- `--notes` liste les services ouverts et leurs versions. `--description` reprend le nom DNS inverse lorsqu'il est simple (lettres, chiffres, `.`, `_`, `-`), sinon l'adresse IP, et est rendu unique car `add_device.php` traite une description déjà existante comme une mise à jour de cet équipement.

Chaque valeur est validée et protégée pour le shell avec `shlex.quote`. Par défaut, aucun secret SNMP n'est écrit dans le fichier : le script résout `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` ou `HOSTCENSUS_SNMP_PRIV_KEY` à l'exécution et s'arrête si l'une des variables est absente. `--include-credentials` écrit à la place les valeurs issues de ces variables d'environnement dans le script, le crée en mode 0600 et journalise un avertissement. `add_device.php` affiche lui-même la communauté et reçoit les secrets en arguments, qui sont visibles dans la liste des processus du serveur Kadupul pendant l'exécution de chaque appel.

`add_device.php` retourne 1 en cas de doublon ou d'erreur ; le script poursuit l'exécution, comptabilise les échecs et quitte avec le code 1 si au moins un équipement n'a pas pu être ajouté. Les identifiants de modèles s'obtiennent via `php cli/add_device.php --list-host-templates`. Codes de sortie de `export` : `0` script généré, `2` entrée illisible, scan incomplet sans `--allow-partial` ou données ne pouvant pas être exportées de manière sûre, `1` impossible d'écrire le script.

## Gestion des versions et processus de publication

hostcensus suit la [gestion sémantique de version](https://semver.org/spec/v2.0.0.html) : les correctifs
compatibles incrémentent la version de correctif (patch), les fonctionnalités ou dépréciations compatibles incrémentent la
version mineure et les ruptures de compatibilité incrémentent la version majeure.
Les commandes et options, les codes de sortie et les schémas JSON constituent le contrat public ;
les comportements dépréciés continuent de fonctionner jusqu'à la prochaine version majeure, sauf si un
correctif de sécurité impose un changement plus rapide (le changelog en explique alors la raison).

release-please ouvre une PR de publication à partir des titres Conventional Commits sur `main`,
mettant à jour `pyproject.toml`, `uv.lock` et `CHANGES.md`. Sa fusion crée le tag
`vMAJOR.MINOR.PATCH` ainsi qu'un brouillon de release GitHub auquel la CI joint une wheel testée,
une archive source et les sommes de contrôle ; GitHub stocke les attestations de compilation pour
ces fichiers via son API d'attestations. Un mainteneur vérifie et publie le
brouillon une fois les fichiers attachés. Les releases ne sont jamais remplacées.

La publication de confiance sur PyPI (Trusted Publishing) est optionnelle et requiert la propriété du projet, un éditeur
de confiance et l'environnement `pypi`. Elle publie les mêmes artefacts vérifiés de la release
sans recompiler ni stocker de jeton API. Les releases taguées dans ce dépôt public
génèrent des attestations d'artefacts GitHub ; les forks privés nécessitent une offre prise en charge
et une activation explicite. Consultez le
[guide complet de publication](../../../docs/releasing.md) pour la configuration, les commandes exactes et les relances.

## Développement

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

Les outils de développement sont regroupés selon la [PEP 735](https://peps.python.org/pep-0735/) dans
`pyproject.toml` (`dev`, `fuzz`, `build`), de sorte qu'ils n'apparaissent jamais dans les
métadonnées du paquet publié. `uv.lock` est l'unique fichier de verrouillage ; la CI installe avec
`uv sync --locked` et échoue si le fichier de verrouillage n'est pas à jour. Sélectionnez l'interpréteur avec
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`) ou tout Python 3.12+.

La CI impose un seuil minimal de 90 % de couverture du paquet. Les tests unitaires incluent des serveurs
loopback contrôlés ainsi que des cas hors ligne pour les profils, l'historique et la validation des releases ; le laboratoire Compose exécute
OpenSSH, MariaDB, nginx et net-snmp sur un pont réseau isolé. Lancez-le avec
`make test-integration`. Consultez [CONTRIBUTING.md](../../../CONTRIBUTING.md) et
[les outils de publication](../../../scripts/README.md).

Le conteneur d'exécution tourne sous l'UID/GID 10001 sans répertoire personnel, sans shell
de connexion ni pip, et peut écrire dans `/app/output`. Accordez à cet utilisateur le droit d'écriture sur
tout répertoire de sortie monté. Il ne requiert aucune capability Linux et fonctionne avec un
système de fichiers racine en lecture seule ; il peut donc être lancé ainsi :

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap utilise son mode de découverte TCP non privilégié dans ce conteneur. La CI fait échouer
la construction de l'image dès que Trivy détecte une vulnérabilité corrigeable de sévérité HIGH ou CRITICAL.

## Vérifications de la chaîne logicielle

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
s'exécute sur main ainsi que chaque semaine, publie son score réel et téléverse les résultats vers GitHub
Code Scanning. Les actions et images de base de conteneurs sont épinglées par empreintes immuables ; les dépendances
Python sont résolues dans `uv.lock`. Les alertes Bandit font échouer la CI, et un fuzzing Atheris
borné teste les analyseurs SSH, MySQL, HTTP, de certificats et BER SNMPv3
sans accès réseau.

Scorecard mesure également l'activité historique de revue de code, la diversité des contributeurs et
la provenance des releases. Ces scores reflètent des éléments factuels ; ils ne prétendent pas
que chaque contrôle de gouvernance ou de release historique est satisfait. Consultez
[SECURITY.md](../../../SECURITY.md) et [la provenance des releases](../../../docs/releasing.md).

## Localisation

Les messages de la CLI ainsi que les tableaux de synthèse et de comparaison dans le terminal prennent en charge 45 locales (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) sans aucune dépendance d'exécution supplémentaire. La résolution suit l'ordre `--lang`, puis `LC_ALL`, `LC_MESSAGES` et `LANG`, avec repli sur `en`. Les schémas JSON, les colonnes CSV et les scripts d'export restent inchangés quelle que soit la locale.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Contribuer

Les contributions doivent inclure un cas reproductible, préserver les contrats CLI et
de formats de données documentés, et satisfaire aux contrôles qualité ci-dessus. Consultez
[CONTRIBUTING.md](../../../CONTRIBUTING.md) pour le flux de développement et
[le guide de publication](../../../docs/releasing.md) pour les décisions relatives à la compatibilité et au versionnage.

## Sécurité et licence

Consultez [SECURITY.md](../../../SECURITY.md) pour le signalement privé des vulnérabilités et les versions prises en charge.
hostcensus est distribué sous [licence MIT](../../../LICENSE).

Les en-têtes des fichiers sources utilisent des identifiants SPDX et préservent l'attribution des contributeurs issue de l'historique Git.
Consultez [AUTHORS.md](../../../AUTHORS.md) pour les crédits. Les captures binaires de test et le
fichier de verrouillage généré utilisent des fichiers `.license` adjacents ; le texte de la licence MIT se trouve dans `LICENSES/MIT.txt`.
