# ucu-ai-checkers

Checkers game AI development tools for the CS301 AI class I teach at UCU.

1. An AI server providing next moves via HTTP API.

```
$ cd ai-server
$ uwsgi --ini uwsgi.ini --socket 0.0.0.0:5000
```

2. A game arena that can run a competition between two AI servers, save the games, and replay them. Provides logging and optional GUI visualization via matplotlib.

```
$ cd game-arena
$ python arena.py compete --gui --num-games 5 http://localhost:5000 http://localhost:5000
```

![image](https://user-images.githubusercontent.com/2750531/31972594-1b7b8ee0-b92a-11e7-91af-8425c3cffb5b.png)
