# Imagens do README do perfil

Duas coisas moram aqui: as logos dos projetos (esta pasta) e os botoes de contato (, gerados por ).

## Logos dos projetos

Pasta das logos usadas na tabela **Projects** do README do perfil.

## Passo a passo

1. **Exporte a logo** como PNG quadrado, **256x256**. Se a logo tiver fundo proprio (tipo um icone de app), mantenha. Se for so o simbolo, use fundo transparente.
2. **Salve aqui** com nome minusculo e sem espaco: `trimos.png`, `vibebar.png`.
3. **Copie o bloco `<tr>`** no README da raiz e troque os valores:

```html
<tr>
<td nowrap><img src="assets/projects/NOME.png" width="22" align="center">&nbsp;<b><a href="https://link">Nome</a></b></td>
<td>Descricao de uma linha</td>
<td><kbd>React</kbd> <kbd>TypeScript</kbd> <kbd>Postgres</kbd></td>
</tr>
```

## Por que a tabela e HTML e nao markdown

Tabela markdown normal nao deixa controlar quebra de linha. Com uma logo pequena ao lado de um nome curto, o navegador separa os dois e joga a logo pra linha de cima assim que a janela aperta. O `nowrap` no `<td>` resolve, e o GitHub aceita esse atributo (testado contra a API de markdown deles). `style="white-space:nowrap"` e `<nobr>` sao removidos pelo sanitizador, entao nao adianta tentar.

## Detalhes que importam

| Item | Recomendacao | Porque |
|:--|:--|:--|
| Tamanho do arquivo | 256x256 px | Nitido em tela Retina mesmo exibido a 22px |
| Exibicao | `width="22"` | Alinha com a altura da linha de texto |
| Espaco antes do nome | `&nbsp;` colado no `>`, sem espaco normal | Espaco normal e ponto de quebra |
| Cantos | Arredonde no proprio PNG (canal alpha) | O GitHub remove `style`, entao `border-radius` via CSS nao funciona |
| Fundo | Transparente, ou fundo proprio com contraste | O README e lido em light **e** dark mode |
| Chips de stack | `<kbd>`, 4 por projeto | `<kbd>` tem fundo e borda visiveis; `<code>` fica quase invisivel no dark |
| Descricao | Uma linha, ate ~90 caracteres | Mais que isso empurra a tabela e come largura das outras colunas |

## Logo que some em um dos modos

Se a logo so funciona em um dos temas, o GitHub suporta troca automatica:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/projects/x-dark.png">
  <img src="assets/projects/x-light.png" width="22" align="center">
</picture>
```

## Nao tem logo pronta?

- Favicon do proprio projeto (`public/favicon.ico`) costuma ja estar em 256x256. Foi assim que a do TrimOS foi feita.
- Screenshot do app, recorte quadrado do icone.
- Ou peca pro Claude gerar um simbolo simples no estilo da marca (`#0A0A0A` / `#AEFA0E`).
