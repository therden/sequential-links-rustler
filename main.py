"""
Functions which, given a "URL-mask" that describes a set of links that feature a
numeric progression, generates an HTML file containing those links and opens
that file in a web browser.

For instance, If example.com had a series of files pic01.jpg through pic09.jpg, the URL_mask
describing that series would be "http://example.com/{01-09;1}.jpg"

Note:  unlike Python's "range", the range definitions in clique's URL_mask are
will include the "stop" value.

See the doc string for each function for more details.
"""
import os, re, webbrowser


def check_range_definitions(range_defs):
    if not range_defs:
        raise Exception("No range definitions found")
    for each in range_defs:
        if not "-" in each:
            raise Exception("Hyphen missing between Start and End values")
        else:
            return True
    return False


def extract_range_definitions(URL_mask):
    """
    Given a well-formatted URL_mask, returns a list of tuples each of which
    containes the Start, End, and Stride values that define a range of integers.

    Supports one or more series with either increasing or decreasing values, negative
    or positive strides, and values which do or don't include leading zeros.
    """
    range_defs = re.findall(r"\{(.*?)\}", URL_mask)
    if not check_range_definitions(range_defs):
        exit()

    for each in range(URL_mask.count("{")):
        if ";" in range_defs[each]:
            span, stride = range_defs[each].split(";")
            stride = int(stride)
            start, end = span.split("-")
            start, end = int(start), int(end)
        else:
            start, end = range_defs[each].split("-")
            start, end = int(start), int(end)
            if start < end:
                stride = 1
            elif start > end:
                stride = -1
        endshift = 1 if stride > 0 else -1
        end += endshift
        range_defs[each] = (start, end, stride)
    return range_defs


def get_value_tuples(range_defs, vals=[]):
    """
    Given a list of range definitions, recursively determines all combinations
    of values that will be used to generate the individual links which they
    define, returning those as a list of tuples.
    """
    try:
        len(value_tuples)
    except:
        # if start < end:
        #     stride = 1
        # elif start > end:
        #     stride = -1
        value_tuples = []
    for each in range(*range_defs[0]):
        values_list = [*vals]
        values_list.append(each)
        if len(range_defs) > 1:
            next_level = get_value_tuples(range_defs[1:], vals=values_list)
            value_tuples += next_level
        else:
            value_tuples.append(tuple(values_list))
    return value_tuples


def rewrite_URL_mask(URL_mask):
    """
    Rewrites the URL_mask to support string format value substitution and
    returns the amended URL_mask as a string.

    For instance:  The URL_mask "http://example.com/{01-09;1}.jpg" would be
    amended and returned as "http://example.com/%02d.jpg"
    """
    bracketed = re.findall(r"(\{.*?\})", URL_mask)
    range_defs = re.findall(r"\{(.*?)\}", URL_mask)
    for counter in range(len(range_defs)):
        each = range_defs[counter]
        if ";" in each:
            span, _ = each.split(";")
            start, end = span.split("-")
        else:
            start, end = each.split("-")
        formatmask = "%01d"
        togo = bracketed[counter]
        if int(start[0]) * int(end[0]) == 0:
            formatmask = f"%0{len(start)}d"
        URL_mask = re.sub(rf"({togo})", formatmask, URL_mask, 1)
    return URL_mask


def get_URL_list_generator(URL_mask):
    """
    This function combines the previous three, accepting a URL_mask and returning
    a generator object that emits the URL links defined by that mask.
    """
    range_defs = extract_range_definitions(URL_mask)
    value_tuples = get_value_tuples(range_defs)
    new_URL_mask = rewrite_URL_mask(URL_mask)
    return (new_URL_mask % each for each in value_tuples)


def get_HTML_file(URL_mask, targetfile=None, hide_missing=False):
    """
    Accepts a URL_mask and saves all of the URL links which it defines to a
    file ("links.html" by default, but target file name can be overwritten.)
    """
    style = "<style>img {display: inline; padding: 5px; width: 150px; position: relative}</style>"
    credit = "Generated by <a href='https://github.com/therden/sequential-links-rustler'><i>Sequential Links Rustler</i></a>"
    if hide_missing:
        javascript = """<script>
        (function() {
        var allimgs = document.images;
        for (var i = 0; i < allimgs.length; i++) {
        allimgs[i].onerror = function() {
        this.style.width = "0px";
        this.style.padding = "0px";
        this.style.float = "left";
        this.style.visibility = "hidden";
        }
        }
        })();
        </script>"""
    else:
        javascript = ""
    top = f"<HTML>\n<HEAD>\n{style}\n</HEAD>\n<BODY>\n"
    body = ""
    for link in get_URL_list_generator(URL_mask):
        body += f'<a href="{link}">'
        body += f'<img src="{link}"></a>\n'
    bottom = f"<br><i>{credit}</i>\n{javascript}\n</BODY>\n</HTML>"
    targetfile = "links.html" if targetfile == None else targetfile
    f = open(targetfile, "w")
    f.write(top + body + bottom)
    f.close()
    targetfile = "file:///" + os.getcwd() + "/" + targetfile
    return targetfile


def open_file_in_firefox(URL):
    """The name says it all."""
    webbrowser.register("firefox", None, webbrowser.GenericBrowser("firefox"))
    ff = webbrowser.get("firefox")
    ff.open_new_tab(URL)


def make_and_open_HTML_file_from_URL_mask(
    URL_mask, targetfile=None, hide_missing=False
):
    """Again: the name says it all.  Uses the functions defined above."""
    URL = get_HTML_file(URL_mask, targetfile=targetfile, hide_missing=hide_missing)
    open_file_in_firefox(URL)


rustle_up_some_links = make_and_open_HTML_file_from_URL_mask


def test_URL_generation_from_masks():
    """
    This function prints the links generated by a set of URL_masks which feature
    - ascending and descending series
    - strides of different lengths
    - values with leading zeroes
    - incorporating multiple, separately defind series within a single URL_mask
    """
    test_masks = [
        "http://www.example.com/gallery/pic{1-4}",
        "http://www.example.com/gallery/pic{1-5;2}",
        "http://www.example.com/gallery/pic{5-1;-2}",
        "http://www.example.com/gallery/pic{01-05;1}",
        "http://www.example.com/gallery/pic{005-000;-2}",
        "http://www.example.com/gallery{1-2;1}/set{03-06}/pic{007-010;2}",
    ]
    for URL_mask in test_masks:
        print(f"Test against mask {URL_mask}.")
        for each in get_URL_list_generator(URL_mask):
            print("  ", each)
        print("\n")


if __name__ == "__main__":
    test_URL_generation_from_masks()
