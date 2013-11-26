sub devicedetect {
    unset req.http.X-UA-Device-Type;

    // sensible defaults
    set req.http.X-UA-Device-Type = "generic";
    set req.http.X-UA-Device-OS   = "unknown";

    if (req.http.Cookie ~ "(?i)X-UA-Device-Force") {
    } else {
        if (req.http.User-Agent ~ "(?i)ipad") {
            set req.http.X-UA-Device-Type = "tablet";
            set req.http.X-UA-Device-OS   = "ios";
        } elsif (req.http.User-Agent ~ "(?i)ip(hone|od)") {
            set req.http.X-UA-Device-Type = "mobile";
            set req.http.X-UA-Device-OS   = "ios";
        } elsif (req.http.User-Agent ~ "(?i)android") {
            // http://stackoverflow.com/questions/5341637/how-do-detect-android-tablets-in-general-useragent
            set req.http.X-UA-Device-OS = "android";
            if (req.http.User-Agent ~ "(?i)android.*(mobile|mini)") {
                set req.http.X-UA-Device-Type = "mobile";
            } elseif (req.http.User-Agent ~ "(?i)android 3") { // looks like android 3/honeycomb are mostly tablet-only
                set req.http.X-UA-Device-Type = "tablet";
            }
            // fallback on tablet
            set req.http.X-UA-Device-Type = "tablet";
        } elseif (req.http.user-Agent ~ "(?i)windows") {
            set req.http.X-UA-Device-OS = "windows";
        }
    }
}
