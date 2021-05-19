"""
Functions which, given a "URL-mask" that describes a set of links that feature a
numeric progression, generates an HTML file containing those links and opens
that file in a web browser.

For instance, If example.com had a series of files pic01.jpg through pic09.jpg,
the URL_mask describing that series would be "http://example.com/{01-09;1}.jpg"

Note:  unlike Python's built-in "range" function, the values produced by the
range definitions in Sequential Link Rustler's URL_mask will _include_ the
"stop" value.

See the doc string for each function for more details.
"""
import os, re, textwrap, threading, webbrowser
from collections import Counter
from os.path import expanduser

from lookup import supported_image_extensions


def check_URL_mask(URL_mask):
    error_prefix = "URL mask error:\n"
    if ":" in URL_mask:
        URL_prefix, _ = URL_mask.split(":")
        if URL_prefix.lower() not in ("file, http, https"):
            return f"{error_prefix}{URL_prefix} not supported in URL mask."
    else:
        return f"{error_prefix}URL mask must begin: file:, http:, or https:"
    mask_char_counts = Counter(URL_mask)
    left_b, right_b = mask_char_counts["{"], mask_char_counts["}"]
    # test for no curly brackets
    if left_b + right_b == 0:
        return f"{error_prefix}No curly brackets found in URL Mask."
    # test for curly bracket
    elif left_b != right_b:
        if left_b > right_b:
            return "%s %s more '{' than '}'." % (error_prefix, left_b - right_b)
        else:
            return "%s %s more '}' than '{'." % (error_prefix, right_b - left_b)
    else:
        # test for any non-empty pair of curly brackets
        sequence_defs = re.findall(r"\{(.*?)\}", URL_mask)
        if len(sequence_defs[0]) == 0:
            return f"{error_prefix}No sequence definitions found within curly brackets."
        else:  # test contents of each pair of brackets
            allowed_chars = [str(x) for x in range(0, 10)] + ["-", ";"]
            illegal_chars = []
            for each_def in sequence_defs:
                def_chars = Counter(each_def).keys()
                for key in def_chars:
                    if not key in allowed_chars:
                        illegal_chars.append(key)
                if illegal_chars:
                    return f"{error_prefix}Illegal characters {illegal_chars} found in sequence definition."
                # test for hyphen
                if not "-" in each_def:
                    return f"{error_prefix}Sequence definition missing hyphen."
                # test whether an interval is defined
                elif ";" in each_def:
                    # test that interval is specified and is anq = (Appointment
                    range_def, stride = each_def.split(";")
                    try:
                        int(stride)
                    except ValueError:
                        return f"{error_prefix}Interval after ';' must be an integer."
                    # test that Start and Stop values are integers
                    start_val, stop_val = range_def.split("-")
                    try:
                        int(start_val)
                    except ValueError:
                        return f"{error_prefix}'Start' value must be an integer."
                    try:
                        int(stop_val)
                    except ValueError:
                        return f"{error_prefix}'Stop' value must be an integer."
                else:
                    # just test that Start and Stop values are integers
                    start_val, stop_val = each_def.split("-")
                    try:
                        int(start_val)
                    except ValueError:
                        return f"{error_prefix}'Start' value must be an integer."
                    try:
                        int(stop_val)
                    except ValueError:
                        return f"{error_prefix}'Stop' value must be an integer."
    return "Okay"


def extract_sequence_definitions(URL_mask):
    """
    Given a well-formatted URL_mask, returns a list of tuples each of which
    containes the Start, End, and Stride values that define a range of integers.

    Supports one or more series with either increasing or decreasing values, negative
    or positive strides, and values which do or don't include leading zeros.
    """
    sequence_defs = re.findall(r"\{(.*?)\}", URL_mask)

    for each in range(URL_mask.count("{")):
        if ";" in sequence_defs[each]:
            span, stride = sequence_defs[each].split(";")
            stride = int(stride)
            start, end = span.split("-")
            start, end = int(start), int(end)
        else:
            stride = 1
            start, end = sequence_defs[each].split("-")
            start, end = int(start), int(end)
        if start > end:
            stride = -stride
        endshift = 1 if stride > 0 else -1
        end += endshift
        sequence_defs[each] = (start, end, stride)
    return sequence_defs


def get_value_tuples(sequence_defs, vals=[]):
    """
    Given a list of range definitions, recursively determines all combinations
    of values that will be used to generate the individual links which they
    define, returning those as a list of tuples.
    """
    try:
        len(value_tuples)
    except:
        value_tuples = []
    for each in range(*sequence_defs[0]):
        values_list = [*vals]
        values_list.append(each)
        if len(sequence_defs) > 1:
            next_level = get_value_tuples(sequence_defs[1:], vals=values_list)
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
    sequence_defs = re.findall(r"\{(.*?)\}", URL_mask)
    for counter in range(len(sequence_defs)):
        each = sequence_defs[counter]
        if ";" in each:
            span, _ = each.split(";")
            start, end = span.split("-")
        else:
            start, end = each.split("-")
        formatmask = "%01d"
        togo = bracketed[counter]
        if int(start) <= int(end) and start[0] == "0":
            formatmask = f"%0{len(start)}d"
        elif int(start) > int(end) and end[0] == "0":
            formatmask = f"%0{len(end)}d"
        URL_mask = re.sub(rf"({togo})", formatmask, URL_mask, 1)
    return URL_mask


def get_URL_list_generator(URL_mask):
    """
    This function combines the previous three, accepting a URL_mask and returning
    a generator object that emits the URL links defined by that mask.
    """
    sequence_defs = extract_sequence_definitions(URL_mask)
    value_tuples = get_value_tuples(sequence_defs)
    new_URL_mask = rewrite_URL_mask(URL_mask)
    return (new_URL_mask % each for each in value_tuples)


def get_HTML_file(URL_mask, targetfile=None, thumbsize="16%", hide_missing=False):
    """
    Accepts a URL_mask and saves all of the URL links which it defines to a
    file ("links.html" by default, but target file name can be overwritten.)
    """
    links_are_images = are_links_images(URL_mask)
    if links_are_images and hide_missing:
        style = "<style>img {display: none; vertical-align: bottom}</style>"
        style += "<! In case any images are missing: "
        style += "Script at end of BODY will display all that load successfully.)>"
        display_imgs_script = (
            """
            <! The following script displays all imgs that load succesfully,
            and styles the Rustler logo in the credits.>
            <script>
                (function() {
                    var allimgs = document.getElementById("links").querySelectorAll("img");
                    for (var i = 0; i < allimgs.length; i++) {
                        allimgs[i].onload = function() {
                            this.style.width      = "%s"
                            this.style.display    = "inline"
                            this.style.padding    = "5x"
                            this.style.visibility = "visible"
                        }
                    }
                    {
                    var logo = document.querySelector(".logo");
                        logo.onload = function() {
                            this.style.display     = "inline"
                            this.style.width       = "40px"
                            this.style.top         = "15px"
                            this.style.position    = "relative"
                            this.style.visibility  = "visible"
                        }
                    }
                })
                ();
            </script>
            """
            % thumbsize
        )
        display_imgs_script = textwrap.dedent(display_imgs_script)
    elif links_are_images:
        style = "<style>img {width:13%; padding:5x; visibility:visible; display:inline; vertical-align:bottom}</style>"
        display_imgs_script = ""
    else:
        style = ""
        display_imgs_script = ""

    page_top = f"<HTML>\n<HEAD>\n{style}\n</HEAD>\n<BODY>\n"

    list_of_link_elements = "<div id='links'>\n"
    for link in get_URL_list_generator(URL_mask):
        link = link.rstrip()
        list_of_link_elements += f'<a href="{link}">'  # add link
        if links_are_images:
            list_of_link_elements += f'<img src="{link}"></a>\n'  # link image
        else:
            list_of_link_elements += f"{link}</a><br>\n"  # link text
    list_of_link_elements += "</div>\n"

    repoURL = "https://github.com/therden/sequential-links-rustler"
    logoURL = "https://raw.githubusercontent.com/therden/sequential-links-rustler/main/assets/logo.png"
    credit = f"<i>This page was generated by the <a href='{repoURL}'>Sequential Links Rustler</a></i> "
    credit += f"<img class='logo' src='{logoURL}' style='display:inline;width:40px;top:15px;position:relative;visibility:visible'>"

    page_bottom = f"{credit}\n{display_imgs_script}</BODY>\n</HTML>"

    if not targetfile:
        targetfile = expanduser("~") + "/" + rustled.html
    f = open(targetfile, "w")
    f.write(page_top + list_of_link_elements + page_bottom)
    f.close()
    targetfile = "file:///" + targetfile
    return targetfile


def are_links_images(URL_mask):
    URL_mask = URL_mask.strip().lower()
    _, ext = URL_mask[-6:].split(".")
    return ext in supported_image_extensions


def open_file_in_selected_browser(URL, selected_browser=None):
    """The name says it all."""
    if selected_browser in ("system_default", None):
        wb = webbrowser.get()
    else:
        webbrowser.register(
            selected_browser, None, webbrowser.GenericBrowser(selected_browser)
        )
        wb = webbrowser.get(using=selected_browser)
    browser_process = lambda: wb.open_new_tab(URL)
    t = threading.Thread(target=browser_process)
    t.start()


def make_and_open_HTML_file_from_URL_mask(
    URL_mask, targetfile=None, selected_browser=None, thumbsize="16%", hide_missing=True
):
    """Again: the name says it all.  Uses the functions defined above."""
    URL = get_HTML_file(
        URL_mask, targetfile=targetfile, thumbsize=thumbsize, hide_missing=hide_missing
    )
    open_file_in_selected_browser(URL, selected_browser=selected_browser)


rustle_up_some_links = make_and_open_HTML_file_from_URL_mask


def convert_URL_to_mask(URL):
    if URL.count("{") + URL.count("}"):  # URL already has curly brackets
        URL_mask = URL
    else:
        URL_mask = re.sub('(\d+)', '{\\1-\\1}', URL)
    return URL_mask


def test_URL_generation_from_masks():
    """
    This function prints the links generated by a set of URL_masks which feature
    - ascending and descending series
    - strides of different lengths
    - values with leading zeroes
    - incorporating multiple, separately defind series within a single URL_mask
    """
    test_masks = [
        "http://www.example.com/gallery/pic{0-4}",
        "http://www.example.com/gallery/pic{4-0}",
        "http://www.example.com/gallery/pic{0-10;2}",
        "http://www.example.com/gallery/pic{05-00}",
        "http://www.example.com/gallery/pic{005-000}",
        "http://www.example.com/gallery{1-2;1}/set{03-06}/pic{007-010;2}",
    ]
    for URL_mask in test_masks:
        print(f"Test against mask {URL_mask}.")
        for each in get_URL_list_generator(URL_mask):
            print("  ", each)
        print("\n")


if __name__ == "__main__":
    test_URL_generation_from_masks()
