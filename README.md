# ucu-ai-checkers

Checkers game AI development tools for the CS301 AI class I teach at UCU.

**1. An AI server providing next moves via HTTP API.**

_Linux, macOS:_

```
$ cd ai-server
$ uwsgi --ini uwsgi.ini --socket 0.0.0.0:5000
```

_Windows (cannot use uWSGI, so can be a bit slower):_

```
$ cd ai-server
$ python app.py 0.0.0.0 5000
```

**2. A game arena that can run a competition between two AI servers, save the games, and replay them. Provides logging and optional GUI visualization via matplotlib.**

```
$ cd game-arena
$ python arena.py compete --gui --num-games 5 http://localhost:5000 http://localhost:5000
```

![ucu-ai-checkers](https://user-images.githubusercontent.com/2750531/32143627-fa839a28-bcb4-11e7-9d75-bf2698b7c193.gif)
