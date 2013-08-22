# Quicklojure

Quicklojure aims to be the quickest, most intuitive and painless clojure distribution with lots of good ones pre-packaged for anyone to start with.

Three great virtues of a programmer: laziness, impatience, and hubris. -- Larry Wal

## Quickstart
* MacOSX
  * Download quicklojure.pkg. Double click to install it. Done!
  * Open Terminal. Type clj. Happy REPLing!

## To Be
* the quickest-to-start clojure distribution
* (TODO) sweet nrepl server-client helper
  * server-side: clj --nrepl PORT (default 7888)
  * client-side: clj --connect PORT (default 7888) or nrepl-connect HOST PORT and you are then in the remote REPL
* (TODO) nrepl plugins for vim, emacs, etc
  * temp work-around:
  * clj, and start nrepl server: (use '[clojure.tools.nrepl.server :only (start-server stop-server)]) (defonce server (start-server :port 7888))
  * vim: use fireplace vim plugin, :Connect nrepl://localhost:7888
* (TODO) auto-dependency
  * clj --deps will update .clojure with correctly generated classpath including maven packages if project.clj found in the current directory


## Not To Be
* a full-fledged package manager
  * use leiningen please


## OS Support
* MacOSX
  * pre-requisite: rlwrap, java
  * (TODO) pkg installer
* Linux
  * pre-requisite: rlwrap, java
* (TODO) Windows


## Under The Hood

Here is the comprehensive list of what are included in the "lots of good ones":

* clj
* sublime text 2 plugin
  * Borrowed from Eleven and refined
* (TODO) vim plugin
* (TODO) emacs plugin


## Known Issues
* jline doesn't work well in macosx. it messes up repl prompt when moving arrow keys.
* use drip to replace java can speed up jvm starting but it will mess up rlwrap.


## License
GPLv3 (c) Evan Liu (hmisty) 2013
