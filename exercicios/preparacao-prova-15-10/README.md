# Executar a aplicação

Na raiz do projeto, rode:

```bash
uv run preparacao-prova-15-10
```

Os módulos dentro de `src/preparacao_prova_15_10` formam um pacote. Por isso,
imports entre eles usam caminhos relativos, e o servidor deve ser iniciado
pelo ponto de entrada do pacote — não executando `routes/animaisRoute.py`
diretamente.