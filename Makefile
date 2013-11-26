.PHONY: test

test:
	@/usr/bin/varnishtest -Dvarnishd=/usr/sbin/varnishd -Dprojectdir=$(PWD) tests/**/*.vtc

