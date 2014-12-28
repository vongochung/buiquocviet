// use: <time class="timesince" datetime="{{post.date|date:'c'}}">{{post.date|date:"c"}}</time>
(function(factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as anonymous module.
        define(['jquery'], factory);
    } else {
        // Browser globals.
        factory(jQuery);
    }
}(function($) {
    $.timesince = function(timestamp) {
        if (timestamp instanceof Date) {
            return timeSince(timestamp);
        } else if (typeof timestamp === 'string') {
            return timeSince($.timesince.parse(timestamp));
        } else if (typeof timestamp === 'number') {
            return timeSince(new Date(timestamp));
        } else {
            // It's an element.
            return timeSince($.timesince.datetime($(timestamp)));
        }
    };

    $.extend($.timesince, {
        options: {
            refreshMs: 60 * 1000, // 1 minute
            strings: {
                prefixAgo: null,
                prefixFromNow: null,
                suffixAgo: "trước",
                suffixFromNow: "Ngay tức thì",
                minute: "phút",
                minutes: "phút",
                hour: "giờ",
                hours: "giờ",
                day: "ngày",
                days: "ngày",
                week: "tuần",
                weeks: "tuần",
                month: "tháng",
                months: "tháng",
                year: "năm",
                years: "năm"
            }
        },
        chunks: [
            [60 * 60 * 24 * 365, "year", "years"],
            [60 * 60 * 24 * 30, "month", "months"],
            [60 * 60 * 24 * 7, "week", "weeks"],
            [60 * 60 * 24, "day", "days"],
            [60 * 60, "hour", "hours"],
            [60, "minute", "minutes"],
        ],
        timeSince: function(deltaMs) {
            var strings = this.options.strings,
                seconds = Math.abs(deltaMs) / 1000,
                prefix,
                suffix,
                i;

            if (deltaMs < 0) {
                prefix = strings.prefixFromNow;
                suffix = strings.suffixFromNow;
            } else {
                prefix = strings.prefixAgo;
                suffix = strings.suffixAgo;
            }

            prefix = (prefix ? prefix + " " : "");
            suffix = (suffix ? " " + suffix : "");

            if (seconds < 60) {
                return prefix + "0 " + strings.minutes + suffix;
            }

            for (i = 0; i < this.chunks.length; i++) {
                var chunk = this.chunks[i],
                    chunkSecs = chunk[0],
                    count = Math.floor(seconds / chunkSecs);

                if (count != 0) {
                    var s = prefix + this.getChunkText(chunk, count);

                    if (i + 1 < this.chunks.length) {
                        // Get the second item.
                        var chunk2 = this.chunks[i + 1],
                            count2 = Math.floor(
                                (seconds - (chunkSecs * count)) / chunk2[0]);

                        if (count2 != 0) {
                            s += ", " + this.getChunkText(chunk2, count2);
                        }
                    }

                    return s + suffix;
                }
            }

            // We shouldn't have reached here.
            return ''
        },
        getChunkText: function(chunk, n) {
            var type = (n === 1 ? chunk[1] : chunk[2]);

            return n + " " + this.options.strings[type];
        },
        parse: function(iso8601) {
            var s = $.trim(iso8601);
            s = s.replace(/\.\d\d\d+/,""); // remove milliseconds
            s = s.replace(/-/,"/").replace(/-/,"/");
            s = s.replace(/T/," ").replace(/Z/," UTC");
            s = s.replace(/([\+\-]\d\d)\:?(\d\d)/," $1$2"); // -04:00 -> -0400
            return new Date(s);
        },
        datetime: function(el) {
            var iso8601 = this.isTime(el)
                          ? el.attr("datetime")
                          : el.attr("title");
            return this.parse(iso8601);
        },
        isTime: function(el) {
            // jQuery's `is()` doesn't play well with HTML5 in IE
            return el[0].tagName.toLowerCase() === "time";
        }
    });

    $.fn.timesince = function(options) {
        var self = this,
            timerCnx,
            refreshMs;

        options = $.extend(options, $.timesince.options);
        refreshMs = options.refreshMs;

        if (refreshMs > 0) {
            timerCnx = setInterval(function() {
                self.each(function() {
                    refresh($(this), timerCnx);
                });
            }, refreshMs);
        }

        return this.each(function() {
            var el = $(this),
                text = $.trim(el.text());

            el.data('timesince', {
                datetime: $.timesince.datetime(el)
            });

            if (text.length > 0 && (!$.timesince.isTime(el) ||
                                    !el.attr("title"))) {
                el.attr("title", text);
            }

            refresh(el);
        });
    };

    function refresh(el, timerCnx) {
        var data = el.data('timesince');

        if (data) {
            el.text($.timesince.timeSince(
                new Date().getTime() - data.datetime.getTime()));
        } else {
            clearInterval(timerCnx);
        }

        return el;
    }

    // IE6 doesn't understand the <time> tag, so create it.
    document.createElement("time");
}));