Varnish Device Detect
=====================

Varnish subroutine to detect device (mobile, tablet and desktop)

Quick Start
-----------

Table of contents
-----------------

1. [Installation](#installation)
2. [Getting started](#getting-started)
3. [Usage](#usage)
4. [Run the test](#run-the-test)
5. [Contributing](#contributing)
6. [Requirements](#requirements)
7. [Authors](#authors)
8. [License](#license)

Installation
------------

```shell
git clone http://git.thebigbrainscompany.com/borisguery/varnish-device-detect.git varnish/routines/folder/or/whatever
```

Getting started
---------------

Varnish subroutines are a **really** simple way to somewhat modularize your VCL, they are actually not functions as they don't take arguments nor they return anything.

To make use of this subroutine, you have to call it from inside the `vcl_recv` subroutine. It will set two new header in the `req` object which allow you to conditionally work
with it.

Usage
-----

```c
include "routines/devicedetect.vcl";

sub vcl_recv {
    call devicedetect;

    if (req.http.X-UA-Device-Type == "mobile") {
        error 701 regsub(req.http.host, "^www\.(.*)", "http://mobile.\1") + req.url; //Capture everything after the www. and place it after a http://
    }
}

sub vcl_error {
    // Redirect to mobile host
    if (obj.status == 701) {
        set obj.http.Location = obj.response;
        set obj.status = 302;

        return(deliver);
    }
}
```

Run the test
------------

```shell
make test
```

Contributing
------------

1. Take a look at the [list of issues](http://github.com/borisguery/varnish-device-detection/issues).
2. Fork
3. Write a test (for either new feature or bug)
4. Make a PR

Requirements
------------

* Varnish 3.x
* Python 2.x

Authors
-------

* Boris Guéry <<guery.b@gmail.com>> - http://borisguery.com - [@borisguery](https://twitter.com/borisguery)

License
-------

`Varnish Device Dectect` is licensed under the MIT License - see the LICENSE file for details
