import multiprocessing
from os import remove
from os.path import expanduser
from platform import system

import PySimpleGUI as sg

from main import check_URL_mask
from main import rustle_up_some_links as do_it
from lookup import supported_browsers


# Set variables used the application window
home_dir = expanduser("~")
icon_file = {
    "linux": "assets/logo.png",
    "windows": "assets/rustler.ico",
    "darwin": "assets/logo.png",  # I _think_ this will work
}[system().lower()]
logo_image = sg.Image(
    filename="assets/logo.png",
    data=None,
    background_color=None,
    size=(120, 136),
    pad=None,
    key="logo",
    tooltip=None,
    right_click_menu=None,
    visible=True,
    enable_events=False,
    metadata=None,
)
thumbsize_percentages = [str(each) for each in range(1, 101)]
window_title = "Sequential Links Rustler"
logo_column = sg.Column([[logo_image]])
main_column = sg.Column(
    [
        [
            sg.Text("", size=(22, None)),
            sg.Button(
                "Rustle Up Them Links", size=(18, 2), bind_return_key=True, key="-DoIt-"
            ),
            sg.Text("", size=(1, None)),
            sg.Button("Show Options", size=(12, 2), key="-Options-"),
            sg.Text("", size=(14, None)),
            sg.Button("Exit", size=(4, 2)),
        ],
        [
            sg.Text("\nEnter/edit URL mask:", size=(22, 3), justification="right",),
            sg.Multiline(key="-URLMask-", size=(65, 3), focus=True),
            sg.Button("Clear", size=(None, 1), key="-Clear URL mask-"),
        ],
        [
            sg.pin(
                sg.Text(
                    "Image Options ", size=(22, None), justification="right", k="e0"
                ),
            ),
            sg.pin(sg.Text("Image thumbnail size:", k="e1")),
            sg.pin(
                sg.Spin(
                    thumbsize_percentages,
                    initial_value="13",
                    size=(4, 4),
                    key="-ThumbSize-",
                )
            ),
            sg.pin(sg.Text("(% of browser window width)", k="e2")),
        ],
        [
            sg.pin(sg.Text("", size=(21, None), justification="right", k="e3"),),
            sg.pin(
                sg.Checkbox(
                    " Hide broken image links", default=False, key="-HideBorkedImages-",
                )
            ),
        ],
        [
            sg.pin(
                sg.Text(
                    "HTML File Options ",
                    size=(22, None),
                    justification="right",
                    k="e4",
                )
            ),
            sg.pin(sg.Text("Path:", k="e5")),
            sg.pin(sg.Input(key="-FilePath-", size=(33, 1), default_text=home_dir)),
            sg.pin(sg.Text("Name:", k="e6")),
            sg.pin(
                sg.Input(key="-FileName-", size=(17, 1), default_text="rustled.html",)
            ),
            sg.pin(sg.Button("Reset", key="-HTML_Defaults-")),
        ],
        [
            sg.pin(sg.Text("", size=(21, None), k="e7")),
            sg.pin(
                sg.Checkbox(
                    " Delete HTML file on Exit", default=True, key="-DeleteFile-",
                )
            ),
        ],
        [
            sg.pin(
                sg.Text("Choose browser  ", size=(22, 1), justification="right", k="e8")
            ),
            sg.pin(
                sg.Combo(
                    supported_browsers,
                    default_value="system_default",
                    size=(20, 1),
                    pad=(1, 1),
                    readonly=True,
                    key="-SelectedBrowser-",
                )
            ),
        ],
    ]
)

layout = [[logo_column, main_column]]

# Create the window
window = sg.Window(window_title, layout, icon=icon_file, finalize=True)


def toggle_option_elements():
    option_elements = [
        "-ThumbSize-",
        "-HideBorkedImages-",
        "-FilePath-",
        "-FileName-",
        "-HTML_Defaults-",
        "-DeleteFile-",
        "-SelectedBrowser-",
        "e0",
        "e1",
        "e2",
        "e3",
        "e4",
        "e5",
        "e6",
        "e7",
        "e8",
    ]
    if window[option_elements[0]].visible:
        set_visibility = False
    else:
        set_visibility = True
    for element in option_elements:
        window[element].update(visible=set_visibility)


toggle_option_elements()


while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit":
        if values["-DeleteFile-"]:
            try:
                remove(values["-FilePath-"] + "/" + values["-FileName-"])
            except Exception:
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
