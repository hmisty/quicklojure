#!/bin/sh
# run clojure source or start repl
# with .classpath if exists

# quicklojure -- focusing on speedy start of clojure
# Evan Liu (hmisty)
# 2013.08.18

# reference: http://en.wikibooks.org/wiki/Clojure_Programming/Getting_Started

NREPL_PORT=7999

RLWRAP=rlwrap
BREAKCHARS="(){}[],^%$#@\"\";:''|\\"
COMPLETIONS=$HOME/.clj_completions

JAVA=/usr/bin/java
JPARAM="-d32 -client -Xverify:none"

CLJ_LIB=/usr/lib/quicklojure/ext
CLASSPATH=`pwd`:$CLJ_LIB/*

if [ -f .classpath ]; then
	CLASSPATH=$CLASSPATH:`cat .classpath`
fi

if [ $# -eq 0 ]; then
	exec $RLWRAP -r -c -b "$BREAKCHARS" -f $COMPLETIONS $JAVA $JPARAM -classpath "$CLASSPATH" clojure.main -r
elif [ "$1" == "--nrepl" ]; then
	if [ "$2" != "" ]; then NREPL_PORT=$2; fi
	exec $RLWRAP -r -c -b "$BREAKCHARS" -f $COMPLETIONS $JAVA $JPARAM -classpath "$CLASSPATH" clojure.main -e "(use '[clojure.tools.nrepl.server :only (start-server stop-server)])(defonce server (start-server :port $NREPL_PORT))" -r
elif [ "$1" == "--nrepl-headless" ]; then
	if [ "$2" != "" ]; then NREPL_PORT=$2; fi
	exec $JAVA $JPARAM -classpath "$CLASSPATH" clojure.main -e "(use '[clojure.tools.nrepl.server :only (start-server stop-server)])(defonce server (start-server :port $NREPL_PORT))"
else #execute a clj file $1
	exec $JAVA $JPARAM -classpath "$CLASSPATH" clojure.main "$1" -- "$@"
fi
