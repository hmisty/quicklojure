# quicklojure

This is a pre-packaged clojure distribution, mainly for clojure newbies:
* to start clojure quickly and painlessly
* to setup a clojure environment easily
* to launch clojure codes fast
* ...and other sweet stuffs...

## Install
* MacOSX
  * git clone https://github.com/hmisty/quicklojure.git
  * cp -R quicklojure ~/Library/
  * sudo ln -s ~/Library/quicklojure/clj /usr/bin
  * clj 
  * #Happy REPLing!

## To Be
* the quickest-to-start clojure distribution
* (TODO) sweet nrepl server-client helper
  * server-side: nrepl-start PORT
  * client-side: nrepl-connect HOST PORT and you are then in the remote REPL
* (TODO) nrepl plugins for vim, emacs, etc
  * temp work-around:
  * clj, and start nrepl server: (use '[clojure.tools.nrepl.server :only (start-server stop-server)]) (defonce server (start-server :port 7888))
  * vim: use fireplace vim plugin, :Connect nrepl://localhost:7888
* (TODO) auto-dependency
  * clj deps will update .clojure with correctly generated classpath including maven packages if project.clj found in the current directory


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


## Known Issues
* jline doesn't work well in macosx. it messes up repl prompt when moving arrow keys.
* use drip to replace java can speed up jvm starting but it will mess up rlwrap.


## License
GPLv3 (c) Evan Liu (hmisty) 2013
