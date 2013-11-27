#!/usr/bin/python

# Generate a varnishtest script to validate the preclassified
# U-A strings in the control set.

import errno, sys, argparse

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

def flush(batchNum, header, buff, tailer, outputdir="."):
    path = outputdir + "9" + str(batchNum).zfill(4) + "-from-controlset.vtc"
    with open(path, "w+") as f:
        f.write(header)
        f.write(buff)
        f.write(tailer)

def main(inputfile, outputdir, splitcount=76):
    try:
        with open(inputfile) as controlset:
            lines = controlset.readlines()
            buff = ""
            i = 1
            batchNum = 1
            for line in lines:
                if line.startswith("#"):
                    continue

                line = line.strip()

                if len(line) == 0:
                    continue

                flushed = False
                typeId, OScode, UAString = line.split("|", 2)
                buff = buff + "\ttxreq -hdr \"User-Agent: %s\"\n" % UAString
                buff = buff + "\trxresp\n"
                buff = buff + "\texpect resp.http.X-UA-Device-Type == \"%s\"\n" % typeId
                buff = buff + "\texpect resp.http.X-UA-Device-OS   == \"%s\"\n" % OScode
                buff = buff + "\n" # for readability

                if (0 == ((i + 1) % splitcount)):
                    flush(batchNum, HEADER, buff, TAILER, outputdir)
                    flushed = True
                    batchNum = batchNum + 1
                    buff = ""
                i = i + 1

        if (False == flushed):
            flush(batchNum, HEADER, buff, TAILER, outputdir)

    except IOError:
        print "Error while reading: %s" % sys.argv[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="Input CSV file", type=str)
    parser.add_argument("outputdir", help="Output directory", type=str)
    parser.add_argument("-s", "--splitcount", help="Determine after how much tests we must split the files", type=int, default=76)
    args = parser.parse_args()
    main(args.inputfile, args.outputdir, args.splitcount)
