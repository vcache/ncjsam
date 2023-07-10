# NCJSAM: Never Code JS AnyMore

NCJSAM is a prototype of a game description language. The language is a YAML with occasional inlines of JS. The scene, GUI, and application layout are described with YAML, while JS is used to code logic and behavior. The whole game is supposed to be defined in a declarative way. 

Please note that this project is more like a sketch than anything close to a production-ready product, which means the following:
  - It is dirty and buggy, especially in corner cases;
  - Not maintained in general;
  - Lack of features (a lot of non-implemented stuff);
  - Massive lack of documentation and comments.

# Motivation

Sometimes you just want to make a little game or prototype of it. NCJSAM tests the following hypothesis: in order to reduce the time-to-market of a game, development iterations should be short and many in number.

# Installation

First of all, dependencies should be installed:

```bash
$ pip3 install -r ./requirements.txt
```

# Usage

Then an example project may be built:

```bash
$ ./ncjsam.py build ./examples/hello-world
```
An output will reside at the `./examples/hello-world/dist` and could be accessed through a local HTTP server, for example:
```bash
$ python3 -m http.server --directory ./examples/hello-world/dist/
```
Then a game may be opened in the browser via the address `http://127.0.0.1:8000/` (or similar, check the output of the `http.server` tool).

As an alternative, a daemon mode could be used:
```bash
$ ./ncjsam.py daemon ./examples/hello-world
```
In this case, NCJSAM runs a daemon that provides a local HTTP server and a project's files tracker. The tracker automagically rebuilds the project every time any of the files changes. The contents of the page update in the same way and, at the same time, save and then restores the game's state.

This mode allows you to see the changes in the game as fast as possible, that is, at every save of the file's contents. It works in the same way as the `grip -b ...` command does.

In addition, there are various options that can be found using the `--help` command:
```bash
$ ./ncjsam.py --help
```

# License

MIT. See LICENSE file.

# Contributing

Any feedback (both positive and negative) and pull requests are appreciated.
