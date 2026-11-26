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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · **Français** · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus est un outil CLI Python pour réaliser des inventaires de services reproductibles sur les réseaux que vous administrez.
Il enregistre ce que les équipements exposent, compare les observations dans le temps et génère
des scripts d'importation Kadupul. Le backend par défaut utilise des sockets asyncio sans droits root ;
la découverte Nmap optionnelle permet d'identifier des hôtes au-delà des ports de services configurés.

## Pourquoi hostcensus

Un rapport ponctuel de ports n'indique pas si l'observation suivante a changé ou
a simplement échoué. hostcensus combine des états de service explicites, des sondes bornées, des
profils d'analyse réutilisables et un historique local. Les opérateurs peuvent répéter le même périmètre, inspecter
les erreurs et distinguer les observations incertaines des changements confirmés.

- **Preuves de service :** identification SSH, messages d'accueil MySQL, en-têtes HTTP, observations de
  certificats TLS et découverte SNMP ou requêtes system-MIB authentifiées.
- **Périmètre reproductible :** profils TOML nommés, exclusions additives, services
  configurables, plafonds d'hôtes/de sondes et workers bornés.
- **Vérifications avant tout trafic :** le preflight local valide les cibles, les outils, l'accès aux
  destinations, le schéma d'historique et les bundles CA TLS configurés.
- **Historique d'inventaire :** des instantanés SQLite transactionnels conservent toutes les observations ;
  les comparaisons gardent visibles les échecs du scanner et les états inconnus.
- **Sorties interopérables :** rapports en terminal, JSON et CSV, instantanés de fichiers versionnés
  et scripts d'importation Kadupul.

L'intégration continue couvre Python 3.12, 3.13 et 3.14 sur Linux et macOS, ainsi qu'un laboratoire d'intégration
Compose contrôlé. Le code utilise des alias de types modernes, des résultats de preflight typés,
des profils utilisant slots et paramètres nommés uniquement, et un nettoyage asynchrone structuré tout en conservant ces
versions d'exécution. Consultez [Gestion des versions et publications](../../../docs/releasing.md) pour le contrat de compatibilité
SemVer et le processus de publication GitHub. Le badge de version décrit les
artefacts publiés, et non le dépôt cloné : le dernier tag publié est actuellement
`v0.3.0`, tandis que cette version du code utilise la version de paquet `3.0.0`. Installez depuis le dépôt
pour utiliser les fonctionnalités d'inventaire documentées ici.

Commencez par [l'installation](#install), puis [les profils et l'historique](#inventory-profiles-preflight-and-local-history).
Pour les détails d'intégration, consultez [les empreintes de services](#fingerprints),
[la comparaison de fichiers](#inventory-diff) et [l'export Kadupul](#kadupul-export).

## Installation

Python 3.12 ou plus récent est requis ; la matrice testée couvre Python 3.12 à 3.14. Depuis ce
dépôt local, installez les dépendances d'exécution verrouillées :

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Pour la découverte d'hôtes optionnelle via Nmap, installez l'exécutable Nmap à l'aide du gestionnaire de
paquets de votre plateforme ; aucun paquet Python supplémentaire n'est nécessaire. La sortie XML de Nmap est analysée avec
defusedxml, une dépendance principale, ce qui bloque l'expansion d'entités. hostcensus exécute
directement le binaire `nmap` trouvé dans `PATH` avec une liste d'arguments fixe, une échéance qui augmente
avec la taille du préfixe et une limite de sortie de 64 Mio. Nmap n'est pas nécessaire pour le backend par défaut.

## Migration depuis netprobe

hostcensus est le nouveau nom de netprobe, publié dans la version 3.0.0. Le projet n'a jamais été
publié sur PyPI sous aucun de ces deux noms ; les installations se faisaient donc depuis un clone ou une
release GitHub. Le dépôt GitHub conserve son nom.

| Auparavant | Maintenant | Compatibilité |
| --- | --- | --- |
| Distribution `netprobe` | `hostcensus` | Réinstallez depuis le dépôt local ; il n'existe pas de paquet sous l'ancien nom. |
| Commande `netprobe` | `hostcensus` | `netprobe` fonctionne toujours et affiche une ligne d'avertissement d'obsolescence sur stderr. Les codes de sortie et stdout sont inchangés. Supprimée dans la prochaine version majeure. |
| Variables d'environnement `NETPROBE_*` | `HOSTCENSUS_*` | Une variable `NETPROBE_*` est utilisée lorsque son équivalent `HOSTCENSUS_*` n'est pas défini, avec un avertissement sur stderr qui nomme les variables et jamais leurs valeurs. `HOSTCENSUS_*` prévaut lorsque les deux sont définies. Supprimées dans la prochaine version majeure. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Rupture de compatibilité.** Aucun shim d'importation n'est installé ; mettez à jour vos imports. |
| Tag d'image Docker `network-discovery:test` (CI uniquement) et utilisateur du conteneur `netprobe` | `hostcensus:test`, utilisateur `hostcensus` | Aucune image de registre n'a jamais été publiée. Reconstruisez l'image et utilisez le point d'entrée `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Un fichier existant portant l'ancien nom par défaut est toujours utilisé, avec un avertissement, tant que le nouveau nom n'existe pas. Les chemins explicites `--config` et `--history` ne sont pas modifiés. |
| Rapports et instantanés avec `"format": "netprobe-report"` ou `"netprobe-snapshot"`, et le champ `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` et `export` chargent toujours les fichiers écrits sous l'ancien nom, et les schémas JSON publiés acceptent les deux orthographes. Les nouveaux fichiers utilisent les nouveaux noms. Les bases d'historique SQLite sont inchangées et se chargent comme avant. |
| Scripts Kadupul issus de `netprobe export` | Scripts issus de `hostcensus export` | Les anciens scripts continuent de fonctionner et lisent toujours `NETPROBE_SNMP_*` lors de leur exécution. Les nouveaux scripts lisent `HOSTCENSUS_SNMP_*`. |

## Exemple rapide

Exécuté depuis le conteneur de test du laboratoire d'intégration décrit dans la section Développement ; sortie tronquée :

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
| `scan` | observations/rapport enregistrés | échec du preflight/backend, de l'historique ou de l'écriture du rapport/instantané | cible, options, configuration ou limites invalides | - | `--deadline` atteint ; rapport partiel écrit, historique et instantané ignorés |
| `preflight` | vérifications réussies | échec d'une vérification locale | cible/configuration invalide ou destinations en conflit | - | - |
| `profiles` | profils validés listés | - | configuration ou sélection illisible/invalide | - | - |
| `history` | résumés listés | historique manquant, invalide ou non pris en charge | options CLI invalides | - | - |
| `compare` | comparaison produite, y compris en cas de changements | historique illisible, périmètre/ordre incompatible ou échec d'écriture | options CLI invalides | - | - |
| `diff` | aucun changement | impossible d'écrire le fichier `-o` | entrée manquante, illisible ou non prise en charge, ou analyse incomplète sans `--allow-partial` | changements détectés, observations non confirmées ou analyse incomplète | - |
| `export` | script écrit | impossible d'écrire le script | entrée illisible, analyse incomplète sans `--allow-partial`, ou données ne pouvant être exportées en toute sécurité | - | - |

## Structure du projet

| Module | Responsabilité |
| --- | --- |
| `cli.py` | Options de commande, résolution des profils, preflight, analyse et génération de rapports |
| `scanner.py`, `probes.py` | Développement des cibles, workers bornés, découverte d'hôtes et observations de services |
| `config.py`, `profiles.py` | Définitions des services et profils d'inventaire validés |
| `models.py`, `output.py` | Types de résultats et rendu terminal/JSON/CSV |
| `history.py`, `diff.py` | Historique SQLite et comparaisons d'instantanés de fichiers versionnés |
| `preflight.py` | Vérifications locales et récupération bornée de la version de Nmap |
| `export.py` | Scripts d'importation Kadupul validés et protégés contre l'injection shell |

Chaque observation de service enregistre son état séparément de l'identité qu'il annonce.
Les lectures et les échéances sont bornées ; les exceptions des sondes restent consignées dans les erreurs par hôte. L'historique SQLite
utilise des transactions, une fermeture explicite des connexions et des chemins de listage et de comparaison
en lecture seule. Les secrets SNMP entrent uniquement via des variables d'environnement ou des fichiers de
secrets ; l'historique d'inventaire stocke les paramètres effectifs non secrets. Consultez
[Architecture](../../../docs/architecture.md) pour le pipeline d'analyse, ses limites et ses frontières de
confiance, ainsi que [SECURITY.md](../../../SECURITY.md#authorized-use) pour les conditions d'utilisation autorisée.


## Utilisation

N'analysez que les réseaux que vous administrez.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Option | Signification |
| --- | --- |
| `NETWORK` | CIDR, IP ou nom d'hôte ; facultatif avec `--profile`. Les identifiants de portée IPv6 sont rejetés. |
| `-o, --output PATH` | Écrit un rapport. Le format suit l'extension (`.json`, `.csv`) ; les autres extensions utilisent JSON par défaut. |
| `-f, --format json\|csv\|kadupul\|auto` | Force le format du rapport. Sans effet sans `--output`. `.sh` sélectionne `kadupul`. |
| `-v, --verbose` | Journalisation de débogage. |
| `-q, --quiet` | Supprime les résultats, la progression et les journaux d'information ; les avertissements et erreurs apparaissent toujours sur stderr. |
| `--backend asyncio\|nmap` | Découverte d'hôtes. `asyncio` (par défaut) sonde directement les ports de services ; `nmap` lance d'abord un balayage ping nmap et nécessite l'exécutable `nmap` dans `PATH`. |
| `--timeout SECONDS` | Délai d'attente pour les sondes qui ne définissent pas leur propre budget (1.0 par défaut). Les sondes de connexion intégrées utilisent 0.3s sauf si la table des services définit `timeout`. |
| `--concurrency N` | Sondes simultanées en vol (256 par défaut). |
| `--deadline SECONDS` | Arrête l'ensemble de l'analyse, balayage nmap inclus, après cette durée (3600 par défaut, 604800 au maximum ; variable `HOSTCENSUS_DEADLINE`). Les hôtes terminés sont écrits dans le rapport avec `"complete": false`, aucun historique ni instantané n'est écrit, et `scan` quitte avec le code 4. |
| `--config PATH` | Définitions de services en TOML et paramètres `[profiles]` nommés optionnels. |
| `--profile NAME` | Utilise un profil nommé ; utilise `hostcensus.toml` par défaut lorsque `--config` est omis. |
| `--exclude IP/CIDR` | Ajoute une exclusion ; à répéter au besoin. Un hôte IPv4 exclu exclut également les adresses IPv6 qui l'atteignent : IPv4-mapped (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) et 6to4. Les cibles et exclusions IPv4-mapped sont traitées comme les adresses IPv4 qu'elles désignent. |
| `--max-hosts N` | Limite d'adresses vérifiée avant les exclusions (valeur par défaut et maximum absolu : 65 536). |
| `--history PATH` | Enregistre l'analyse terminée dans une base d'historique SQLite facultative. |
| `--services NAMES` | Liste de noms de services séparés par des virgules à vérifier, dans cet ordre (par défaut : tous). |
| `--ports SPEC` | Liste séparée par des virgules de `NAME=PORT` (déplacer un service) ou `PORT` (ajouter une vérification TCP simple nommée `tcp-PORT`). |
| `--snmp-community-file PATH` | Fichier contenant la communauté SNMPv2c pour la requête MIB système. Env : `HOSTCENSUS_SNMP_COMMUNITY` (la valeur) ou `HOSTCENSUS_SNMP_COMMUNITY_FILE` (le chemin). |
| `--snmp-user` | Utilisateur SNMPv3. Env : `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (par défaut), `SHA224`, `SHA256`, `SHA384`, `SHA512` et un fichier contenant la phrase secrète. Env : `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` ou `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (par défaut), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` et un fichier contenant la phrase secrète. Env : `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` ou `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Écrit également un instantané versionné pour `hostcensus diff`. |
| `--tls-ca-file PATH` | Vérifie les certificats HTTPS à l'aide de ce bundle PEM plutôt que du magasin système. Env : `HOSTCENSUS_TLS_CA_FILE`. |

Par défaut, chaque hôte est vérifié pour SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) et HTTPS (TCP 443). Les ports TCP sont testés avec une connexion complète. SNMP est testé avec une requête de découverte de moteur SNMPv3, à laquelle tout agent SNMPv3 doit répondre sans identifiants ; les agents qui ne parlent que v1/v2c ne seront pas détectés par cette sonde. Avec le backend asyncio, un hôte est considéré comme actif dès qu'une sonde obtient une réponse, y compris un refus de connexion ; ainsi, un hôte qui ignore silencieusement chaque sonde a `alive=false` et l'erreur « Host is down », ce qui ne prouve pas qu'il soit physiquement éteint. Avec `--backend nmap`, nmap détermine quels hôtes sont actifs (ICMP en tant que root, TCP 80/443 sinon).

### Empreintes de services

Chaque service ouvert est identifié à partir de ce qu'il envoie avant toute authentification. Rien ne s'authentifie à l'exception de la requête SNMP, et uniquement lorsque vous fournissez des identifiants.

| Sonde | Lit | `version` | Clés de `details` |
| --- | --- | --- | --- |
| `ssh` | Ligne d'identification RFC 4253 | logiciel, par ex. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Poignée de main initiale MySQL/MariaDB | version du serveur | `server_version`, `flavor`, `auth_plugin`, ou `error_code`/`error` |
| `http` | Réponse à `HEAD /` | En-tête `Server` | `status`, `server` |
| `https` | Poignée de main TLS, certificat, `HEAD /` | En-tête `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | Découverte SNMPv3 ; avec identifiants, GET de sysDescr, sysObjectID, sysName | sysDescr | `engine_id` ; avec identifiants `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, ou `snmp_error` |

Une cible fournie par nom d'hôte est résolue une fois par hôte et chaque sonde se connecte à cette adresse, enregistrée sous `address` dans les résultats ; le nom est utilisé uniquement pour le SNI TLS, la vérification du certificat et l'en-tête HTTP `Host`. Un nom qui ne peut pas être résolu donne des états `unknown` et une erreur `Cannot resolve`. Les noms DNS inverses ne sont conservés que s'ils contiennent des caractères de nom d'hôte, et au plus 16 recherches s'exécutent simultanément. HTTPS applique la vérification du certificat et du nom d'hôte par rapport au magasin système ou à `--tls-ca-file`. Le magasin de confiance est chargé une fois pour l'analyse et réutilisé pour chaque sonde HTTPS. La connexion TCP et la poignée de main TLS sont chronométrées séparément, si bien qu'un port qui accepte les connexions mais bloque la poignée de main est `open` avec `tls_error`, et non `filtered`. Si la vérification échoue, le résultat enregistre `cert_verified: false` et `cert_verify_error` ; il ne réessaie pas avec des paramètres plus faibles et n'envoie pas de requête HTTP. Les détails du certificat et les en-têtes HTTP ne sont collectés qu'après réussite de la vérification. Fournissez le bundle CA approprié pour les services utilisant une autorité de certification privée. Les anciens rapports peuvent contenir `cert_read_unverified`, que les sondes actuelles ne produisent plus.

Les secrets SNMP sont lus uniquement depuis des variables d'environnement ou des fichiers (`--snmp-*-file`, ou la variable `HOSTCENSUS_SNMP_*_FILE` correspondante), jamais depuis des valeurs en ligne de commande, que d'autres utilisateurs locaux peuvent voir dans la liste des processus. `--snmp-community`, `--snmp-auth-key` et `--snmp-priv-key` avec une valeur quittent avec le code 2 et indiquent l'option de remplacement. Un fichier de secret doit être en UTF-8 non vide d'au plus 4096 octets ; un saut de ligne final est ignoré, et définir à la fois une variable et un fichier pour le même secret est une erreur. Les erreurs nomment le fichier mais n'affichent jamais son contenu. Les rapports d'analyse et l'historique n'incluent pas intentionnellement les valeurs d'identifiants. L'exportateur dispose d'une option distincte et explicite `--include-credentials` décrite ci-dessous. Une communauté sélectionne SNMPv2c ; un utilisateur sélectionne SNMPv3, avec authentification lorsqu'une clé d'authentification est fournie et chiffrement lorsque les deux clés sont fournies (`snmp_security_level` indique lequel). hostcensus refuse, avec le code de sortie 2, de combiner une communauté avec un utilisateur v3, d'utiliser une clé de chiffrement sans clé d'authentification ou d'utiliser des clés sans utilisateur, et il ne réessaie jamais une requête v3 échouée avec v2c ou un niveau de sécurité inférieur. Les agents qui ne parlent que v1/v2c ignorent la découverte v3 sans identifiants ; ils n'apparaissent donc comme ouverts que lorsqu'une communauté est fournie.

Le texte des bannières est réduit aux caractères imprimables et plafonné à 256 caractères avant d'être stocké ou affiché. Les lectures sont également bornées : 4 Kio par ligne, 4 Kio pour un message d'accueil MySQL, 16 Kio d'en-têtes HTTP. Un identifiant de moteur SNMP dépassant 32 octets est tronqué avant d'être stocké. HTTP et HTTPS envoient un en-tête Host avec une adresse IPv6 entre crochets et avec le port lorsqu'il est différent de 80 ou 443. Les cellules CSV qui commencent par un caractère déclencheur de formule de tableur sont préfixées afin que la cellule reste du texte.

### Limites

Une exécution accepte au plus 65 536 adresses, 64 services et 524 288 sondes (hôtes multipliés par services) ; les demandes plus importantes quittent avec le code 2 avant tout envoi. `--concurrency` est plafonné à 4096 sockets. Chaque sonde dispose d'une échéance stricte égale à quatre fois son propre budget. Les sondes de connexion (`tcp`, `ssh`, `mysql`, `http`) utilisent 0,3 seconde sauf si ce service définit `timeout`. SNMP et HTTPS utilisent `--timeout` (1.0 par défaut) lorsqu'ils n'en définissent pas. Une sonde qui atteint son échéance est signalée comme `unknown` avec « probe timed out » dans `errors`. Les défaillances locales de sockets (par exemple un épuisement des descripteurs de fichiers) donnent également `unknown` avec l'erreur enregistrée ; elles ne comptent jamais comme un port filtré ni comme un hôte inactif. Avant de sonder, hostcensus élève la limite souple de fichiers ouverts vers la limite stricte pour accommoder `--concurrency` plus 64 descripteurs ; s'il n'y parvient pas, la vérification preflight `open files` échoue et `scan` quitte avec le code 1 avant d'émettre du trafic. La découverte Nmap utilise un délai d'attente par hôte de 30 secondes. Un préfixe est transmis à nmap au format CIDR, et un balayage échoue avec le code 1 lorsque nmap signale moins d'adresses qu'il n'en a reçu (par exemple un nom qu'il ne peut pas résoudre) plutôt que de marquer des hôtes comme inactifs. Une cible par nom d'hôte est résolue une fois et cette adresse est transmise à nmap, afin que la découverte et les sondes atteignent la même machine. Un préfixe complet correspond à un seul processus nmap dont l'échéance de sous-processus est de 35 secondes pour chaque tranche de 256 adresses, arrondie au supérieur. Les balayages avec exclusions utilisent des lots de 256 hôtes avec une échéance de 35 secondes par lot. La création de workers est bornée indépendamment de la taille de la plage. Le DNS inverse et la résolution de noms d'hôtes disposent d'une échéance distincte de deux secondes ; un appel de résolveur qui ne répond jamais est abandonné sur son propre thread, de sorte qu'il ne puisse pas maintenir hostcensus actif au-delà de ces limites. Au plus 16 recherches s'exécutent simultanément, et un appel abandonné conserve son emplacement jusqu'à son retour, ce qui borne le nombre de threads bloqués ; si les 16 se bloquent, les recherches suivantes attendent un emplacement en dehors de l'échéance de deux secondes (qui démarre une fois qu'un emplacement se libère) jusqu'à ce que `--deadline` arrête l'analyse. `NetworkScanner` utilisé comme bibliothèque sans `deadline` peut attendre un tel emplacement indéfiniment. `--deadline` (une heure par défaut) borne l'exécution globale en plus de ces limites.

### Configuration des services

Les services peuvent être modifiés à l'aide d'un fichier TOML :

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` vaut `tcp`, `ssh`, `mysql`, `http`, `https` ou `snmp`, et prend par défaut le nom du service s'il s'agit d'une sonde connue, sinon `tcp`. Seul `snmp` utilise UDP. Les noms de services sont composés de lettres minuscules, de chiffres, de `-` et de `_`. Deux services ne peuvent pas partager le même port et le même protocole ; l'historique enregistre un seul état pour cette paire. `timeout` est optionnel, en secondes, et vaut au moins 0,05. Les sondes de type connexion (`tcp`, `ssh`, `mysql`, `http`) utilisent 0,3 seconde par défaut. `snmp` et `https` utilisent le `--timeout` de l'analyse lorsque le service ne définit pas `timeout`. `--timeout` ne remplace pas un budget déjà défini par le service.

Les rapports JSON sont des documents versionnés (`"format": "hostcensus-report"`, `"version": 1`) qui enregistrent la cible, les services sondés et les paramètres aux côtés de `devices` ; `--format json` sans `-o` écrit le rapport sur stdout au lieu du tableau. Chaque sortie JSON dispose d'un schéma publié ; consultez [Sortie JSON](../../../docs/json-output.md). Les équipements conservent les champs d'origine `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` et `errors`, et ajoutent une liste `services` contenant pour chaque sonde `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered` ou `unknown` lorsque la sonde a échoué localement ou atteint son échéance), `version` et `details`. La sortie CSV gagne des colonnes finales `services` et `versions` pour les services ouverts. Les booléens `ssh`, `snmp` et `mysql` suivent les services portant exactement ces noms.


## Profils d'inventaire, preflight et historique local

Les profils nommés partagent un fichier TOML avec les définitions `[services]` existantes. Copiez
[hostcensus.example.toml](../../../hostcensus.example.toml) vers `hostcensus.toml` et indiquez les réseaux
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

`preflight` résout les options et les profils exactement comme le fait `scan`, y compris
`--concurrency` pour la vérification des fichiers ouverts, si bien qu'un preflight réussi signifie que `scan`
démarrera avec le même plan.

Les profils acceptent `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency` et `max_hosts`. `services` et `ports` utilisent la syntaxe existante en liste séparée par des virgules. Les options CLI explicites remplacent les paramètres du profil ; les options `--exclude` répétées
s'ajoutent aux exclusions du profil. Un réseau explicite avec `--profile` doit être
inclus dans le périmètre IP/CIDR de ce profil. Les noms d'hôtes restent pris en charge pour les
analyses directes, mais ne peuvent pas être combinés avec des exclusions IP. Les limites d'hôtes s'appliquent avant
les exclusions ; le plafond total de sondes s'applique toujours après. Les hôtes exclus sont
omis tant des vérifications de services que de la découverte Nmap optionnelle.

Chaque analyse effectue des vérifications locales de preflight avant d'émettre du trafic vers les cibles : limites de
cibles/sondes, accès aux destinations, disponibilité de l'exécutable ou du wrapper Nmap optionnel, schéma
d'historique et bundle CA TLS configuré. `preflight` produit du JSON et n'analyse pas
les cibles ni ne crée de base d'historique. Il écrit temporairement un fichier voisin pour tester
l'accès en écriture à la destination sans modifier le contenu existant. Le backend asyncio par défaut
ne nécessite toujours ni Nmap ni les droits root. Les chemins de destination doivent être distincts les uns des
autres et de la configuration d'entrée, y compris via des liens durs ; les liens symboliques de destination sont
rejetés. Les vérifications échouées retournent 1 ; un périmètre ou une configuration invalide retourne 2.

L'écriture des rapports et des exports exige la prise en charge de `O_NOFOLLOW`. Sur les plateformes qui en sont dépourvues,
dont Windows, ces écritures échouent sans ouvrir ni tronquer la destination.
Les nouveaux rapports et scripts d'exportation sont accessibles uniquement au propriétaire (mode 0600) ; le remplacement d'un fichier existant conserve ses
permissions. L'écriture vers un tube nommé sans lecteur échoue immédiatement au lieu d'attendre. Une nouvelle base `--history` est également créée accessible uniquement au propriétaire ; une base existante conserve son mode. Les messages de journal vont toujours sur stderr, afin que stdout ne contienne que les résultats. Les exports contenant des identifiants forcent toujours le mode 0600.

L'historique est facultatif et complète les instantanés JSON existants ainsi que la commande `diff` :

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Utilisez les identifiants issus de `history` ; l'exemple suppose une nouvelle base de données. Les instantanés sont stockés
de manière transactionnelle avec les heures de début/fin en UTC, la version du paquet, les paramètres effectifs
non secrets, les résumés et toutes les observations d'hôtes/services, y compris les erreurs par hôte.
Les observations d'hôtes incomplètes sont conservées. Les exécutions annulées ne sont pas enregistrées. Les contrats existants
de rapports, d'instantanés, d'exports et de codes de sortie de `scan` sont préservés.

`history` liste des résumés JSON sans lire l'ensemble des charges utiles historiques des équipements.
`compare` lit deux analyses enregistrées, exige des identités de cibles et des ports sélectionnés
identiques, et signale les changements de réactivité, d'état et d'état des ports. L'identifiant de l'analyse
antérieure doit précéder l'identifiant ultérieur. Lorsque les deux analyses ont enregistré `timeout` ou `backend`
et que ces valeurs diffèrent, le rapport affiche un avertissement tout en comparant les
observations. Un délai d'attente différent peut faire apparaître un port filtré comme ouvert. Les erreurs du scanner
et les observations de ports inconnus sont signalées comme incertaines plutôt que traitées comme une
disparition ou une fermeture confirmée : les hôtes avec erreurs apparaissent dans `uncertain_hosts`, et
chaque transition de port impliquant `unknown` (y compris inconnu dans les deux analyses) est listée
dans `unconfirmed_ports` au lieu de `port_changes`, sauf pour un port qui est ouvert dans l'analyse
ultérieure, ce qui constitue un changement de port. `compare` et `diff` classent les ports selon la même règle.
`no_longer_responding` signifie l'absence de réponse, et non la preuve du retrait d'un équipement.
Un code de sortie 0 de `scan` ne garantit pas que chaque hôte a répondu : inspectez les erreurs par hôte. Une comparaison réussie retourne 0 qu'il y ait ou non des changements ; la commande `diff` sur fichiers
conserve son contrat de code de sortie 3. Un historique non pris en charge ou corrompu retourne 1.

L'historique stocke des informations d'inventaire ; choisissez donc un répertoire local protégé de manière
appropriée. Les fichiers de profil et les paramètres stockés ne contiennent pas d'identifiants SNMP ;
la gestion des identifiants continue de passer par les options et variables d'environnement existantes à l'exécution.

## Comparaison d'inventaire

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Un instantané est un document JSON contenant `format: "hostcensus-snapshot"`, `version: 1`, la version de hostcensus, l'heure de création UTC, la cible, le `timeout` et le `backend` de l'analyse lorsqu'elle les a enregistrés, les services qui ont été sondés et les hôtes actifs sous la même forme que le rapport `-o`. Les hôtes inactifs sont omis. `diff` accepte également les rapports JSON simples issus de `scan -o`, y compris ceux antérieurs à l'existence du champ `services`.

`diff` signale les hôtes apparus et disparus, les ports ouverts ou fermés sur les hôtes présents dans les deux analyses et les services dont `version` a changé. Les ports sondés dans une seule des deux analyses ne sont pas comparés, et un avertissement l'indique. Les observations échouées ne sont jamais interprétées comme « aucun changement » : un port qui vaut `unknown` dans l'une ou l'autre analyse et qui n'est pas ouvert dans la plus récente est listé sous `unconfirmed`, et non sous `closed`, avec `before` valant `open`, `unknown` ou `not-open` (sondé et fermé ou filtré) et `after` valant `unknown` ou `not-open` ; un port désormais ouvert est signalé sous `opened` même si la sonde précédente avait échoué. Un hôte dont toutes les sondes ont échoué sans réponse dans l'une ou l'autre analyse est listé sous `unsettled_hosts` (avec `before`/`after` valant `up`, `uncertain` ou `absent`, y compris lorsqu'il a échoué dans les deux analyses ou est absent de l'autre fichier) au lieu de `vanished_hosts` ; s'il répond dans l'analyse ultérieure, il est également signalé comme nouvel hôte avec ses ports ouverts. Les instantanés conservent ces hôtes en échec pour cette raison. Un avertissement apparaît également lorsque les cibles diffèrent, et lorsque les deux fichiers ont enregistré un délai ou un backend différent. `-o PATH` écrit aussi la forme JSON dans un fichier.

Un rapport issu d'une analyse arrêtée par `--deadline` (`"complete": false`) ne liste que les hôtes atteints ; `diff` et `export` le refusent donc avec le code de sortie 2. `--allow-partial` l'accepte avec un avertissement sur stderr : `diff` liste alors les hôtes que l'analyse incomplète n'a pas du tout listés sous `unsettled_hosts` en tant que `unscanned` au lieu de disparus (un hôte qu'elle a listé comme inactif reste considéré comme disparu), définit `partial` à true et ne signale jamais aucun changement, tandis qu'`export` inscrit un avertissement dans l'en-tête du script.

Codes de sortie de `diff` : `0` aucun changement, `3` changements détectés, observations n'ayant pu être confirmées ou entrée incomplète (`changed` vaut true dès qu'une liste quelconque, y compris `unsettled_hosts` et `unconfirmed`, est non vide, ou que `partial` vaut true), `2` un fichier est manquant, illisible, n'est pas un instantané pris en charge ou est incomplet sans `--allow-partial`, `1` le fichier `-o` n'a pas pu être écrit.

## Export Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (un fork de Cacti 1.2.31) ne propose pas d'importation en masse par fichier d'équipements. La méthode prise en charge pour ajouter des équipements depuis un script est `cli/add_device.php`, un équipement par appel, avec des arguments `--option=value`. `hostcensus export` écrit un script `sh` POSIX composé de ces appels :

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Chaque hôte actif devient `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...` :

- Les hôtes pour lesquels la requête SNMP de l'analyse a réussi reçoivent `--version=2 --community=...` ou `--version=3 --username=... --authproto=... --password=...` (plus `--privproto`/`--privpass` pour authPriv), `--port` et `--avail=snmp`. L'export SNMPv3 nécessite `--snmp-user`, et noAuthNoPriv est refusé car `add_device.php` exige un mot de passe v3.
- Les autres hôtes reçoivent `--version=0 --avail=ping`, avec `--ping_method=tcp --ping_port=` correspondant au premier port TCP ouvert, ou ICMP s'il n'y en a aucun.
- `--notes` énumère les services ouverts et leurs versions. `--description` est le nom DNS inverse lorsqu'il est simple (lettres, chiffres, `.`, `_`, `-`), sinon l'IP, et est rendu unique, car `add_device.php` traite une description existante comme une mise à jour de cet équipement.

Chaque valeur est validée et protégée pour le shell avec `shlex.quote`. Par défaut, aucun secret SNMP n'est écrit : le script développe `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` ou `HOSTCENSUS_SNMP_PRIV_KEY` à l'exécution et s'arrête si l'un d'eux n'est pas défini. `--include-credentials` inscrit à la place les valeurs issues de ces variables d'environnement dans le script, le crée avec le mode 0600 et journalise un avertissement. `add_device.php` lui-même affiche la communauté et reçoit les secrets en arguments, lesquels sont visibles dans la liste des processus du serveur Kadupul pendant l'exécution de chaque appel.

`add_device.php` quitte avec le code 1 en cas de doublon ou d'erreur ; le script continue, compte les échecs et quitte avec le code 1 si au moins un équipement n'a pas été ajouté. Les identifiants de modèles proviennent de `php cli/add_device.php --list-host-templates`. Codes de sortie de `export` : `0` écrit, `2` entrée illisible, analyse incomplète sans `--allow-partial`, ou données ne pouvant être exportées en toute sécurité, `1` impossible d'écrire le script.

## Gestion des versions et processus de publication

hostcensus suit la [Gestion sémantique de version (SemVer)](https://semver.org/spec/v2.0.0.html) : les
correctifs compatibles incrémentent la version de correctif, les fonctionnalités compatibles et dépréciations incrémentent la
version mineure, et les changements cassant la compatibilité incrémentent la version majeure.
Les commandes et options, les codes de sortie et les schémas JSON constituent le contrat public ;
les comportements obsolètes continuent de fonctionner jusqu'à la prochaine version majeure, à moins qu'un
correctif de sécurité n'impose de les modifier plus tôt (le changelog en explique alors la raison).

release-please ouvre une PR de publication à partir des titres Conventional Commit sur `main`,
en mettant à jour `pyproject.toml`, `uv.lock` et `CHANGES.md`. Sa fusion crée le
tag `vMAJOR.MINOR.PATCH` et un brouillon de release GitHub, auquel la CI joint un
wheel testé, une archive source et des sommes de contrôle ; GitHub stocke des attestations de build pour
ces fichiers via son API d'attestations. Un mainteneur vérifie et publie le
brouillon une fois les fichiers joints. Les releases ne sont jamais remplacées.

La publication de confiance PyPI est facultative et requiert la propriété du projet, un éditeur de
confiance (`trusted publisher`) et l'environnement `pypi`. Elle publie les mêmes artefacts de release vérifiés
sans reconstruire ni stocker de jeton API. Les releases taguées dans ce dépôt
public génèrent des attestations d'artefacts GitHub ; les forks privés nécessitent un plan pris en
charge et une activation explicite. Consultez le
[guide complet de publication](../../../docs/releasing.md) pour la configuration, les commandes exactes et les nouvelles tentatives.

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

Les outils de développement se trouvent dans les groupes de dépendances [PEP 735](https://peps.python.org/pep-0735/)
dans `pyproject.toml` (`dev`, `fuzz`, `build`), afin de ne jamais apparaître dans les
métadonnées du paquet publié. `uv.lock` est l'unique fichier de verrouillage ; la CI installe avec
`uv sync --locked` et échoue si le fichier de verrouillage est obsolète. Choisissez l'interpréteur avec
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`), ou n'importe quel Python 3.12+.

La CI impose un plancher de couverture de 90 % sur le paquet. Les tests unitaires incluent des serveurs
en boucle locale contrôlés et des cas hors ligne de profils, d'historique et de validation de release ; le laboratoire Compose exécute
OpenSSH, MariaDB, nginx et net-snmp sur un bridge isolé. Exécutez-le avec
`make test-integration`. Consultez [CONTRIBUTING.md](../../../CONTRIBUTING.md) et
[l'outillage de publication](../../../scripts/README.md).

Le conteneur d'exécution tourne sous l'UID/GID 10001 sans répertoire personnel, sans shell de
connexion et sans pip, et peut écrire dans `/app/output`. Accordez à cet utilisateur l'accès en écriture à
tout répertoire de sortie monté. Il ne nécessite aucune capacité Linux et fonctionne avec un
système de fichiers racine en lecture seule ; il peut donc être exécuté ainsi :

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Nmap utilise son comportement de découverte TCP non privilégié dans ce conteneur. La CI fait échouer
la construction de l'image pour toute vulnérabilité HIGH ou CRITICAL corrigeable signalée par Trivy.

## Vérifications de la chaîne d'approvisionnement

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
s'exécute sur main et chaque semaine, publie son score réel et envoie les résultats vers GitHub
code scanning. Les Actions et les bases de conteneurs sont épinglées par des empreintes immuables ; les dépendances
Python sont résolues dans `uv.lock`. Les échecs de Bandit font échouer la CI, et un fuzzing Atheris
borné exerce les analyseurs SSH, MySQL, HTTP, de certificats et BER SNMPv3
sans accès réseau.

Scorecard mesure également l'activité historique de relecture, la diversité des contributeurs et la
provenance des releases. Ces scores reflètent des preuves réelles ; ils ne prétendent pas
que chaque critère de gouvernance ou d'historique des publications soit satisfait. Consultez
[SECURITY.md](../../../SECURITY.md) et [la provenance des releases](../../../docs/releasing.md).

## Localisation

Les messages CLI et les tableaux de résumé et de comparaison en terminal prennent en charge 45 locales (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) sans aucune dépendance d'exécution supplémentaire. La résolution suit `--lang`, puis `LC_ALL`, `LC_MESSAGES` et `LANG`, avec repli sur `en`. Les schémas JSON, les colonnes CSV et les scripts d'exportation restent inchangés dans toutes les locales.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Contribution

Les contributions doivent inclure un cas reproductible, préserver les contrats documentés de la CLI et des
formats de données, et réussir les vérifications qualité ci-dessus. Consultez
[CONTRIBUTING.md](../../../CONTRIBUTING.md) pour le workflow de développement et
[le guide de publication](../../../docs/releasing.md) pour les décisions de compatibilité et de gestion des versions.

## Sécurité et statut de licence

Consultez [SECURITY.md](../../../SECURITY.md) pour le signalement privé et les versions prises en charge.
hostcensus est distribué sous la [licence MIT](../../../LICENSE).

Les en-têtes des fichiers source utilisent des identifiants SPDX et préservent les crédits des contributeurs issus de l'historique
Git. Consultez [AUTHORS.md](../../../AUTHORS.md) pour les attributions. Les captures de test binaires et le
fichier de verrouillage généré utilisent des fichiers `.license` adjacents ; le texte de la licence MIT se trouve dans `LICENSES/MIT.txt`.
