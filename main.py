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
import os, re, textwrap, threading, webbrowser

from lookup import supported_image_extensions


def check_sequence_definitions(sequence_defs):
    if not sequence_defs:
        raise Exception("No range definitions found")
    for each in sequence_defs:
        if not "-" in each:
            raise Exception("Hyphen missing between Start and End values")
        else:
            return True
    return False


def extract_sequence_definitions(URL_mask):
    """
    Given a well-formatted URL_mask, returns a list of tuples each of which
    containes the Start, End, and Stride values that define a range of integers.

    Supports one or more series with either increasing or decreasing values, negative
    or positive strides, and values which do or don't include leading zeros.
    """
    sequence_defs = re.findall(r"\{(.*?)\}", URL_mask)
    if not check_sequence_definitions(sequence_defs):
        exit()

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
        style = "<style>img {display: none}</style> <! In case of missing imgs: "
        style += "Script at end of BODY will display all that load successfully.)>"
        display_imgs_script = (
            """
        <! The following script displays all imgs that load succesfully.>
        <script>
            (function() {
                var allimgs = document.images;
                for (var i = 0; i < allimgs.length; i++) {
                    allimgs[i].onload = function() {
                        this.style.width      = "%s"
                        this.style.display    = "inline"
                        this.style.padding    = "5x"
                        this.style.position   = "relative"
                        this.style.visibility = "visible"
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
        style = f"<style>img {width: {thumbsize}; padding: 5x; position: relative; visibility: visible; display: inline}</style>"
        display_imgs_script = ""
    else:
        style = ""
        display_imgs_script = ""

    page_top = f"<HTML>\n<HEAD>\n{style}\n</HEAD>\n<BODY>\n"

    list_of_link_elements = ""
    for link in get_URL_list_generator(URL_mask):
        link = link.rstrip()
        list_of_link_elements += f'<a href="{link}">'  # add link
        if links_are_images:
            list_of_link_elements += f'<img src="{link}"></a>\n'  # link image
        else:
            list_of_link_elements += f"{link}</a><br>\n"  # link text

    credit = "<br>This page was generated by "
    credit += "<a href='https://github.com/therden/sequential-links-rustler'>"
    credit += "<i>Sequential Links Rustler</i></a>"

    page_bottom = f"<br>\n<i>{credit}</i>\n{display_imgs_script}\n</BODY>\n</HTML>"

    targetfile = "links.html" if targetfile == None else targetfile
    f = open(targetfile, "w")
    f.write(page_top + list_of_link_elements + page_bottom)
    f.close()
    targetfile = "file:///" + os.getcwd() + "/" + targetfile
    return targetfile


def are_links_images(URL_mask):
    URL_mask = URL_mask.strip().lower()
    _, ext = URL_mask[-6:].split(".")
    return ext in supported_image_extensions


# def open_file_in_firefox(URL):
#     """The name says it all."""
#     webbrowser.register("firefox", None, webbrowser.GenericBrowser("firefox"))
#     ff = webbrowser.get("firefox")
#     ff.open_new_tab(URL)
#
#
# def open_file_in_default_browser(URL):
#     """The name says it all."""
#     wb = webbrowser.get()
#     wb.open_new_tab(URL)


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
    # open_file_in_default_browser(URL)
    # open_file_in_selected_browser(URL, selected_browser=None)
    open_file_in_selected_browser(URL, selected_browser=selected_browser)


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
    # test_URL_generation_from_masks()
    # open_file_in_selected_browser("rustled.html", selected_browser="firefox")
    open_file_in_selected_browser("rustled.html", selected_browser="chromium-browser")
