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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · **Português (BR)** · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

hostcensus é uma CLI em Python para inventário repetível de serviços em redes que você administra.
Ele registra o que os dispositivos expõem, compara observações ao longo do tempo e gera
scripts de importação para o Kadupul. O backend padrão usa sockets asyncio sem root;
a descoberta opcional com Nmap pode identificar hosts além das portas de serviço configuradas.

## Por que o hostcensus

Um relatório pontual de portas não explica se a observação seguinte mudou ou
simplesmente falhou. O hostcensus combina estados explícitos de serviço, sondagens limitadas, perfis
de varredura reutilizáveis e histórico local. Operadores podem repetir o mesmo escopo, inspecionar
erros e distinguir observações incertas de alterações confirmadas.

- **Evidências de serviço:** identificação SSH, saudações MySQL, cabeçalhos HTTP, observações
  de certificados TLS e descoberta SNMP ou consultas autenticadas à system-MIB.
- **Escopo repetível:** perfis TOML nomeados, exclusões aditivas, serviços
  configuráveis, limites de hosts/sondagens e workers limitados.
- **Verificações antes do tráfego:** o preflight local valida alvos, ferramentas, acesso
  ao destino, esquema de histórico e pacotes de CA TLS configurados.
- **Histórico de inventário:** snapshots transacionais em SQLite retêm todas as observações;
  as comparações mantêm falhas do scanner e estados desconhecidos visíveis.
- **Saída interoperável:** relatórios no terminal, JSON e CSV, snapshots versionados em arquivo
  e scripts de importação para o Kadupul.

A CI cobre Python 3.12, 3.13 e 3.14 no Linux e no macOS, além de um laboratório de integração
controlado com Compose. O código usa aliases de tipo modernos, resultados de preflight tipados,
perfis com slots somente por palavra-chave e limpeza assíncrona estruturada, mantendo compatibilidade com essas
versões do runtime. Consulte [Versionamento e lançamentos](../../../docs/releasing.md) para o contrato de
compatibilidade SemVer e o processo de release no GitHub. O badge de release descreve
artefatos publicados, não o checkout: a tag publicada mais recente é atualmente
`v0.3.0`, enquanto este checkout usa a versão de pacote `3.0.0`. Instale a partir do checkout
para usar os recursos de inventário documentados aqui.

Comece pela [instalação](#install) e, em seguida, veja [perfis e histórico](#inventory-profiles-preflight-and-local-history).
Para detalhes de integração, consulte [impressões digitais de serviços](#fingerprints),
[comparação de arquivos](#inventory-diff) e [exportação para o Kadupul](#kadupul-export).

## Instalação

É necessário Python 3.12 ou superior; a matriz testada é Python 3.12 a 3.14. A partir deste
checkout, instale as dependências de runtime travadas:

```bash
uv sync --locked
uv run hostcensus --help
uv run hostcensus --version
uv run hostcensus preflight 127.0.0.1
uv run hostcensus scan 127.0.0.1 --services ssh -o loopback.json
```

Para a descoberta opcional de hosts com Nmap, instale o executável do Nmap usando o gerenciador de pacotes
da sua plataforma; nenhum pacote Python adicional é necessário. A saída XML do Nmap é analisada com
defusedxml, uma dependência principal, portanto a expansão de entidades é recusada. O hostcensus executa
o `nmap` encontrado no `PATH` diretamente com uma lista fixa de argumentos, um prazo limite que cresce
com o tamanho do prefixo e um limite de saída de 64 MiB. O Nmap não é necessário para o backend padrão.

## Migrando do netprobe

hostcensus é o novo nome do netprobe, lançado na versão 3.0.0. O projeto nunca foi
publicado no PyPI sob nenhum dos dois nomes, então as instalações vieram de um checkout ou de uma release
do GitHub. O repositório do GitHub mantém seu nome.

| Era | Agora | Compatibilidade |
| --- | --- | --- |
| Distribuição `netprobe` | `hostcensus` | Reinstale a partir do checkout; não há pacote com o nome antigo. |
| Comando `netprobe` | `hostcensus` | `netprobe` ainda executa e imprime uma linha de descontinuação no stderr. Códigos de saída e stdout permanecem inalterados. Será removido na próxima versão principal. |
| Variáveis de ambiente `NETPROBE_*` | `HOSTCENSUS_*` | Uma variável `NETPROBE_*` é usada quando sua equivalente `HOSTCENSUS_*` não está definida, com um aviso no stderr que nomeia as variáveis e nunca seus valores. `HOSTCENSUS_*` prevalece quando ambas estão definidas. Será removido na próxima versão principal. |
| `import netprobe`, `python -m netprobe` | `import hostcensus`, `python -m hostcensus` | **Incompatível.** Nenhum shim de importação é instalado; atualize os imports. |
| Tag de imagem Docker `network-discovery:test` (apenas CI) e usuário de contêiner `netprobe` | `hostcensus:test`, usuário `hostcensus` | Nenhuma imagem de registro foi publicada. Construa a imagem novamente e use o entrypoint `hostcensus`. |
| `netprobe.toml`, `netprobe-history.sqlite3` | `hostcensus.toml`, `hostcensus-history.sqlite3` | Um arquivo existente com o nome padrão antigo ainda é usado, com um aviso, enquanto o novo nome não existir. Caminhos explícitos de `--config` e `--history` não são afetados. |
| Relatórios e snapshots com `"format": "netprobe-report"` ou `"netprobe-snapshot"`, e o campo `netprobe_version` | `hostcensus-report`, `hostcensus-snapshot`, `hostcensus_version` | `diff` e `export` ainda carregam arquivos gravados com o nome antigo, e os JSON Schemas publicados aceitam ambas as grafias. Novos arquivos usam os novos nomes. Bancos de dados de histórico SQLite permanecem inalterados e carregam como antes. |
| Scripts Kadupul de `netprobe export` | Scripts de `hostcensus export` | Scripts antigos continuam funcionando e ainda leem `NETPROBE_SNMP_*` quando executados. Novos scripts leem `HOSTCENSUS_SNMP_*`. |

## Exemplo rápido

Execute a partir do contêiner tester do laboratório de integração descrito em Desenvolvimento; saída resumida:

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

## Códigos de saída

| Comando | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `scan` | observações/relatório registrados | falha no preflight/backend, histórico ou gravação de relatório/snapshot | alvo, opções, configuração ou limites inválidos | - | `--deadline` atingido; relatório parcial gravado, histórico e snapshot ignorados |
| `preflight` | verificações aprovadas | verificação local falhou | alvo/configuração inválidos ou destinos conflitantes | - | - |
| `profiles` | perfis validados listados | - | configuração ou seleção ilegível/inválida | - | - |
| `history` | resumos listados | histórico ausente, inválido ou não suportado | opções de CLI inválidas | - | - |
| `compare` | comparação gerada, inclusive quando há alterações | histórico ilegível, escopo/ordem incompatíveis ou falha de gravação | opções de CLI inválidas | - | - |
| `diff` | sem alterações | arquivo `-o` não pôde ser gravado | entrada ausente, ilegível ou não suportada, ou varredura incompleta sem `--allow-partial` | alterações encontradas, observações não confirmadas ou varredura incompleta | - |
| `export` | script gravado | script não pôde ser gravado | entrada ilegível, varredura incompleta sem `--allow-partial` ou dados que não podem ser exportados com segurança | - | - |

## Estrutura

| Módulo | Responsabilidade |
| --- | --- |
| `cli.py` | Opções de comando, resolução de perfis, preflight, varredura e relatórios |
| `scanner.py`, `probes.py` | Expansão de alvos, workers limitados, descoberta de hosts e observações de serviços |
| `config.py`, `profiles.py` | Definições de serviços e perfis de inventário validados |
| `models.py`, `output.py` | Tipos de resultado e renderização no terminal/JSON/CSV |
| `history.py`, `diff.py` | Histórico SQLite e comparações de snapshots versionados em arquivo |
| `preflight.py` | Verificações locais e consulta limitada da versão do Nmap |
| `export.py` | Scripts de importação do Kadupul validados e com escape de shell |

Cada observação de serviço registra seu estado separadamente da identidade anunciada.
Leituras e prazos são limitados; exceções de sondagem permanecem nos erros do host. O histórico
SQLite usa transações, limpeza explícita de conexões e caminhos de listagem e comparação somente
leitura. Segredos SNMP entram apenas por variáveis de ambiente ou arquivos de segredo; o histórico de
inventário armazena as configurações efetivas não secretas. Consulte
[Arquitetura](../../../docs/architecture.md) para o pipeline de varredura, seus limites e fronteiras de confiança,
e [SECURITY.md](../../../SECURITY.md#authorized-use) para uso autorizado.


## Uso

Faça varreduras apenas em redes que você administra.

```bash
hostcensus scan 192.168.1.0/24              # table of alive hosts
hostcensus scan 192.168.1.1 -o results.json # JSON report
hostcensus scan 10.0.0.0/24 -o report.csv   # CSV report
hostcensus scan 10.0.0.0/24 -q -o out.json  # no table, file only
hostcensus scan 10.0.0.0/24 --format json | jq '.devices[]'  # JSON report on stdout
```

| Opção | Significado |
| --- | --- |
| `NETWORK` | CIDR, IP ou hostname; opcional com `--profile`. Identificadores de escopo IPv6 são rejeitados. |
| `-o, --output PATH` | Grava um relatório. O formato segue a extensão (`.json`, `.csv`); outras extensões usam JSON como fallback. |
| `-f, --format json\|csv\|kadupul\|auto` | Força o formato do relatório. Não tem efeito sem `--output`. `.sh` seleciona `kadupul`. |
| `-v, --verbose` | Registro de depuração. |
| `-q, --quiet` | Suprime resultados, progresso e logs informativos; avisos e erros ainda aparecem no stderr. |
| `--backend asyncio\|nmap` | Descoberta de hosts. `asyncio` (padrão) sonda as portas de serviço diretamente; `nmap` executa primeiro uma varredura ping do nmap e exige o executável `nmap` no `PATH`. |
| `--timeout SECONDS` | Espera para sondagens que não definem seu próprio orçamento (padrão 1.0). Sondagens de conexão integradas usam 0.3s, a menos que a tabela de serviços defina `timeout`. |
| `--concurrency N` | Sondagens simultâneas em andamento (padrão 256). |
| `--deadline SECONDS` | Interrompe toda a varredura, incluindo a varredura nmap, após esse tempo (padrão 3600, no máximo 604800; env `HOSTCENSUS_DEADLINE`). Hosts que terminaram são gravados no relatório com `"complete": false`, nenhum histórico ou snapshot é gravado e `scan` sai com código 4. |
| `--config PATH` | Definições de serviço TOML e configurações nomeadas opcionais em `[profiles]`. |
| `--profile NAME` | Usa um perfil nomeado; o padrão é `hostcensus.toml` quando `--config` é omitido. |
| `--exclude IP/CIDR` | Adiciona uma exclusão; repita conforme necessário. Um host IPv4 excluído também exclui os endereços IPv6 que o alcançam: mapeados para IPv4 (`::ffff:a.b.c.d`), NAT64 (`64:ff9b::/96`) e 6to4. Alvos e exclusões mapeados para IPv4 são tratados como os endereços IPv4 que denotam. |
| `--max-hosts N` | Limite de endereços verificado antes das exclusões (padrão/máximo rígido 65.536). |
| `--history PATH` | Registra a varredura concluída em um banco de dados de histórico SQLite opcional. |
| `--services NAMES` | Lista separada por vírgulas de nomes de serviços a verificar, nessa ordem (padrão: todos). |
| `--ports SPEC` | Lista separada por vírgulas de `NAME=PORT` (move um serviço) ou `PORT` (adiciona uma verificação TCP simples chamada `tcp-PORT`). |
| `--snmp-community-file PATH` | Arquivo com a community SNMPv2c para a consulta da MIB do sistema. Env: `HOSTCENSUS_SNMP_COMMUNITY` (o valor) ou `HOSTCENSUS_SNMP_COMMUNITY_FILE` (o caminho). |
| `--snmp-user` | Usuário SNMPv3. Env: `HOSTCENSUS_SNMP_USER`. |
| `--snmp-auth-protocol`, `--snmp-auth-key-file PATH` | `MD5`, `SHA` (padrão), `SHA224`, `SHA256`, `SHA384`, `SHA512` e um arquivo contendo a senha. Env: `HOSTCENSUS_SNMP_AUTH_PROTOCOL`, `HOSTCENSUS_SNMP_AUTH_KEY` ou `HOSTCENSUS_SNMP_AUTH_KEY_FILE`. |
| `--snmp-priv-protocol`, `--snmp-priv-key-file PATH` | `DES`, `AES` (padrão), `AES128`, `AES192`, `AES192C`, `AES256`, `AES256C` e um arquivo contendo a senha. Env: `HOSTCENSUS_SNMP_PRIV_PROTOCOL`, `HOSTCENSUS_SNMP_PRIV_KEY` ou `HOSTCENSUS_SNMP_PRIV_KEY_FILE`. |
| `--save-snapshot PATH` | Também grava um snapshot versionado para `hostcensus diff`. |
| `--tls-ca-file PATH` | Verifica certificados HTTPS com este pacote PEM em vez do armazenamento do sistema. Env: `HOSTCENSUS_TLS_CA_FILE`. |

Por padrão, cada host é verificado quanto a SSH (TCP 22), SNMP (UDP 161), MySQL (TCP 3306), HTTP (TCP 80) e HTTPS (TCP 443). Portas TCP são testadas com uma conexão completa. SNMP é testado com uma requisição de descoberta de engine SNMPv3, que qualquer agente SNMPv3 deve responder sem credenciais; agentes que falam apenas v1/v2c não serão detectados por essa sondagem. Com o backend asyncio, um host é considerado ativo quando qualquer sondagem obtém uma resposta, incluindo uma conexão recusada, portanto um host que descarta todas as sondagens recebe `alive=false` e o erro "Host is down"; isso não prova que ele esteja fisicamente desligado. Com `--backend nmap`, o nmap decide quais hosts estão ativos (ICMP como root, TCP 80/443 caso contrário).

### Impressões digitais

Cada serviço aberto recebe uma impressão digital a partir do que ele envia antes de qualquer login. Nada se autentica, exceto a consulta SNMP, e somente quando você fornece credenciais.

| Sondagem | Lê | `version` | Chaves de `details` |
| --- | --- | --- | --- |
| `ssh` | Linha de identificação RFC 4253 | software, ex. `OpenSSH_10.0` | `protocol`, `software`, `comments` |
| `mysql` | Handshake inicial do MySQL/MariaDB | versão do servidor | `server_version`, `flavor`, `auth_plugin`, ou `error_code`/`error` |
| `http` | Resposta `HEAD /` | Cabeçalho `Server` | `status`, `server` |
| `https` | Handshake TLS, certificado, `HEAD /` | Cabeçalho `Server` | `tls_version`, `cert_verified`, `cert_verify_error`, `cert_subject`, `cert_issuer`, `cert_sans`, `cert_not_before`, `cert_not_after` (UTC ISO 8601), `cert_self_signed`, `status`, `server` |
| `snmp` | Descoberta SNMPv3; com credenciais, GET de sysDescr, sysObjectID, sysName | sysDescr | `engine_id`; com credenciais `snmp_version`, `sys_descr`, `sys_object_id`, `sys_name`, ou `snmp_error` |

Um alvo de hostname é resolvido uma vez por host e toda sondagem se conecta a esse endereço, registrado como `address` nos resultados; o nome é usado apenas para TLS SNI, verificação de certificado e o cabeçalho HTTP `Host`. Um nome que não resolve resulta em estados `unknown` e um erro `Cannot resolve`. Nomes de DNS reverso são mantidos apenas quando contêm caracteres de hostname, e no máximo 16 consultas são executadas simultaneamente. HTTPS usa verificação de certificado e hostname contra o armazenamento do sistema ou `--tls-ca-file`. O armazenamento confiável é carregado uma vez para a varredura e reutilizado em cada sondagem HTTPS. A conexão TCP e o handshake TLS têm tempos medidos separadamente, portanto uma porta que aceita conexões mas trava no handshake é `open` com `tls_error`, não `filtered`. Se a verificação falhar, o resultado registra `cert_verified: false` e `cert_verify_error`; ele não tenta novamente com configurações mais fracas nem envia uma requisição HTTP. Detalhes do certificado e cabeçalhos HTTP são coletados somente após a verificação ser bem-sucedida. Forneça o pacote de CA correto para serviços com CA privada. Relatórios mais antigos podem conter `cert_read_unverified`, que as sondagens atuais não produzem mais.

Segredos SNMP são lidos apenas de variáveis de ambiente ou de arquivos (`--snmp-*-file`, ou a variável `HOSTCENSUS_SNMP_*_FILE` correspondente), nunca de valores na linha de comando, que outros usuários locais podem ver na lista de processos. `--snmp-community`, `--snmp-auth-key` e `--snmp-priv-key` com um valor encerram com código 2 e informam a alternativa correta. Um arquivo de segredo deve ser UTF-8 não vazio com no máximo 4096 bytes; uma quebra de linha final é ignorada, e definir tanto uma variável quanto um arquivo para o mesmo segredo gera um erro. Erros informam o arquivo, mas nunca imprimem seu conteúdo. Relatórios de varredura e histórico não incluem intencionalmente valores de credenciais. O exportador tem uma opção separada e explícita `--include-credentials` descrita abaixo. Uma community seleciona SNMPv2c; um usuário seleciona SNMPv3, com autenticação quando uma chave de autenticação é fornecida e privacidade quando ambas as chaves são fornecidas (`snmp_security_level` registra qual nível foi usado). O hostcensus recusa, com código de saída 2, combinar uma community com um usuário v3, usar uma chave de privacidade sem uma chave de autenticação ou usar chaves sem um usuário, e nunca tenta novamente uma consulta v3 com falha usando v2c ou um nível de segurança inferior. Agentes que falam apenas v1/v2c ignoram a descoberta v3 sem credenciais, portanto aparecem como abertos apenas quando uma community é fornecida.

O texto do banner é reduzido a caracteres imprimíveis e limitado a 256 caracteres antes de ser armazenado ou exibido. As leituras também são limitadas: 4 KiB por linha, 4 KiB para uma saudação MySQL, 16 KiB de cabeçalhos HTTP. Um engine ID SNMP maior que 32 octetos é truncado antes de ser armazenado. HTTP e HTTPS enviam um cabeçalho Host com um endereço IPv6 entre colchetes e com a porta quando ela não é 80 ou 443. Células CSV que começam com um gatilho de fórmula de planilha recebem um prefixo para que a célula permaneça como texto.

### Limites

Uma execução aceita no máximo 65.536 endereços, 64 serviços e 524.288 sondagens (hosts multiplicados por serviços); requisições maiores encerram com código 2 antes que qualquer coisa seja enviada. `--concurrency` é limitado a 4096 sockets. Cada sondagem tem um prazo rígido de quatro vezes o seu próprio orçamento. Sondagens de conexão (`tcp`, `ssh`, `mysql`, `http`) usam 0.3 segundos, a menos que o serviço defina `timeout`. SNMP e HTTPS usam `--timeout` (padrão 1.0) quando não definem um. Uma sondagem que atinge o prazo limite é relatada como `unknown` com "probe timed out" em `errors`. Falhas locais de socket (por exemplo, ficar sem descritores de arquivo) também são `unknown` com o erro registrado; elas nunca contam como porta filtrada ou host inativo. Antes de sondar, o hostcensus eleva o limite flexível de arquivos abertos em direção ao limite rígido para comportar `--concurrency` mais 64 descritores; quando não consegue, a verificação de preflight `open files` falha e `scan` sai com código 1 antes de enviar tráfego. A descoberta com Nmap usa um timeout de host de 30 segundos. Um prefixo é passado ao nmap em forma CIDR, e uma varredura falha com código de saída 1 quando o nmap relata menos endereços do que recebeu (por exemplo, um nome que não consegue resolver) em vez de marcar hosts como inativos. Um alvo de hostname é resolvido uma vez e o nmap recebe esse endereço, de modo que a descoberta e as sondagens alcancem a mesma máquina. Um prefixo completo é um processo nmap cujo prazo limite do subprocesso é de 35 segundos para cada 256 endereços, arredondado para cima. Varreduras com exclusões usam lotes de 256 hosts e um prazo de 35 segundos para cada lote. A criação de workers é limitada independentemente do tamanho da faixa. DNS reverso e resolução de hostname têm um prazo separado de dois segundos; uma chamada de resolvedor que nunca retorna é abandonada em sua própria thread, de modo que não possa manter o hostcensus em execução além desses limites. No máximo 16 consultas são executadas simultaneamente, e uma chamada abandonada mantém seu slot até retornar, mantendo limitado o número de threads presas; se todas as 16 travarem, consultas posteriores aguardam na fila por um slot fora do prazo de dois segundos (que começa quando um slot é liberado) até que `--deadline` interrompa a varredura. `NetworkScanner` usado como biblioteca sem um `deadline` pode aguardar por esse slot indefinidamente. `--deadline` (padrão de uma hora) limita toda a execução além desses limites.

### Configurando serviços

Os serviços podem ser alterados com um arquivo TOML:

```toml
[services.ssh]          # same name as a built-in: replaces it
port = 2222
timeout = 0.5

[services.admin-ui]     # a new service, probed like HTTPS
port = 8443
probe = "https"
```

`probe` é um entre `tcp`, `ssh`, `mysql`, `http`, `https` ou `snmp` e assume por padrão o nome do serviço quando esse for uma sondagem, caso contrário `tcp`. Apenas `snmp` usa UDP. Nomes de serviço são letras minúsculas, dígitos, `-` e `_`. Dois serviços não podem compartilhar uma porta e protocolo; o histórico registra um único estado para esse par. `timeout` é opcional, em segundos, e de pelo menos 0.05. Sondagens do estilo de conexão (`tcp`, `ssh`, `mysql`, `http`) usam 0.3 segundos por padrão. `snmp` e `https` usam o `--timeout` da varredura quando o serviço não define `timeout`. `--timeout` não substitui um orçamento que o serviço já possui.

Relatórios JSON são documentos versionados (`"format": "hostcensus-report"`, `"version": 1`) que registram o alvo, os serviços sondados e as configurações ao lado de `devices`; `--format json` sem `-o` grava o relatório no stdout em vez da tabela. Toda saída JSON possui um esquema publicado; consulte [Saída JSON](../../../docs/json-output.md). Os dispositivos mantêm os campos originais `ip`, `alive`, `ssh`, `snmp`, `mysql`, `hostname` e `errors` e adicionam uma lista `services` com `name`, `port`, `protocol`, `state` (`open`, `closed`, `filtered` ou `unknown` quando a sondagem falhou localmente ou atingiu seu prazo), `version` e `details` de cada sondagem. A saída CSV ganha as colunas finais `services` e `versions` para os serviços abertos. Os booleanos `ssh`, `snmp` e `mysql` seguem os serviços com exatamente esses nomes.


## Perfis de inventário, preflight e histórico local

Perfis nomeados compartilham um arquivo TOML com as definições `[services]` existentes. Copie
[hostcensus.example.toml](../../../hostcensus.example.toml) para `hostcensus.toml` e defina as redes
que você administra:

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

`preflight` resolve opções e perfis exatamente como `scan` faz, incluindo
`--concurrency` para a verificação de arquivos abertos, portanto um preflight aprovado significa que `scan`
iniciará com o mesmo plano.

Perfis aceitam `network`, `exclusions`, `services`, `ports`, `backend`, `timeout`,
`concurrency` e `max_hosts`. `services` e `ports` usam a sintaxe existente de lista separada por vírgulas. Opções explícitas na CLI substituem as configurações do perfil; opções `--exclude` repetidas
se somam às exclusões do perfil. Uma rede explícita com `--profile` deve estar
contida no escopo IP/CIDR desse perfil. Hostnames continuam suportados para varreduras
diretas, mas não podem ser combinados com exclusões de IP. Limites de hosts se aplicam antes
das exclusões; o limite total de sondagens ainda se aplica depois. Hosts excluídos são
omitidos tanto das verificações de serviço quanto da descoberta opcional com Nmap.

Toda varredura executa verificações locais de preflight antes do tráfego de destino: limites
de alvos/sondagens, acesso ao destino, disponibilidade opcional do executável/wrapper do Nmap, esquema
do histórico e um pacote de CA TLS configurado. `preflight` gera saída JSON e não faz varredura
nos alvos nem cria um banco de dados de histórico. Ele grava temporariamente um arquivo irmão para testar
o acesso ao destino sem alterar o conteúdo existente. O backend asyncio padrão
ainda não requer Nmap nem root. Os caminhos de destino devem ser distintos entre si
e da configuração de entrada, incluindo hard links; symlinks de destino são
rejeitados. Verificações que falham retornam 1; escopo/configuração inválidos retornam 2.

Gravações de relatório e exportação exigem suporte a `O_NOFOLLOW`. Em plataformas sem esse suporte,
incluindo Windows, essas gravações falham sem abrir ou truncar o destino.
Novos relatórios e scripts de exportação são exclusivos do proprietário (modo 0600); substituir um arquivo existente preserva suas
permissões. Gravar em um named pipe sem leitor falha imediatamente em vez de aguardar. Um novo banco de dados `--history` também é criado exclusivo do proprietário; um existente mantém seu modo. Mensagens de log sempre vão para o stderr, portanto o stdout carrega apenas os resultados. Exportações contendo credenciais sempre forçam o modo 0600.

O histórico é opcional e complementa os snapshots JSON existentes e o comando `diff`:

```bash
mkdir -p output
hostcensus scan --profile office --history output/inventory.sqlite3
# Repeat later with the same targets and service selection.
hostcensus scan --profile office --history output/inventory.sqlite3
hostcensus history --history output/inventory.sqlite3 --limit 20
hostcensus compare 1 2 --history output/inventory.sqlite3
hostcensus compare 1 2 --history output/inventory.sqlite3 -o output/changes.json
```

Use IDs de `history`; o exemplo pressupõe um banco de dados novo. Snapshots são armazenados
de forma transacional com horários de início/fim em UTC, versão do pacote, configurações efetivas
não secretas, resumos e todas as observações de hosts/serviços, incluindo erros por host.
Observações incompletas de hosts são retidas. Execuções canceladas não são salvas. Contratos existentes de
relatório, snapshot, exportação e códigos de saída da varredura são preservados.

`history` lista resumos JSON sem ler todos os payloads históricos de dispositivos.
`compare` lê duas varreduras salvas, exige identidades de alvo e portas selecionadas idênticas
e relata alterações de responsividade, status e estado de portas. O ID da varredura anterior
deve preceder o ID posterior. Quando ambas as varreduras registraram `timeout` ou `backend`
e esses valores diferem, o relatório lista um aviso e ainda compara as
observações. Uma espera diferente pode fazer uma porta filtrada parecer aberta. Erros do scanner
e observações de portas desconhecidas são sinalizados como incertos em vez de tratados como
desaparecimento ou fechamento confirmado: hosts com erros aparecem em `uncertain_hosts`, e
toda transição de porta envolvendo `unknown` (incluindo unknown em ambas as varreduras) é listada
em `unconfirmed_ports` em vez de `port_changes`, exceto uma porta que esteja aberta na
varredura posterior, o que é uma alteração de porta. `compare` e `diff` classificam portas com a mesma regra.
`no_longer_responding` significa falta de resposta, não prova de remoção do dispositivo.
O código de saída 0 da varredura não garante que todo host respondeu: inspecione erros por host. O sucesso da comparação retorna 0 existam ou não alterações; o comando de arquivo `diff` existente
mantém seu contrato de código de saída 3. Histórico não suportado ou corrompido retorna 1.

O histórico armazena informações de inventário, portanto escolha um diretório local
adequadamente protegido. Arquivos de perfil e configurações armazenadas não contêm credenciais SNMP;
o tratamento de credenciais continua por meio das opções/ambiente de execução existentes.

## Diff de inventário

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot monday.json
hostcensus scan 10.0.0.0/24 -q --save-snapshot tuesday.json
hostcensus diff monday.json tuesday.json             # table
hostcensus diff monday.json tuesday.json -f json     # JSON on stdout
```

Um snapshot é um JSON com `format: "hostcensus-snapshot"`, `version: 1`, a versão do hostcensus, o horário de criação em UTC, o alvo, o `timeout` e `backend` da varredura quando a varredura os registrou, os serviços que foram sondados e os hosts ativos no mesmo formato do relatório `-o`. Hosts inativos são omitidos. `diff` também aceita relatórios JSON simples de `scan -o`, inclusive aqueles de antes de o campo `services` existir.

`diff` relata hosts novos e desaparecidos, portas que abriram ou fecharam em hosts presentes em ambos e serviços cuja `version` mudou. Portas que foram sondadas em apenas uma das duas varreduras não são comparadas, e um aviso informa isso. Observações com falha nunca são lidas como "sem alteração": uma porta que está `unknown` em qualquer uma das varreduras e não está aberta na posterior é listada em `unconfirmed`, não em `closed`, com `before` sendo `open`, `unknown` ou `not-open` (sondada e fechada ou filtrada) e `after` sendo `unknown` ou `not-open`; uma porta que está aberta agora é relatada em `opened` mesmo que a sondagem anterior tenha falhado. Um host cujas sondagens falharam todas sem resposta em qualquer uma das varreduras é listado em `unsettled_hosts` (com `before`/`after` sendo `up`, `uncertain` ou `absent`, inclusive quando falhou em ambas as varreduras ou está ausente no outro arquivo) em vez de `vanished_hosts`; se responder na varredura posterior, também é relatado como um novo host com suas portas abertas. Snapshots mantêm esses hosts com falha por esse motivo. Um aviso também aparece quando os alvos diferem e quando ambos os arquivos registraram um timeout ou backend e esses valores diferem. `-o PATH` grava também o formato JSON em um arquivo.

Um relatório de uma varredura interrompida por `--deadline` (`"complete": false`) lista apenas os hosts que alcançou, portanto `diff` e `export` o recusam com código de saída 2. `--allow-partial` o aceita com um aviso no stderr: `diff` então lista hosts que a varredura incompleta não listou em `unsettled_hosts` como `unscanned` em vez de desaparecidos (um host que ela listou como inativo continua desaparecido), define `partial` como true e nunca relata ausência de alterações, e `export` grava um aviso no cabeçalho do script.

Códigos de saída de `diff`: `0` sem alterações, `3` alterações encontradas, observações que não puderam ser confirmadas ou uma entrada incompleta (`changed` é true sempre que qualquer lista, incluindo `unsettled_hosts` e `unconfirmed`, não está vazia, ou `partial` é true), `2` um arquivo está ausente, ilegível, não é um snapshot suportado ou está incompleto sem `--allow-partial`, `1` o arquivo `-o` não pôde ser gravado.

## Exportação para o Kadupul

O [Kadupul](https://github.com/kadupulhq/kadupul) (um fork do Cacti 1.2.31) não possui importação em lote de arquivos de dispositivos. Sua forma suportada de adicionar dispositivos a partir de um script é `cli/add_device.php`, um dispositivo por chamada, com argumentos `--option=value`. `hostcensus export` grava um script POSIX `sh` com essas chamadas:

```bash
hostcensus scan 10.0.0.0/24 -q --save-snapshot inventory.json
hostcensus export inventory.json -o kadupul-import.sh --template 1
# or in one step, with template 0: hostcensus scan 10.0.0.0/24 -q -o kadupul-import.sh

# on the Kadupul server, as the user that owns the install:
export HOSTCENSUS_SNMP_COMMUNITY=...        # only if the script asks for it
KADUPUL_ROOT=/var/www/html/kadupul sh kadupul-import.sh
```

Cada host ativo torna-se `php "$KADUPUL_ROOT/cli/add_device.php" --description=... --ip=... --template=N ...`:

- Hosts em que a consulta SNMP da varredura foi bem-sucedida recebem `--version=2 --community=...` ou `--version=3 --username=... --authproto=... --password=...` (além de `--privproto`/`--privpass` para authPriv), `--port` e `--avail=snmp`. A exportação SNMPv3 precisa de `--snmp-user`, e noAuthNoPriv é recusado porque `add_device.php` exige uma senha v3.
- Outros hosts recebem `--version=0 --avail=ping`, com `--ping_method=tcp --ping_port=` sendo a primeira porta TCP aberta, ou ICMP se não houver nenhuma.
- `--notes` lista os serviços abertos e suas versões. `--description` é o nome de DNS reverso quando for simples (letras, dígitos, `.`, `_`, `-`), caso contrário o IP, e é tornado único, pois `add_device.php` trata uma descrição existente como uma atualização desse dispositivo.

Cada valor é validado e protegido para shell com `shlex.quote`. Por padrão nenhum segredo SNMP é gravado: o script expande `HOSTCENSUS_SNMP_COMMUNITY`, `HOSTCENSUS_SNMP_AUTH_KEY` ou `HOSTCENSUS_SNMP_PRIV_KEY` em tempo de execução e para se alguma não estiver definida. `--include-credentials` grava os valores dessas variáveis de ambiente no script em vez disso, cria o arquivo com modo 0600 e registra um aviso. O próprio `add_device.php` imprime a community e recebe segredos como argumentos, que ficam visíveis na lista de processos do servidor Kadupul enquanto cada chamada é executada.

`add_device.php` sai com código 1 para duplicatas e erros; o script continua, contabiliza falhas e sai com código 1 se algum dispositivo não foi adicionado. Os IDs de template vêm de `php cli/add_device.php --list-host-templates`. Códigos de saída de `export`: `0` gravado, `2` entrada ilegível, varredura incompleta sem `--allow-partial` ou dados que não podem ser exportados com segurança, `1` o script não pôde ser gravado.

## Versionamento e processo de lançamento

O hostcensus segue o [Semantic Versioning](https://semver.org/spec/v2.0.0.html): correções
compatíveis incrementam a versão patch, recursos/descontinuações compatíveis incrementam a
versão minor e alterações que quebram a compatibilidade incrementam a versão major.
Comandos e opções, códigos de saída e os esquemas JSON formam o contrato público;
o comportamento descontinuado continua funcionando até a próxima versão principal, a menos que uma
correção de segurança exija alterá-lo antes (o changelog então explica o motivo).

O release-please abre um PR de lançamento a partir dos títulos de Conventional Commit na `main`,
atualizando `pyproject.toml`, `uv.lock` e `CHANGES.md`. O merge cria a
tag `vMAJOR.MINOR.PATCH` e um rascunho de release no GitHub, ao qual a CI anexa um
wheel testado, a distribuição de código-fonte e checksums; o GitHub armazena atestações de build para
esses arquivos por meio da API de atestações. Um mantenedor revisa e publica o
rascunho assim que os arquivos são anexados. Releases nunca são substituídas.

A publicação confiável no PyPI é opcional e requer propriedade do projeto, um publicador
confiável e o ambiente `pypi`. Ela publica os mesmos artefatos de lançamento verificados
sem reconstruir nem armazenar um token de API. Releases com tag neste repositório
público geram atestações de artefatos do GitHub; forks privados exigem um plano
suportado e adesão explícita. Consulte o
[guia completo de lançamento](../../../docs/releasing.md) para configuração, comandos exatos e novas tentativas.

## Desenvolvimento

```bash
uv sync --locked                 # runtime plus the default `dev` group
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=hostcensus
uv build --no-build-isolation
uv run twine check --strict dist/*.whl dist/*.tar.gz
```

As ferramentas de desenvolvimento ficam nos grupos de dependência [PEP 735](https://peps.python.org/pep-0735/)
em `pyproject.toml` (`dev`, `fuzz`, `build`), portanto nunca aparecem nos
metadados do pacote publicado. `uv.lock` é o único arquivo de lock; a CI instala com
`uv sync --locked` e falha quando o lockfile está desatualizado. Selecione o interpretador com
`uv python`, mise (`mise exec python@3.14 -- uv sync --locked`) ou qualquer Python 3.12+.

A CI impõe um piso de cobertura de pacote de 90%. Os testes unitários incluem servidores de loopback
controlados e casos offline de perfil/histórico/validador de lançamento; o laboratório Compose executa
OpenSSH, MariaDB, nginx e net-snmp em uma bridge isolada. Execute-o com
`make test-integration`. Consulte [CONTRIBUTING.md](../../../CONTRIBUTING.md) e
[ferramentas de lançamento](../../../scripts/README.md).

O contêiner de runtime é executado como UID/GID 10001 sem diretório home, sem login de
shell e sem pip, e pode gravar em `/app/output`. Dê a esse usuário acesso de gravação a
qualquer diretório de saída montado. Ele não precisa de capabilities e funciona com um
sistema de arquivos raiz somente leitura, portanto pode ser executado como:

```sh
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp -v "$PWD/out:/app/output" IMAGE scan 192.0.2.0/28 -o /app/output/report.json
```

O Nmap usa seu comportamento de descoberta TCP sem privilégios neste contêiner. A CI reprova
a construção da imagem se houver qualquer vulnerabilidade HIGH ou CRITICAL corrigível relatada pelo Trivy.

## Verificações da cadeia de suprimentos

O [OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/python-network-discovery-tool)
é executado na main e semanalmente, publica sua pontuação real e envia descobertas para o GitHub
code scanning. Actions e bases de contêiner são fixadas por hashes imutáveis; dependências
Python são resolvidas em `uv.lock`. Falhas do Bandit reprovam a CI, e o fuzzing limitado com Atheris
exercita os analisadores SSH, MySQL, HTTP, de certificados e SNMPv3 BER
sem acesso à rede.

O Scorecard também mede atividade histórica de revisão, diversidade de contribuidores e
proveniência de lançamentos. Essas pontuações refletem evidências reais; não são afirmações
de que toda verificação de governança ou de lançamento histórico seja atendida. Consulte
[SECURITY.md](../../../SECURITY.md) e [proveniência de lançamentos](../../../docs/releasing.md).

## Localização

Mensagens da CLI e tabelas de resumo/diff no terminal suportam 45 idiomas (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) sem dependências adicionais de runtime. A resolução respeita `--lang`, depois `LC_ALL`, `LC_MESSAGES` e `LANG`, usando `en` como fallback. Esquemas JSON, colunas CSV e scripts de exportação permanecem inalterados em todos os idiomas.

```bash
hostcensus --lang de version
LANG=ja_JP.UTF-8 hostcensus scan 192.0.2.0/28
```

## Contribuição

As contribuições devem incluir um caso reproduzível, preservar os contratos documentados da CLI e
de formato de dados e passar pelas verificações de qualidade acima. Consulte
[CONTRIBUTING.md](../../../CONTRIBUTING.md) para o fluxo de desenvolvimento e
[o guia de lançamento](../../../docs/releasing.md) para decisões de compatibilidade e versionamento.

## Status de segurança e licença

Consulte [SECURITY.md](../../../SECURITY.md) para divulgação privada e versões suportadas.
O hostcensus é licenciado sob a [Licença MIT](../../../LICENSE).

Os cabeçalhos de código-fonte usam identificadores SPDX e preservam os créditos de contribuidores do histórico do Git.
Consulte [AUTHORS.md](../../../AUTHORS.md) para atribuição. Capturas binárias de teste e o
lockfile gerado usam arquivos `.license` adjacentes; o texto da MIT está em `LICENSES/MIT.txt`.
