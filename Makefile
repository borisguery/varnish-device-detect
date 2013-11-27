.PHONY: test clean

test: clean
	@echo "[test]\t- Generating tests from control set"
	@$(PWD)/tests/devicedetect/resources/controlset-to-vtc.py -s 70 $(PWD)/tests/devicedetect/resources/controlset.csv $(PWD)/tests/devicedetect/
	@/usr/bin/varnishtest -Dvarnishd=/usr/sbin/varnishd -Dprojectdir=$(PWD) tests/**/*.vtc

clean:
	@echo "[clean]\t- Cleaning generated tests"
	@rm -f $(PWD)/tests/devicedetect/9*from-controlset.vtc
