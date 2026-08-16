---
layout: post
title: "Guia prático: como criar e publicar novos posts"
date: 2026-08-16
categories: blog
tags: [jekyll, escrita, publicacao]
image: images/pic02.jpg
excerpt: "Um passo a passo simples para criar, revisar e publicar novos posts no portfólio sem quebrar o padrão do site."
---

## Objetivo

Este guia existe para facilitar o processo de criação de novos posts no portfólio, mantendo padronização visual, consistência de conteúdo e publicação segura.

## 1) Crie a base do post

Comece a partir do modelo em [src/_drafts/post-template.md](src/_drafts/post-template.md).

Campos obrigatórios no front matter:

- `layout: post`
- `title: "..."`
- `date: YYYY-MM-DD`

Campos recomendados:

- `categories: blog`
- `tags: [tag1, tag2]`
- `image: images/pic01.jpg`
- `excerpt: "Resumo curto para o card da página de blog"`

## 2) Nomeie o arquivo corretamente

Use o padrão:

`YYYY-MM-DD-slug-do-post.md`

Exemplo:

`2026-08-16-como-criar-novos-posts.md`

## 3) Estruture o conteúdo

Sugestão de estrutura:

- Introdução: contexto e objetivo
- Desenvolvimento: passos, exemplos e decisões
- Conclusão: resumo e próximos passos

Boas práticas:

- Use títulos curtos e claros
- Escreva parágrafos pequenos
- Priorize listas para instruções
- Evite links quebrados

## 4) Revise com checklist rápido

Antes de publicar, confirme:

- O `title` está preenchido no front matter
- A `date` está correta
- O `excerpt` resume o texto em 1 frase
- A `image` existe em [src/images](src/images)
- Não há placeholders (ex.: "escreva aqui")
- Links externos usam HTTPS

## 5) Teste no ambiente local

Com o servidor em hot reload:

- Salve o arquivo
- Abra `http://localhost:4000/blog.html`
- Verifique se o card do post apareceu com título e resumo
- Abra o post e valide leitura, formatação e links

## 6) Publique

Se você começou em `src/_drafts`, mova para `src/_posts` com o nome final.

Depois:

1. Faça commit das alterações.
2. Faça push para o repositório.
3. Valide no ambiente publicado.

## Erros comuns e como evitar

- Post não aparece no blog: faltou `title` no front matter.
- Link do post errado: nome do arquivo fora do padrão de data.
- Card sem resumo útil: `excerpt` vazio ou muito genérico.
- Imagem quebrada: caminho incorreto em `image`.

## Modelo mínimo reutilizável

```md
---
layout: post
title: "Título do post"
date: 2026-08-16
categories: blog
tags: [tag1, tag2]
image: images/pic01.jpg
excerpt: "Resumo curto para o card"
---

## Introdução

## Desenvolvimento

## Conclusão
```

Com esse fluxo, qualquer novo post passa a aparecer automaticamente em [src/blog.html](src/blog.html), mantendo o padrão do site com menos retrabalho.
