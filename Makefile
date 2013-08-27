TMP=/tmp/quicklojure

all: build_osx_pkg

build_osx_pkg:
	mkdir -p $(TMP)/usr/bin $(TMP)/usr/lib/quicklojure/ext
	cp -R src/clj.sh $(TMP)/usr/bin/clj
	cp -R lib/* $(TMP)/usr/lib/quicklojure/ext/
	pkgbuild --identifier quicklojure.pkg.app --root $(TMP) quicklojure.pkg
	rm -rf $(TMP)

.PHONE: clean
clean:
	rm quicklojure.pkg
