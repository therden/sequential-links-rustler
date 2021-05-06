import multiprocessing
from os import remove
from os.path import expanduser
from platform import system

import PySimpleGUI as sg

from main import check_URL_mask
from main import rustle_up_some_links as do_it
from lookup import supported_browsers

# set variables used by the gui
home_dir = expanduser("~")
icons = {
    "linux": "assets/logo.png",
    "windows": "assets/rustler.ico",
    "darwin": "assets/logo.png",  # I _think_ this will work
}
host_os = system().lower()
icon_file = icons[host_os]
rustler_logo = sg.Image(
    filename="assets/logo.png",
    size=(120, 136),
    key="logo",
    visible=True,
    enable_events=False,
)
window_title = "Sequential Links Rustler"

# create Fixed gui elements
button_rustle = sg.Button(
    "Rustle\nUp\nSome\nLinks",
    size=(11, 6),
    font=("Any", 12),
    bind_return_key=True,
    key="-DoIt-",
)
button_options = sg.Button(
    "Show Options", size=(16, 2), font=("Any", 12), key="-Options-"
)
button_exit = sg.Button("Exit", size=(8, 2), font=("Any", 12))
label_URLmask = sg.Text(
    " Enter or Edit URL mask below", text_color="black", font=("Any", 10)
)
input_URLmask = sg.Multiline(key="-URLMask-", size=(62, 4), focus=True)
button_clear = sg.Button("Clear URL mask", size=(None, 1), key="-Clear URL mask-")

# create Options gui elements
button_reset = sg.Button("Restore default filepath and name", key="-HTML_Defaults-")
label_imagesize = sg.Text("Image thumbnail size:")
label_file_options = sg.Text(
    "HTML File Options ", size=(18, 1), text_color="black", justification="right",
)
spin_thumbsize = sg.Spin(
    [str(each) for each in range(1, 101)],
    initial_value="13",
    size=(4, 4),
    key="-ThumbSize-",
)
label_percent_width = sg.Text("(% of browser window width)")
input_hideborked = sg.Checkbox(
    " Hide broken image links", default=False, key="-HideBorkedImages-"
)
label_filepath = sg.Text("Path:")
input_filepath = sg.Input(key="-FilePath-", size=(31, 1), default_text=home_dir)
label_filename = sg.Text("Name:")
input_filename = sg.Input(key="-FileName-", size=(15, 1), default_text="rustled.html")
input_delete = sg.Checkbox(
    " Delete HTML file on Exit", default=True, key="-DeleteFile-"
)
label_browser = sg.Text(
    "Choose browser ", size=(18, 2), text_color="black", justification="right"
)
input_browser = sg.Combo(
    supported_browsers,
    default_value="system_default",
    size=(20, 1),
    pad=(1, 1),
    readonly=True,
    key="-SelectedBrowser-",
)

# create layout
fixed_column_1 = sg.Column(
    [
        [sg.Text(" ")],
        [rustler_logo],
        [sg.Text(" ")],
        [button_clear],
    ],
    element_justification="right",
)

fixed_column_2 = sg.Column(
    [
        [sg.Text(" ")],
        [
            button_rustle,
            sg.vbottom(button_options),
            sg.vbottom(button_exit)
        ],
        [sg.Text(" ")],
        [label_URLmask],
        [input_URLmask],
    ],
)


options_column = sg.Column(
    [
        [
            sg.Frame(
                "Image Options",
                [
                    [label_imagesize, spin_thumbsize, label_percent_width],
                    [input_hideborked],
                ],
                title_color="black",
            )
        ],
        [
            sg.Frame(
                "HTML File Options",
                [
                    [
                        label_filepath,
                        input_filepath,
                        label_filename,
                        input_filename,
                    ],
                    [sg.Text("", size=(4, 1)), button_reset],
                    [input_delete],
                ],
                title_color="black",
            )
        ],
        [
            sg.Frame(
                "Choose Browser",
                [[input_browser]],
                title_color="black",
            )
        ],
    ],
    key="options",
)

column_a = sg.Column([[fixed_column_1]])
column_b = sg.Column(
    [
        [fixed_column_2],
        [sg.pin(options_column, shrink=True, expand_x=True, expand_y=True)]
    ]
)
layout = [[sg.vtop(column_a), column_b]]

# Create the window
window = sg.Window(window_title, layout, font=("Any", 10), icon=icon_file, finalize=True)


def toggle_option_elements():
    window["options"].update(visible = not window["options"].visible)


toggle_option_elements()

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit":
        try:
            if values["-DeleteFile-"]:
                try:
                    remove(values["-FilePath-"] + "/" + values["-FileName-"])
                except Exception:
                    pass
        except:
            pass
        break
    elif event == "-Options-":
        toggle_option_elements()
        if window["-Options-"].get_text() == "Show Options":
            window["-Options-"].update(text="Hide Options")
        else:
            window["-Options-"].update(text="Show Options")
    elif event == "-DoIt-":
        check_result = check_URL_mask(values["-URLMask-"])
        if check_result == "Okay":
            do_it(
                values["-URLMask-"],
                targetfile=values["-FilePath-"] + "/" + values["-FileName-"],
                selected_browser=values["-SelectedBrowser-"],
                thumbsize=values["-ThumbSize-"] + "%",
                hide_missing=values["-HideBorkedImages-"],
            )
        else:
            sg.popup_ok(check_result)
    elif event == "-Clear URL mask-":
        window["-URLMask-"].update("")
    elif event == "-HTML_Defaults-":
        window["-FilePath-"].update(home_dir)
        window["-FileName-"].update("rustled.html")
    else:
        print(event, values)

# Finish up by removing from the screen
window.close()
