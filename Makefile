.PHONY: test clean

test: clean
	@echo "[test]\t- Generating tests from control set"
	@$(PWD)/tests/scripts/controlset-to-vtc.py -s 70 $(PWD)/tests/scripts/controlset.csv $(PWD)/tests/
	@/usr/bin/varnishtest -Dvarnishd=/usr/sbin/varnishd -Dprojectdir=$(PWD) tests/*.vtc

clean:
	@echo "[clean]\t- Cleaning generated tests"
	@rm -f $(PWD)/tests/9*from-controlset.vtc
