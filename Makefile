.PHONY: test clean

test:
	@echo test: Generating tests from control set
	@$(PWD)/tests/devicedetect/resources/controlset-to-vtc.py $(PWD)/tests/devicedetect/resources/controlset.csv > $(PWD)/tests/devicedetect/100-from-controlset.vtc
	@/usr/bin/varnishtest -Dvarnishd=/usr/sbin/varnishd -Dprojectdir=$(PWD) tests/**/*.vtc

clean:
	@rm $(PWD)/tests/devicedetect/100-from-controlset.vtc
