# Quicklojure

Quicklojure aims to be the quickest, most intuitive and painless clojure distribution with good ones pre-packaged for anyone to start with.

Three great virtues of a programmer: laziness, impatience, and hubris. -- Larry Wal

## Quickstart
* MacOSX
  * Download quicklojure.pkg. Double click to install it. Done!
  * Open Terminal. Type clj. Happy REPLing!

* Linux
TODO

* Windows
TODO

## To Be
* the quickest-to-start clojure distribution
* (TODO) sweet nrepl server-client helper
  * server-side: clj --nrepl PORT (default 7888)
  * client-side: clj --connect PORT (default 7888) or nrepl-connect HOST PORT and you are then in the remote REPL
* (TODO) auto-dependency
  * clj --deps will update .clojure with correctly generated classpath including maven packages if project.clj found in the current directory


## Not To Be
* a full-fledged package manager
  * use leiningen please


## Known Issues
* jline doesn't work well in macosx. it messes up repl prompt when moving arrow keys.
* use drip to replace java can speed up jvm starting but it will mess up rlwrap.


## License
GPLv3 (c) Evan Liu (hmisty) 2013
