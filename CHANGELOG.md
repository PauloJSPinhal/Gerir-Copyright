# Changelog

## [1.0.0] - 2026-04-06

### Adicionado
- Suporte para múltiplos formatos de imagem (JPEG, TIFF, HEIC, HEIF, DNG, CR2, CR3)
- Atualização de metadados múltiplos (Artist, Creator, By-line, Copyright)
- Detecção automática de autor e ano existentes
- Validação para garantir que todas as imagens sejam do mesmo ano
- Confirmação antes de alterar autor existente
- Verificação de metadados já atualizados (pula arquivos sem alterações)
- Formato de copyright: "(c) <Autor> (<Ano>). Todos os direitos reservados."
- Interface GTK com melhor gerenciamento de janelas
- Mensagens de sucesso e erro com detalhes
- Integração com Nautilus via extensão
- Uso via linha de comando

### Melhorias
- Processamento mais rápido com exiftool `-fast2`
- Gerenciamento limpo do loop GTK com função `quit_app()`
- Melhor tratamento de janelas modais e parent-child
- Suporte para leitura de metadados em múltiplos formatos (Artist, Creator, By-line, Copyright)

### Técnicos
- Código reescrito com melhor estrutura e organização
- Tratamento de erros aprimorado
- Uso de `GLib.idle_add()` para todas as chamadas de UI em threads
- Verificação de diretórios aninhados na coleta de imagens
