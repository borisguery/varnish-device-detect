#!/usr/bin/python

# Generate a varnishtest script to validate the preclassified
# U-A strings in the control set.

import errno, sys

HEADER="""varnishtest "automatic test of control set"
server s1 {
       rxreq
       txresp
} -start

varnish v1 -vcl+backend {
        include "${projectdir}/devicedetect.vcl";
        sub vcl_recv {
            call devicedetect;
        }

        sub vcl_deliver {
            set resp.http.X-UA-Device-Type = req.http.X-UA-Device-Type;
            set resp.http.X-UA-Device-OS   = req.http.X-UA-Device-OS;
        }
} -start

client c1 {
"""
TAILER="""
}
client c1 -run
"""

def main():
    try:
        with open(sys.argv[1]) as controlset:
            lines = controlset.readlines()
            print HEADER
            for line in lines:
                if line.startswith("#"):
                    continue

                line = line.strip()

                if len(line) == 0:
                    continue

                typeId, OScode, UAString = line.split("|", 2)
                print "\ttxreq -hdr \"User-Agent: %s\"" % UAString
                print "\trxresp"
                print "\texpect resp.http.X-UA-Device-Type == \"%s\"" % typeId
                print "\texpect resp.http.X-UA-Device-OS   == \"%s\"" % OScode
                print "\n" # for readability
            print TAILER
    except IOError:
        print "Error while reading: %s" % sys.argv[1]

if __name__ == "__main__":
        main()
