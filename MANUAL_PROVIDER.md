# Manual Provider

O `manual` provider permite usar o ChatGPT Plus sem API e sem custo adicional de tokens da API.

## Configuração

No `.env`:

```env
JARVIS_PROVIDER=manual
JARVIS_ALLOWED_ROOT=E:\projects
JARVIS_MANUAL_OPEN_PROMPT=true
JARVIS_MANUAL_EDITOR=notepad
JARVIS_VOICE_ENABLED=false
```

## Como funciona

Quando o Jarvis precisar de IA, ele irá:

1. gerar um arquivo de prompt em `.jarvis/manual/outbox`;
2. abrir o prompt no editor configurado;
3. esperar você colar a resposta no terminal;
4. salvar a resposta em `.jarvis/manual/inbox`;
5. continuar o fluxo normalmente.

## Finalização da resposta

Ao colar a resposta no terminal, finalize com:

```text
<<<END>>>
```

## Exemplo

```text
/spec refine E:\projects\teste-jarvis registro-inconsistencias-wiki
```

O Jarvis gera o prompt. Você cola no ChatGPT Plus, copia a resposta e cola de volta.

## Implementação de arquivos

Para `/spec implement` ou `/spec diff`, a resposta do ChatGPT precisa conter blocos:

```text
```file path=docs/exemplo.md
conteúdo completo
```
```

Sem esses blocos, o Jarvis irá salvar a proposta, mas não aplicará arquivos.
