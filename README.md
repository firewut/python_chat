About
=====
Angular2 and Python aiohttp built chat. Uses postgres as database.


Backend
=======

```bash
docker pull postgres
docker run -p 0.0.0.0:32769:5432 -d --name=postgres postgres

virtualenv env
source env/bin/activate
pip install -e requirements.txt
cd messenger && python .
```


Frontend
========

```bash
cd web2 && npm install && npm start
```