# Comandos importantes
+ pybabel extract -F babel.cfg -k _l -o messages.pot .  (gera arquivo com mensagens)
+ pybabel init -i messages.pot -d app/translations -l en (cria um arquivo para colocar a tradução em inglês)
+ pybabel compile -d translations (compila os arquivos de com as traduções para gerar um arquivo mo.)
+ pybabel compile -f -d translations (faz o mesmo acima ignorando erros de #, fuzzy)
