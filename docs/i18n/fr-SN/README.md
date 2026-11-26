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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · **Français (Sénégal)** · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus est un outil en ligne de commande Python destiné à réaliser un inventaire reproductible des services sur les réseaux que vous administrez.
Il enregistre ce que les équipements exposent, compare les observations dans le temps et génère des scripts d'importation Kadupul. Le moteur par défaut utilise des sockets asyncio sans privilèges root ; la découverte optionnelle par Nmap permet d'identifier des hôtes au-delà des ports de services configurés.

## Pourquoi utiliser hostcensus

Un simple rapport de ports ponctuel n'explique pas si l'observation suivante a réellement changé ou si elle a simplement échoué. hostcensus associe des états de services explicites, des sondes bornées, des profils d'analyse réutilisables et un historique local. Les opérateurs peuvent répéter le même périmètre, examiner les erreurs et distinguer les observations incertaines des changements confirmés.

- **Preuves de services :** identification SSH, messages d'accueil MySQL, en-têtes HTTP, observations de certificats TLS et découverte SNMP ou requêtes system-MIB authentifiées.
- **Périmètre reproductible :** profils TOML nommés, exclusions cumulatives, services configurables, limites d'hôtes et de sondes, et nombre de tâches concurrentes borné.
- **Vérifications avant tout trafic :** le contrôle préalable local (preflight) valide les cibles, les outils, l'accès aux fichiers de destination, le schéma d'historique et les bundles CA TLS configurés.
- **Historique d'inventaire :** les instantanés SQLite transactionnels conservent toutes les observations ; les comparaisons gardent visibles les échecs du scanner et les états inconnus.
- **Sorties interopérables :** rapports en terminal, JSON et CSV, instantanés fichiers versionnés et scripts d'importation Kadupul.

L'intégration continue (CI) couvre Python 3.12, 3.13 et 3.14 sur Linux et macOS, ainsi qu'un laboratoire d'intégration contrôlé sous Compose. Le code s'appuie sur des alias de types modernes, des résultats de contrôle préalable typés, des profils optimisés par slots à paramètres nommés obligatoires et un nettoyage asynchrone structuré, tout en maintenant la compatibilité avec ces versions de Python. Consultez [Gestion des versions et publications](../../../docs/releasing.md) pour le contrat de compatibilité SemVer et le processus de publication sur GitHub. Le badge de version reflète les artefacts publiés et non cette copie locale : le dernier tag publié est actuellement `v0.3.0`, tandis que cette copie utilise la version de paquet `3.0.0`. Installez depuis cette copie locale pour profiter des fonctionnalités d'inventaire documentées ici.

Commencez par l'[installation](#install), puis consultez [profils et historique](#inventory-profiles-preflight-and-local-history).
Pour les détails d'intégration, voir [empreintes des services](#fingerprints), [comparaisons de fichiers](#inventory-diff) et [export Kadupul](#kadupul-export).

## Installation

Python 3.12 ou une version ultérieure est requis ; la matrice testée couvre Python 3.12 à 3.14. Depuis cette copie locale, installez les dépendances d'exécution verrouillées :

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Pour la découverte d'hôtes optionnelle via Nmap, installez l'exécutable Nmap à l'aide du gestionnaire de paquets de votre système ; aucun paquet Python supplémentaire n'est nécessaire. La sortie XML de Nmap est analysée avec defusedxml, une dépendance principale, de sorte que l'expansion d'entités XML est refusée. hostcensus exécute directement le binaire `nmap` présent dans `PATH` avec une liste d'arguments fixe, un délai limite qui augmente selon la taille du préfixe et un plafond de sortie de 64 MiB. Nmap n'est pas nécessaire pour le moteur par défaut.

## Migration depuis netprobe

hostcensus est le nouveau nom de netprobe, publié avec la version 3.0.0. Le projet n'a jamais été publié sur PyPI sous aucun des deux noms ; les installations provenaient donc d'une copie du dépôt ou d'une release GitHub. Le dépôt GitHub conserve son nom actuel.

| Avant | Maintenant | Compatibilité |
| --- | --- | --- |
| Distribution `netprobe` | `hostcensus` | Réinstallez depuis la copie locale ; il n'existe pas de paquet sous l'ancien nom. |
| Commande `netprobe` | `hostcensus` | `netprobe` fonctionne encore et affiche une ligne d'avertissement de dépréciation sur stderr. Les codes de retour et stdout restent inchangés. Supprimée dans la prochaine version majeure. |
| Variables d'environnement `NETPROBE_*` | `HOSTCENSUS_*` | Une variable `NETPROBE_*` est utilisée lorsque son équivalent `HOSTCENSUS_*` n'est pas défini, avec un avertissement sur stderr citant les noms des variables et jamais leurs valeurs. `HOSTCENSUS_*` l'emporte si les deux sont définies. Supprimées dans la prochaine version majeure. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Rupture de compatibilité.** Aucune couche de compatibilité d'import n'est installée ; mettez à jour vos imports. |
| Tag d'image Docker `network-discovery:test` (CI uniquement) et utilisateur du conteneur `netprobe` | `hostcensus:test`, utilisateur `hostcensus` | Aucune image n'a jamais été publiée sur un registre. Reconstruisez l'image et utilisez le point d'entrée `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Un fichier existant portant l'ancien nom par défaut continue d'être utilisé, avec un avertissement, tant que le nouveau nom n'existe pas. Les chemins explicites passés via `--config` et `--history` ne sont pas affectés. |
| Rapports et instantanés avec `"format": "netprobe-report"` ou `"netprobe-snapshot"`, et champ `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` et `export` chargent toujours les fichiers générés sous l'ancien nom, et les schémas JSON publiés acceptent les deux graphies. Les nouveaux fichiers utilisent les nouveaux noms. Les bases d'historique SQLite sont inchangées et se chargent comme avant. |
| Scripts Kadupul issus de `netprobe export` | Scripts issus de `hostcensus export` | Les anciens scripts continuent de fonctionner et lisent toujours `NETPROBE_SNMP_*` à l'exécution. Les nouveaux scripts lisent `HOSTCENSUS_SNMP_*`. |

## Exemple rapide

Exécuté depuis le conteneur de test du laboratoire d'intégration décrit dans la section Développement (sortie abrégée) :

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

## Codes de retour

| Commande | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | observations ou rapport enregistrés | échec du contrôle préalable, du moteur, de l'historique ou de l'écriture du rapport/instantané | cible, options, configuration ou limites invalides | - | `--deadline` atteint ; rapport partiel écrit, historique et instantané ignorés |
| `preflight` | vérifications réussies | échec d'une vérification locale | cible/configuration invalide ou destinations en conflit | - | - |
| `profiles` | profils validés listés | - | configuration ou sélection illisible ou invalide | - | - |
| `history` | résumés listés | historique manquant, invalide ou non pris en charge | options CLI invalides | - | - |
| `compare` | comparaison produite, y compris si des changements existent | historique illisible, périmètre/ordre incompatible ou échec d'écriture | options CLI invalides | - | - |
| `diff` | aucun changement | impossible d'écrire le fichier `-o` | entrée manquante, illisible ou non prise en charge, ou analyse incomplète sans `--allow-partial` | changements détectés, observations non confirmées ou analyse incomplète | - |
| `export` | script écrit | impossible d'écrire le script | entrée illisible, analyse incomplète sans `--allow-partial` ou données impossibles à exporter de manière sûre | - | - |

## Structure du projet

| Module | Rôle |
| --- | --- |
| `cli.py` | Options de commande, résolution des profils, contrôle préalable, analyse et génération de rapports |
| `scanner.py`, `probes.py` | Expansion des cibles, tâches concurrentes bornées, découverte d'hôtes et observations de services |
| `config.py`, `profiles.py` | Définitions des services et profils d'inventaire validés |
| `models.py`, `output.py` | Types de résultats et rendu terminal/JSON/CSV |
| `history.py`, `diff.py` | Historique SQLite et comparaisons d'instantanés fichiers versionnés |
| `preflight.py` | Vérifications locales et détection bornée de la version de Nmap |
| `export.py` | Scripts d'importation Kadupul validés et protégés pour le shell |

Chaque observation de service enregistre son état séparément de l'identité qu'il annonce.
Les lectures et les délais sont bornés ; les exceptions des sondes restent consignées dans les erreurs de l'hôte. L'historique SQLite utilise des transactions, une fermeture explicite des connexions ainsi que des accès en lecture seule pour le listage et la comparaison. Les secrets SNMP ne sont transmis que via des variables d'environnement ou des fichiers de secrets ; l'historique d'inventaire enregistre uniquement les paramètres effectifs non sensibles. Consultez [Architecture](../../../docs/architecture.md) pour le pipeline d'analyse, ses limites et ses frontières de confiance, ainsi que [SECURITY.md](../../../SECURITY.md#authorized-use) pour le cadre d'utilisation autorisée.


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
| `NETWORK` | CIDR, adresse IP ou nom d'hôte ; facultatif avec `--profile`. Les identifiants de zone IPv6 sont rejetés. |
| `-o, --output PATH` | Écrit un rapport. Le format suit l'extension (`.json`, `.csv`) ; les autres extensions utilisent JSON par défaut. |
| `-f, --format json\|csv\|kadupul\|auto` | Force le format du rapport. Sans effet sans `--output`. `.sh` sélectionne `kadupul`. |
| `-v, --verbose` | Active la journalisation de débogage. |
| `-q, --quiet` | Masque les résultats, la progression et les journaux d'information ; les avertissements et erreurs restent affichés sur stderr. |
| `--backend asyncio\|nmap` | Découverte d'hôtes. `asyncio` (par défaut) sonde directement les ports de services ; `nmap` lance d'abord un balayage ping nmap et nécessite l'exécutable `nmap` dans `PATH`. |
| `--timeout SECONDS` | Délai d'attente pour les sondes qui ne définissent pas leur propre budget (par défaut 1,0). Les sondes de connexion intégrées utilisent 0,3 s sauf si la table de services définit `timeout`. |
| `--concurrency N` | Nombre de sondes exécutées simultanément (par défaut 256). |
| `--deadline SECONDS` | Arrête l'ensemble de l'analyse, balayage nmap inclus, passé ce délai (par défaut 3600, au maximum 604800 ; variable `HOSTCENSUS_DEADLINE`). Les hôtes terminés sont inscrits dans le rapport avec `"complete": false`, aucun historique ni instantané n'est écrit, et `scan` retourne le code 4. |
| `--config PATH` | Définitions de services TOML et paramètres de profils nommés `[profiles]` optionnels. |
| `--profile NAME` | Utilise un profil nommé ; pointe par défaut sur `hostcensus.toml` lorsque `--config` est omis. |
| `--exclude IP/CIDR` | Ajoute une exclusion ; répétable autant que nécessaire. Un hôte IPv4 exclu exclut également les adresses IPv6 qui l'atteignent : IPv4 mappées (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) et 6to4. Les cibles et exclusions IPv4 mappées sont traitées comme les adresses IPv4 qu'elles désignent. |
| `--max-hosts N` | Limite d'adresses vérifiée avant les exclusions (valeur par défaut et plafond strict : 65 536). |
| `--history PATH` | Enregistre l'analyse terminée dans une base d'historique SQLite optionnelle. |
| `--services NAMES` | Liste de noms de services séparés par des virgules à vérifier dans cet ordre (par défaut : tous). |
| `--ports SPEC` | Liste séparée par des virgules de `NAME=PORT` (déplace un service) ou `PORT` (ajoute un contrôle TCP simple nommé `tcp-PORT`). |
| `--snmp-community-file PATH` | Fichier contenant la communauté SNMPv2c pour la requête system MIB. Variables : `HOSTCENSUS_SNMP_COMMUNITY` (valeur) ou `HOSTCENSUS_SNMP_COMMUNITY_FILE` (chemin). |
| `--snmp-user` | Utilisateur SNMPv3. Variable : `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (par défaut), `SHA224`, `SHA256`, `SHA384`, `SHA512` et fichier contenant la phrase de passe. Variables : `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` ou `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (par défaut), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` et fichier contenant la phrase de passe. Variables : `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` ou `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Écrit aussi un instantané versionné destiné à `hostcensus diff`. |
| `--tls-ca-file PATH` | Vérifie les certificats HTTPS à l'aide de ce bundle PEM au lieu du magasin système. Variable : `HOSTCENSUS_TLS_CA_FILE`. |

Par défaut, chaque hôte est vérifié pour SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) et HTTPS (TCP 443). Les ports TCP sont testés par une connexion complète. SNMP est testé par une requête de découverte de moteur SNMPv3, à laquelle tout agent SNMPv3 doit répondre sans identifiants ; les agents qui ne parlent que v1/v2c ne seront pas détectés par cette sonde. Avec le moteur asyncio, un hôte est considéré comme actif dès qu'une sonde obtient une réponse, y compris une connexion refusée ; un hôte qui ignore toutes les sondes obtient donc `alive=false` et l'erreur "Host is down", ce qui ne prouve pas qu'il soit physiquement éteint. Avec `--backend nmap`, c'est nmap qui détermine quels hôtes sont actifs (ICMP en root, TCP 80/443 sinon).

### Empreintes des services

Chaque service ouvert est identifié à partir de ce qu'il envoie avant toute authentification. Aucune sonde ne s'authentifie, à l'exception de la requête SNMP, et uniquement lorsque vous fournissez des identifiants.

| Sonde | Données lues | `version` | Clés de `details` |
| --- | --- | --- | --- |
| `ssh` | Ligne d'identification RFC 4253 | logiciel, par ex. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Handshake initial MySQL/MariaDB | version du serveur | `server_version`, `flavor`, `auth_plugin`, ou `error_code`/`error` |
| `http` | Réponse `HEAD /` | en-tête `Server` | `status`, `server` |
| `https` | Handshake TLS, certificat, `HEAD /` | en-tête `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | Découverte SNMPv3 ; avec identifiants, GET de sysDescr, sysObjectID, sysName | sysDescr | `engine_id` ; avec identifiants `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, ou `snmp_error` |

Une cible désignée par nom d'hôte est résolue une seule fois par hôte et chaque sonde se connecte à cette adresse, enregistrée sous `address` dans les résultats ; le nom est utilisé uniquement pour le SNI TLS, la vérification du certificat et l'en-tête HTTP `Host`. Un nom impossible à résoudre produit des états `unknown` et une erreur `Cannot resolve`. Les noms issus du DNS inverse ne sont conservés que s'ils contiennent uniquement des caractères valides de nom d'hôte, et au plus 16 résolutions s'exécutent simultanément. HTTPS effectue la vérification du certificat et du nom d'hôte par rapport au magasin système ou à `--tls-ca-file`. Le magasin de confiance est chargé une seule fois pour l'analyse et réutilisé pour chaque sonde HTTPS. La connexion TCP et le handshake TLS sont chronométrés séparément, si bien qu'un port qui accepte la connexion mais bloque le handshake est marqué `open` avec `tls_error`, et non `filtered`. Si la vérification échoue, le résultat enregistre `cert_verified: false` et `cert_verify_error` ; la sonde ne réessaie pas avec des paramètres moins stricts et n'envoie pas de requête HTTP. Les détails du certificat et les en-têtes HTTP ne sont collectés qu'après réussite de la vérification. Fournissez le bundle CA approprié pour les services utilisant une autorité de certification privée. Les rapports plus anciens peuvent contenir `cert_read_unverified`, que les sondes actuelles ne produisent plus.

Les secrets SNMP ne sont lus que depuis des variables d'environnement ou des fichiers (`--snmp-*-file`, ou la variable `HOSTCENSUS_SNMP_*_FILE` correspondante), jamais depuis des valeurs en ligne de commande visibles par d'autres utilisateurs locaux dans la liste des processus. `--snmp-community`, `--snmp-auth-key` et `--snmp-priv-key` passés avec une valeur quittent avec le code 2 en indiquant l'option de remplacement. Un fichier de secret doit contenir de l'UTF-8 non vide d'au plus 4096 octets ; un retour à la ligne final est ignoré, et définir à la fois une variable et un fichier pour le même secret constitue une erreur. Les messages d'erreur mentionnent le nom du fichier mais n'affichent jamais son contenu. Les rapports d'analyse et l'historique n'incluent pas intentionnellement les valeurs d'identifiants. L'exportateur dispose d'une option distincte et explicite `--include-credentials` décrite plus bas. Une communauté sélectionne SNMPv2c ; un utilisateur sélectionne SNMPv3, avec authentification lorsqu'une clé d'authentification est fournie et chiffrement (privacy) lorsque les deux clés sont fournies (`snmp_security_level` indique le niveau retenu). hostcensus refuse, avec le code de retour 2, de combiner une communauté avec un utilisateur v3, d'utiliser une clé de chiffrement sans clé d'authentification ou d'utiliser des clés sans utilisateur, et il ne réessaie jamais une requête v3 en échec avec v2c ou un niveau de sécurité inférieur. Les agents qui ne parlent que v1/v2c ignorent la découverte v3 sans identifiants et n'apparaissent donc ouverts que lorsqu'une communauté est fournie.

Le texte des bannières est ramené aux caractères imprimables et plafonné à 256 caractères avant stockage ou affichage. Les lectures sont elles aussi bornées : 4 KiB par ligne, 4 KiB pour un message d'accueil MySQL, 16 KiB d'en-têtes HTTP. Un identifiant de moteur SNMP dépassant 32 octets est tronqué avant enregistrement. HTTP et HTTPS envoient un en-tête Host avec l'adresse IPv6 entre crochets et le numéro de port lorsqu'il ne s'agit pas de 80 ou 443. Les cellules CSV commençant par un caractère déclencheur de formule de tableur sont préfixées afin que la cellule reste du texte brut.

### Limites

Une exécution accepte au maximum 65 536 adresses, 64 services et 524 288 sondes (hôtes multipliés par services) ; les demandes plus grandes quittent avec le code 2 avant tout envoi réseau. `--concurrency` est plafonné à 4096 sockets. Chaque sonde dispose d'une échéance stricte égale à quatre fois son propre budget. Les sondes de connexion (`tcp`, `ssh`, `mysql`, `http`) utilisent 0,3 seconde sauf si le service définit `timeout`. SNMP et HTTPS utilisent `--timeout` (par défaut 1,0) lorsqu'aucun délai spécifique n'est configuré. Une sonde atteignant son échéance est signalée comme `unknown` avec "probe timed out" dans `errors`. Les erreurs locales de socket (par exemple un manque de descripteurs de fichiers) sont aussi marquées `unknown` avec l'erreur enregistrée ; elles ne sont jamais comptées comme un port filtré ni comme un hôte hors ligne. Avant de sonder, hostcensus relève la limite souple de fichiers ouverts vers la limite stricte afin d'atteindre `--concurrency` plus 64 descripteurs ; en cas d'impossibilité, la vérification préalable `open files` échoue et `scan` quitte avec le code 1 avant d'envoyer du trafic. La découverte Nmap applique un délai de 30 secondes par hôte. Un préfixe est transmis à nmap au format CIDR, et un balayage échoue avec le code 1 lorsque nmap signale moins d'adresses que celles fournies (par exemple un nom qu'il ne peut pas résoudre) au lieu de marquer les hôtes comme inactifs. Une cible par nom d'hôte est résolue une fois et cette adresse est transmise à nmap, de sorte que la découverte et les sondes interrogent la même machine. Un préfixe complet s'exécute dans un seul processus nmap dont le délai d'expiration est de 35 secondes par tranche de 256 adresses, arrondi au supérieur. Les balayages comportant des exclusions utilisent des lots de 256 hôtes avec un délai de 35 secondes par lot. La création des tâches concurrentes est bornée indépendamment de la taille de la plage. Le DNS inverse et la résolution de noms disposent d'un délai distinct de deux secondes ; un appel de résolution qui ne rend jamais la main est abandonné dans son propre thread afin de ne pas bloquer hostcensus au-delà de ces limites. Au plus 16 résolutions s'exécutent en parallèle, et un appel abandonné conserve son créneau jusqu'à son retour, ce qui maintient borné le nombre de threads bloqués ; si les 16 se figent, les résolutions suivantes attendent un créneau en dehors du délai de deux secondes (qui démarre une fois un créneau libéré) jusqu'à ce que `--deadline` arrête l'analyse. Utilisé comme bibliothèque sans `deadline`, `NetworkScanner` peut attendre un tel créneau indéfiniment. `--deadline` (une heure par défaut) borne l'ensemble de l'exécution au-dessus de toutes ces limites.

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

`probe` prend l'une des valeurs `tcp`, `ssh`, `mysql`, `http`, `https` ou `snmp` et reprend par défaut le nom du service s'il correspond à une sonde, sinon `tcp`. Seul `snmp` utilise UDP. Les noms de services se composent de lettres minuscules, chiffres, `-` et `_`. Deux services ne peuvent pas partager le même port et le même protocole ; l'historique enregistre un seul état pour cette paire. `timeout` est optionnel, exprimé en secondes, et vaut au minimum 0,05. Les sondes de type connexion (`tcp`, `ssh`, `mysql`, `http`) utilisent 0,3 seconde par défaut. `snmp` et `https` reprennent le `--timeout` de l'analyse si le service ne définit pas `timeout`. `--timeout` ne remplace pas un budget déjà défini au niveau du service.

Les rapports JSON sont des documents versionnés (`"format": "hostcensus-report"`, `"version": 1`) qui enregistrent la cible, les services sondés et les paramètres aux côtés de `devices` ; `--format json` sans `-o` écrit le rapport sur stdout à la place du tableau. Chaque sortie JSON dispose d'un schéma publié ; voir [Sortie JSON](../../../docs/json-output.md). Les équipements conservent les champs d'origine `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` et `errors`, et ajoutent une liste `services` contenant pour chaque sonde `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered`, ou `unknown` lorsque la sonde a échoué localement ou dépassé son échéance), `version` et `details`. La sortie CSV ajoute en fin de ligne les colonnes `services` et `versions` pour les services ouverts. Les booléens `ssh`, `snmp` et `mysql` suivent les services portant exactement ces noms.


## Profils d'inventaire, contrôle préalable et historique local

Les profils nommés partagent le même fichier TOML que les définitions `[services]` existantes. Copiez [hostcensus.example.toml](../../../hostcensus.example.toml) vers `hostcensus.toml` et indiquez les réseaux que vous administrez :

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

`preflight` résout les options et les profils exactement comme `scan`, y compris `--concurrency` pour la vérification des fichiers ouverts ; un contrôle préalable réussi garantit donc que `scan` démarrera avec le même plan d'exécution.

Les profils acceptent `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`, `concurrency` et `max_hosts`. `services` et `ports` utilisent la syntaxe habituelle en liste séparée par des virgules. Les options CLI explicites remplacent les réglages du profil ; les options `--exclude` répétées s'ajoutent aux exclusions du profil. Un réseau indiqué explicitement avec `--profile` doit être inclus dans le périmètre IP/CIDR de ce profil. Les noms d'hôtes restent pris en charge pour les analyses directes, mais ne peuvent pas être combinés avec des exclusions IP. Les limites d'hôtes s'appliquent avant les exclusions ; le plafond total de sondes reste appliqué après. Les hôtes exclus sont écartés aussi bien des contrôles de services que de la découverte Nmap optionnelle.

Chaque analyse effectue des vérifications préalables locales avant tout trafic vers les cibles : limites de cibles et de sondes, accès aux destinations, disponibilité optionnelle de l'exécutable ou wrapper Nmap, schéma de l'historique et bundle CA TLS configuré. `preflight` renvoie du JSON et ne sonde aucune cible ni ne crée de base d'historique. Il crée temporairement un fichier voisin pour tester l'accès en écriture sans modifier les fichiers existants. Le moteur asyncio par défaut ne requiert toujours ni Nmap ni droits root. Les chemins de destination doivent être distincts les uns des autres ainsi que de la configuration d'entrée, y compris via des liens matériels ; les liens symboliques en destination sont refusés. Un échec de vérification retourne 1 ; un périmètre ou une configuration invalide retourne 2.

L'écriture des rapports et des exports exige la prise en charge de `O_NOFOLLOW`. Sur les plateformes qui ne le proposent pas, dont Windows, ces écritures échouent sans ouvrir ni tronquer la destination. Les nouveaux rapports et scripts d'export sont accessibles uniquement au propriétaire (mode 0600) ; remplacer un fichier existant conserve ses permissions. Écrire dans un tube nommé sans lecteur échoue immédiatement au lieu de bloquer. Une nouvelle base `--history` est aussi créée en accès propriétaire uniquement ; une base existante garde son mode. Les messages de journalisation vont toujours sur stderr afin que stdout ne contienne que les résultats. Les exports contenant des identifiants forcent toujours le mode 0600.

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

Utilisez les identifiants fournis par `history` ; l'exemple suppose une base neuve. Les instantanés sont stockés de manière transactionnelle avec les horodatages UTC de début et de fin, la version du paquet, les paramètres effectifs non sensibles, les résumés et l'ensemble des observations d'hôtes et de services, y compris les erreurs par hôte. Les observations partielles d'hôtes sont conservées. Les exécutions annulées ne sont pas enregistrées. Les contrats existants de rapports, instantanés, exports et codes de retour de `scan` sont préservés.

`history` liste les résumés JSON sans relire l'intégralité des données historiques des équipements. `compare` lit deux analyses sauvegardées, exige des identités de cibles et des ports sélectionnés identiques, et signale les changements de réactivité, d'état et d'ouverture de ports. L'identifiant de l'analyse antérieure doit précéder celui de la plus récente. Lorsque les deux analyses ont enregistré `timeout` ou `backend` avec des valeurs différentes, le rapport affiche un avertissement tout en comparant les observations. Un délai différent peut en effet faire apparaître comme ouvert un port auparavant filtré. Les erreurs du scanner et les observations de ports inconnues sont signalées comme incertaines plutôt que traitées comme une disparition ou une fermeture confirmée : les hôtes en erreur apparaissent dans `uncertain_hosts`, et toute transition de port impliquant `unknown` (y compris inconnu dans les deux analyses) figure dans `unconfirmed_ports` plutôt que dans `port_changes`, sauf pour un port ouvert dans l'analyse la plus récente, qui constitue bien un changement de port. `compare` et `diff` appliquent la même règle de classification des ports. `no_longer_responding` signifie une absence de réponse, et non la preuve que l'équipement a été retiré. Un code de retour 0 de `scan` ne garantit pas que tous les hôtes ont répondu : vérifiez les erreurs par hôte. Une comparaison réussie retourne 0 qu'il y ait ou non des changements ; la commande `diff` sur fichiers conserve son contrat de code de retour 3. Un historique non pris en charge ou corrompu retourne 1.

L'historique stocke des informations d'inventaire ; choisissez donc un répertoire local convenablement protégé. Les fichiers de profils et les paramètres stockés ne contiennent pas d'identifiants SNMP ; la gestion des identifiants passe toujours par les options d'exécution et les variables d'environnement existantes.

## Comparaison d'inventaire (diff)

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Un instantané est un fichier JSON contenant `format: "hostcensus-snapshot"`, `version: 1`, la version de hostcensus, l'horodatage UTC de création, la cible, le `timeout` et le `backend` lorsque l'analyse les a enregistrés, les services sondés et les hôtes actifs au même format que le rapport `-o`. Les hôtes hors ligne ne sont pas inclus. `diff` accepte également les rapports JSON simples issus de `scan -o`, y compris ceux générés avant l'ajout du champ `services`.

`diff` signale les hôtes apparus et disparus, les ports ouverts ou fermés sur les hôtes présents dans les deux fichiers, ainsi que les services dont `version` a changé. Les ports sondés dans une seule des deux analyses ne sont pas comparés, ce qu'indique un avertissement. Les observations en échec ne sont jamais interprétées comme une absence de changement : un port `unknown` dans l'une des deux analyses et non ouvert dans la seconde figure dans `unconfirmed`, et non dans `closed`, avec `before` valant `open`, `unknown` ou `not-open` (sondé et fermé ou filtré) et `after` valant `unknown` ou `not-open` ; un port désormais ouvert est rapporté dans `opened` même si la sonde précédente avait échoué. Un hôte dont toutes les sondes ont échoué sans réponse dans l'une des deux analyses apparaît dans `unsettled_hosts` (avec `before`/`after` valant `up`, `uncertain` ou `absent`, y compris s'il a échoué dans les deux analyses ou s'il manque dans l'autre fichier) plutôt que dans `vanished_hosts` ; s'il répond dans la seconde analyse, il est aussi signalé comme nouvel hôte avec ses ports ouverts. C'est pour cette raison que les instantanés conservent ces hôtes en échec. Un avertissement s'affiche aussi si les cibles diffèrent, ou si les deux fichiers ont enregistré un délai d'attente ou un moteur différent. `-o PATH` écrit également le résultat JSON dans un fichier.

Un rapport issu d'une analyse interrompue par `--deadline` (`"complete": false`) ne liste que les hôtes atteints avant l'arrêt ; `diff` et `export` le refusent donc avec le code de retour 2. `--allow-partial` l'accepte avec un avertissement sur stderr : `diff` place alors les hôtes totalement absents de l'analyse incomplète dans `unsettled_hosts` avec l'état `unscanned` au lieu de les déclarer disparus (un hôte indiqué comme hors ligne reste considéré disparu), positionne `partial` à true et ne renvoie jamais « aucun changement », tandis que `export` ajoute un avertissement dans l'en-tête du script.

Codes de retour de `diff` : `0` aucun changement, `3` changements détectés, observations impossibles à confirmer ou entrée incomplète (`changed` vaut true dès qu'une liste quelconque, y compris `unsettled_hosts` et `unconfirmed`, est non vide, ou lorsque `partial` vaut true), `2` fichier manquant, illisible, instantané non pris en charge ou incomplet sans `--allow-partial`, `1` impossible d'écrire le fichier `-o`.

## Export vers Kadupul

[Kadupul](https://github.com/kadupulhq/kadupul) (un fork de Cacti 1.2.31) ne propose pas d'import en masse d'équipements par fichier. Sa méthode officielle pour ajouter des équipements par script est `cli/add_device.php`, un équipement par appel, avec des arguments `--option=value`. `hostcensus export` génère un script POSIX `sh` regroupant ces appels :

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Chaque hôte actif devient `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...` :

- Les hôtes pour lesquels la requête SNMP de l'analyse a réussi reçoivent `--version=2 --community=...` ou `--version=3 --username=... --authproto=... --password=...` (plus `--privproto`/`--privpass` pour authPriv), `--port` et `--avail=snmp`. L'export SNMPv3 requiert `--snmp-user`, et noAuthNoPriv est refusé car `add_device.php` exige un mot de passe v3.
- Les autres hôtes reçoivent `--version=0 --avail=ping`, avec `--ping_method=tcp --ping_port=` pointant sur le premier port TCP ouvert, ou ICMP s'il n'y en a aucun.
- `--notes` liste les services ouverts et leurs versions. `--description` reprend le nom DNS inverse lorsqu'il est simple (lettres, chiffres, `.`, `_`, `-`), sinon l'adresse IP, et est rendu unique car `add_device.php` traite une description existante comme une mise à jour de l'équipement concerné.

Chaque valeur est validée et protégée pour le shell avec `shlex.quote`. Par défaut, aucun secret SNMP n'est écrit dans le fichier : le script développe `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` ou `HOSTCENSUS_SNMP_PRIV_KEY` à l'exécution et s'arrête si l'une d'elles manque. `--include-credentials` écrit à la place les valeurs issues de ces variables d'environnement directement dans le script, le crée en mode 0600 et affiche un avertissement. `add_device.php` affiche lui-même la communauté et reçoit les secrets en arguments, qui sont visibles dans la liste des processus du serveur Kadupul pendant l'exécution de chaque appel.

`add_device.php` retourne 1 en cas de doublon ou d'erreur ; le script poursuit l'exécution, comptabilise les échecs et retourne 1 si au moins un équipement n'a pas pu être ajouté. Les identifiants de modèles proviennent de `php cli/add_device.php --list-host-templates`. Codes de retour d'`export` : `0` écriture réussie, `2` entrée illisible, analyse incomplète sans `--allow-partial` ou données impossibles à exporter de manière sûre, `1` échec d'écriture du script.

## Gestion des versions et processus de publication

hostcensus suit [Semantic Versioning](https://semver.org/spec/v2.0.0.html) : les correctifs compatibles incrémentent la version patch, les fonctionnalités compatibles et dépréciations incrémentent la version mineure, et les changements cassant la compatibilité incrémentent la version majeure. Les commandes et options, les codes de retour ainsi que les schémas JSON constituent le contrat public ; les comportements dépréciés continuent de fonctionner jusqu'à la prochaine version majeure, sauf si un correctif de sécurité impose de les modifier plus tôt (auquel cas le journal des changements en explique la raison).

release-please ouvre une pull request de publication à partir des titres Conventional Commit sur `main`, en mettant à jour `pyproject.toml`, `uv.lock` et `CHANGES.md`. Sa fusion crée le tag `vMAJOR.MINOR.PATCH` et un brouillon de release GitHub auquel la CI joint une wheel testée, une archive source et les sommes de contrôle ; GitHub stocke les attestations de build de ces fichiers via son API d'attestations. Un mainteneur vérifie puis publie le brouillon une fois les fichiers joints. Une release n'est jamais remplacée.

La publication de confiance (trusted publishing) sur PyPI est optionnelle et nécessite la propriété du projet, un éditeur de confiance et l'environnement `pypi`. Elle publie les mêmes artefacts vérifiés sans reconstruire ni stocker de jeton API. Les releases taguées de ce dépôt public génèrent des attestations d'artefacts GitHub ; les forks privés nécessitent une offre compatible et une activation explicite. Consultez le [guide complet de publication](../../../docs/releasing.md) pour la configuration, les commandes exactes et les procédures de reprise.

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

Les outils de développement résident dans les groupes de dépendances [PEP 735](https://peps.python.org/pep-0735/) de `pyproject.toml` (`dev`, `fuzz`, `build`), afin qu'ils n'apparaissent jamais dans les métadonnées du paquet publié. `uv.lock` est l'unique fichier de verrouillage ; la CI installe avec `uv sync --locked` et échoue si ce fichier n'est pas à jour. Sélectionnez l'interpréteur via `uv python`, mise (`mise exec python@3.14 -- uv sync --locked`) ou tout interpréteur Python 3.12+.

La CI impose un seuil minimal de 90 % de couverture de code sur le paquet. Les tests unitaires incluent des serveurs sur l'interface de bouclage (loopback) ainsi que des cas hors ligne pour les profils, l'historique et la validation des releases ; le laboratoire Compose exécute OpenSSH, MariaDB, nginx et net-snmp sur un pont réseau isolé. Lancez-le avec `make test-integration`. Consultez [CONTRIBUTING.md](../../../CONTRIBUTING.md) et [les outils de publication](../../../scripts/README.md).

Le conteneur d'exécution tourne sous l'UID/GID 10001 sans répertoire personnel, sans shell de connexion et sans pip, et peut écrire dans `/app/output`. Accordez à cet utilisateur un accès en écriture sur tout répertoire de sortie monté. Il ne demande aucune capacité système (capability) et fonctionne avec un système de fichiers racine en lecture seule ; il peut donc être lancé ainsi :

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

Dans ce conteneur, Nmap emploie son mode de découverte TCP sans privilèges. La CI fait échouer la construction de l'image dès que Trivy détecte une vulnérabilité corrigible de niveau HIGH ou CRITICAL.

## Vérifications de la chaîne d'approvisionnement

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool) s'exécute sur main et chaque semaine, publie son score réel et envoie les résultats vers GitHub code scanning. Les actions et les images de base des conteneurs sont épinglées par empreintes immuables ; les dépendances Python sont résolues dans `uv.lock`. Toute alerte Bandit fait échouer la CI, et un fuzzing borné avec Atheris teste les analyseurs SSH, MySQL, HTTP, certificats et BER SNMPv3 sans accès réseau.

Scorecard évalue également l'historique des revues de code, la diversité des contributeurs et la provenance des releases. Ces scores reflètent des éléments factuels et ne prétendent pas que chaque contrôle de gouvernance ou de release historique soit satisfait. Voir [SECURITY.md](../../../SECURITY.md) et [provenance des releases](../../../docs/releasing.md).

## Localisation

Les messages CLI ainsi que les tableaux récapitulatifs et de comparaison dans le terminal prennent en charge 45 locales (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) sans aucune dépendance d'exécution supplémentaire. La résolution suit `--lang`, puis `LC_ALL`, `LC_MESSAGES` et `LANG`, avec repli sur `en`. Les schémas JSON, les colonnes CSV et les scripts d'export restent identiques dans toutes les locales.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Contribution

Les contributions doivent inclure un cas reproductible, respecter les contrats documentés de la CLI et des formats de données, et passer l'ensemble des contrôles qualité ci-dessus. Consultez [CONTRIBUTING.md](../../../CONTRIBUTING.md) pour le flux de développement et [le guide de publication](../../../docs/releasing.md) pour les décisions liées à la compatibilité et au versionnage.

## Sécurité et licence

Consultez [SECURITY.md](../../../SECURITY.md) pour le signalement privé et les versions prises en charge.
hostcensus est distribué sous [licence MIT](../../../LICENSE).

Les en-têtes des fichiers sources utilisent des identifiants SPDX et préservent les crédits des contributeurs issus de l'historique Git. Voir [AUTHORS.md](../../../AUTHORS.md) pour les attributions. Les captures de tests binaires et le fichier de verrouillage généré disposent de fichiers `.license` adjacents ; le texte de la licence MIT se trouve dans `LICENSES/MIT.txt`.
