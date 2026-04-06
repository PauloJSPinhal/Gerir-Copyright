# Gerir Copyright

Ferramenta GTK3/Python para gerir autoria e copyright de fotografias em lote. Valida anos, confirma alterações e grava metadados com exiftool.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%28Debian%29-ff69b4.svg)

## 📸 Visão Geral

Esta aplicação permite adicionar metadados de direitos autorais em imagens usando o formato padrão: **`(c) <Autor> (<Ano>)`**. Ela se integra ao gerenciador de arquivos Nautilus através do script `gerir_copyright.py`, facilitando a aplicação de autorias em lote.

## ✨ Funcionalidades

- ✅ Atualizar múltiplos metadados simultaneamente (Artist, Creator, By-line, Copyright)
- ✅ Detecção automática de autor e ano existentes
- ✅ Validação para garantir que todas as imagens sejam do mesmo ano
- ✅ Confirmação antes de alterar autor existente
- ✅ Verificação de metadados já atualizados (pula arquivos sem alterações)
- ✅ Formato de copyright: "(c) <Autor> (<Ano>). Todos os direitos reservados."
- ✅ Interface GTK com melhor gerenciamento de janelas
- ✅ Mensagens de sucesso e erro com detalhes

## 🖥️ Requisitos do Sistema

- **Sistema Operacional**: Debian 13 (Trixie)
- **Python**: 3.7+
- **Bibliotecas**:
  - `python3-gi` (GTK 3 bindings)
  - `exiftool` (metadados)
  - `notify-send` (notificações desktop - opcional)

### Instalação de Dependências

```bash
sudo apt update
sudo apt install python3-gi exiftool libnotify-bin
```

## 📦 Formatos Suportados

- JPEG / JPG
- TIFF / TIF
- HEIC / HEIF
- DNG
- RAW: CR2, CR3

> **Nota**: O script atualiza os metadados diretamente no arquivo, sem necessidade de arquivos `.xmp` laterais.

## 🚀 Como Usar

### Integração com Nautilus

1. Copie o script para a pasta de extensões do Nautilus:
   ```bash
   cp gerir_copyright.py ~/.local/share/nautilus-python/extensions/
   ```

2. Reinicie o Nautilus:
   ```bash
   nautilus -q
   ```

3. Clique com botão direito em imagens e selecione a opção de autoria.

### Uso via Linha de Comando

```bash
# Um ou mais arquivos
python3 gerir_copyright.py foto1.jpg foto2.jpg

# Pasta inteira
python3 gerir_copyright.py /caminho/para/pasta

# Mista
python3 gerir_copyright.py foto1.jpg pasta/ foto2.jpeg
```

> **Nota**: O script atualiza automaticamente os campos Artist, Creator, By-line e Copyright com o formato: "(c) <Autor> (<Ano>). Todos os direitos reservados."

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
gerir_copyright.py
└── Gerencia autorias em imagens
    ├── collect_images()       # Coleta arquivos de imagem
    ├── get_metadata_fast()    # Lê metadados exiftool (Artist, Creator, By-line, Copyright)
    ├── show_main_dialog()     # Interface GTK para edição
    ├── apply_authorship()     # Atualiza metadados (Artist, Creator, By-line, Copyright)
    └── quit_app()             # Termina o loop GTK
```

### Contribuindo

Contribuições são bem-vindas! Sinta-se livre para:
- Abrir issues para bugs ou sugestões
- Enviar pull requests com melhorias

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

**Nota**: Este script foi desenvolvido especificamente para Debian 13 com ambiente GNOME/Nautilus. Pode requerer adaptações para outras distribuições ou ambientes de desktop.
