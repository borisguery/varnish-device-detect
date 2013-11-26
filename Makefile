.PHONY: test clean

test: clean
	@echo "[test]\t- Generating tests from control set"
	@$(PWD)/tests/devicedetect/resources/controlset-to-vtc.py $(PWD)/tests/devicedetect/resources/controlset.csv > $(PWD)/tests/devicedetect/100-from-controlset.vtc
	@/usr/bin/varnishtest -Dvarnishd=/usr/sbin/varnishd -Dprojectdir=$(PWD) tests/**/*.vtc

clean:
	@echo "[clean]\t- Cleaning generated tests"
	@rm $(PWD)/tests/devicedetect/100-from-controlset.vtc
