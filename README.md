Resize Photos Challenge - Solução para o Algoritmo
================================

.. image:: https://travis-ci.org/felipeanchieta/resize-photos.svg?branch=master
    :target: https://travis-ci.org/felipeanchieta/resize-photos

O Problema
-----------

O desafio proposto é para consumir um determinado serviço de internet on-line, no caso um servidor de imagens JPG, redimensioná-los como 320x240, 384x288, e 640x480 os persistem como documentos MongoDB e depois criar um servidor web que liste estas imagens  usando um JSON de resposta, com seus respectivos tamanhos disponíveis.


Solução Proposta
-----------------

A solução proposta foi construir um servidor web usando o Python Flask, em seguida, usar PIL para redimensionar as imagens e um adaptador MongoDB para persistir os novos arquivos.

Foi desenvolvido um módulo com toda a lógica, onde temos um MongoDB em execução e um aplicativo Flask também em execução.

>>> python core.py


É um requisito que se tenha o Python 3 instalado.

Testes Automatizados
-----------------

Execute o teste automatizado através da linha de comando abaixo:

>>> python -m unittest test_automated_tests

Ele verificará o estado do webservice e o que fizemos até aqui (download, redimensionamento, economia, etc.).
