PREFIX ?= /usr/local

install:
	mkdir -p $(PREFIX)/bin/ydict_lib
	cp -r src/ydict/ydict_lib/ylib.py $(PREFIX)/bin/ydict_lib/ylib.py
	install -Dm755 src/ydict/ydict.py $(PREFIX)/bin/ydict.py

clean:
	rm -rf $(PREFIX)/bin/ydict
	rm -rf $(PREFIX)/bin/ydict_lib
