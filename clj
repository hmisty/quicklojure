#!/bin/sh
# run clojure source or start repl
# with .classpath if exists

# quicklojure -- focusing on speedy start of clojure
# Evan Liu (hmisty)
# 2013.08.18

# reference: http://en.wikibooks.org/wiki/Clojure_Programming/Getting_Started

RLWRAP=rlwrap
BREAKCHARS="(){}[],^%$#@\"\";:''|\\"
COMPLETIONS=$HOME/.clj_completions
JAVA=/usr/bin/java
CLJ_LIB=$HOME/Library/Clojure/lib
CLASSPATH=`find $HOME/Library/Clojure/lib | xargs | sed 's/ /:/g'`

if [ -f .classpath ]; then
	CLASSPATH=$CLASSPATH:`cat .classpath`
fi

if [ $# -eq 0 ]; then 
	exec $RLWRAP --remember -c -b "$BREAKCHARS" $JAVA -cp "$CLASSPATH" clojure.main
else
	exec $JAVA -cp "$CLASSPATH" clojure.main "$1" -- "$@"
fi

