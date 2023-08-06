## Rabbit PWX Connection Data Base
Project for PWX connection to PostgreSQL and Redis

### Update Project
Faças as alterações, e mude no arquivo 
`setup.py`, a próxima versão da biblioteca `version='0.0.9'`, por exemplo,
e então comite-as na master. 

Após o merge, realizar os seguintes passos:

No terminal da virtualenv, digite:

``python setup.py sdist bdist_wheel``

Em seguide, digite:

``twine upload dist/*``

Basta digitar o usuário do repositório e senha e a biblioteca estará no ar!

Para finalizar, apague as pastas: build, dist e pwx_db_connection.egg-info

