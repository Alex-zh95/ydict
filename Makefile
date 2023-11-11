PREFIX ?= /usr/local

install: ydict.py ydict_lib
	cp -r ydict_lib $(PREFIX)/bin/ydict_lib
	install -Dm755 ydict.py $(PREFIX)/bin/ydict

clean:
	rm $(PREFIX)/bin/ydict
	rm -rf $(PREFIX)/bin/ydict_lib
