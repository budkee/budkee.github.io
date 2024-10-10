---
layout: post
title:  "Git Flow"
date:   2024-04-12 
categories: jekyll update
---

## Teoria

### Branches

`main`: registro histórico do projeto. Somente será alterado (merge) em casos de lançamentos (releases) ou manutenções de documentação e segurança (hotfixs).

`develop`: seu branch de trabalho principal. Aqui você realiza o merge dos novos recursos (features) que você desenvolveu.

`feature`: branch dedicado ao desenvolvimento do novo recurso do código. Este deverá ser criado a partir da ramificação mais recente de desenvolvimento.

`release`: esta branch contém todos os recursos desenvolvidos durante um período de lançamento a partir da branch de desenvolvimento (develop). **Esta branch dá início ao próximo ciclo de lançamento, não podendo, portanto, adicionar novos recursos após este ponto.**

`hotfix`: branch para manutenção de documentação e/ou segurança do código.

## Prática

Verifique em qual branch você está:

    git branch

### Git Flow | Iniciando o workflow

Iniciar a `main` com o git flow

    git flow init

Alternar para o `develop`

    git checkout develop

### Git Flow | Novo recurso

Iniciar um novo recurso `feature` a partir da branch `develop`

    git flow feature start feature_branch

    # Output
    Switched to a new branch 'feature/feature_branch'
    Summary of actions:
    - A new branch 'feature/feature_branch' was created, based on 'develop'
    - You are now on branch 'feature/feature_branch'

    Now, start committing on your feature. When done, use:

    git flow feature finish feature_branch

    # FimOutput

Merge da `feature` à `develop` e retorno para a mesma (branch)

    git flow feature finish feature_branch

    # Output
    Switched to branch 'develop'
    Already up to date.
    Deleted branch feature/feature_branch (was af4029b).

    Summary of actions:
    - The feature branch 'feature/feature_branch' was merged into 'develop'
    - Feature branch 'feature/feature_branch' has been removed
    - You are now on branch 'develop'

    # FimOutput

Iniciar um novo lançamento `release` a partir da branch `develop`

    git flow release start 0.1.0

    # Output
    Switched to a new branch 'release/0.1.0'

    Summary of actions:
    - A new branch 'release/0.1.0' was created, based on 'develop'
    - You are now on branch 'release/0.1.0'

    Follow-up actions:
    - Bump the version number now!
    - Start committing last-minute fixes in preparing your release
    - When done, run:

    git flow release finish '0.1.0'

    # FimOutput

Merge da `release` à `main` e `develop`, e retorno para `main`

    git flow release finish '0.1.0'

    # Output
    Switched to branch 'main'
    Your branch is ahead of 'origin/main' by 1 commit.
    (use "git push" to publish your local commits)
    Deleted branch release/0.1.0 (was af4029b).

    Summary of actions:
    - Latest objects have been fetched from 'origin'
    - Release branch has been merged into 'main'
    - The release was tagged '0.1.0'
    - Release branch has been back-merged into 'develop'
    - Release branch 'release/0.1.0' has been deleted

Iniciar a manutenção do código `hotfix`

    git flow hotfix start hotfix_branch

    # Output
    Switched to a new branch 'hotfix/hotfix_branch'

    Summary of actions:
    - A new branch 'hotfix/hotfix_branch' was created, based on 'main'
    - You are now on branch 'hotfix/hotfix_branch'

    Follow-up actions:
    - Bump the version number now!
    - Start committing your hot fixes
    - When done, run:

    git flow hotfix finish 'hotfix_branch'

    # FimOutput

Merge da `hotfix` à `main` e retorno para `main`

    git flow hotfix finish 'hotfix_branch'

    # Output
    Switched to branch 'main'
    Your branch is up to date with 'origin/main'.
    Merge made by the 'ort' strategy.
    ## Alterações
    Switched to branch 'develop'
    Merge made by the 'ort' strategy.
    ## Alterações
    Deleted branch hotfix/hotfix_branch (was 61a9ba5).

    Summary of actions:
    - Latest objects have been fetched from 'origin'
    - Hotfix branch has been merged into 'main'
    - The hotfix was tagged 'hotfix_branch'
    - Hotfix branch has been back-merged into 'develop'
    - Hotfix branch 'hotfix/hotfix_branch' has been deleted

## Links e Referências

- [Git Flow: modelo de desenvolvimento colaborativo](https://www.atlassian.com/br/git/tutorials/comparing-workflows/gitflow-workflow)
- [Nunca usei o Git: por onde começo?]()
- [Já usei o Git: como estabeleço uma rotina de desenvolvimento?]()
- [Configuração CI/CD: por onde começo?]()
