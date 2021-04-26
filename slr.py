import multiprocessing
from os import remove
from os.path import expanduser
from platform import system

import PySimpleGUI as sg

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

# Define the window's contents
left_buttons = [
    [sg.Text("")],
    [logo_image],
    [sg.Text("")],
    [sg.Text("")],
]

layout = [
    [
        sg.Column(left_buttons,),
        sg.Column(
            [
                [
                    sg.Text("    Enter/edit URL mask:"),
                    sg.Multiline(key="-URLMask-", size=(65, 3)),
                    sg.Button("Clear", size=(None, 3), key="-Clear URL mask-"),
                ],
                [
                    sg.pin(
                        sg.Text(
                            (10 * " ") + "Image Options   " + "Image thumbnail size:",
                            key="-Element001-",
                        )
                    ),
                    sg.pin(
                        sg.Spin(
                            thumbsize_percentages,
                            initial_value="13",
                            size=(4, 4),
                            key="-ThumbSize-",
                        )
                    ),
                    sg.pin(sg.Text("(% of browser window width)", key="-Element002-",)),
                ],
                [
                    sg.pin(sg.Text(24 * " ", key="-Element003-",)),
                    sg.pin(
                        sg.Checkbox(
                            " Hide broken image links",
                            default=False,
                            key="-HideBorkedImages-",
                        )
                    ),
                ],
                [
                    sg.pin(
                        sg.Text((6 * " ") + "HTML File Options ", key="-Element004-",)
                    ),
                    sg.pin(sg.Text("Path:", key="-Element005-",)),
                    sg.pin(
                        sg.Input(key="-FilePath-", size=(33, 1), default_text=home_dir)
                    ),
                    sg.pin(sg.Text("Name:", key="-Element006-",)),
                    sg.pin(
                        sg.Input(
                            key="-FileName-", size=(17, 1), default_text="rustled.html"
                        )
                    ),
                    sg.pin(sg.Button("Reset", key="-HTML_Defaults-")),
                ],
                [
                    sg.pin(sg.Text(24 * " ", key="-Element007-",)),
                    sg.pin(
                        sg.Checkbox(
                            " Delete HTML file on Exit",
                            default=True,
                            key="-DeleteFile-",
                        )
                    ),
                ],
                [
                    sg.pin(sg.Text((12 * " ") + "Use browser  ", key="-Element008-",)),
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
                [
                    sg.Button("Rustle Up Them Links", size=(0, 3), key="-DoIt-",),
                    # sg.Text((50 * " ")),
                    sg.Text((24 * " ")),
                    sg.Button("Show Options", size=(0, 3), key="-Options-"),
                    sg.Text((24 * " ")),
                    sg.Button(" Exit ", size=(0, 3)),
                ],
            ]
        ),
    ],
]

# Create the window
window = sg.Window(window_title, layout, icon=icon_file, finalize=True)


def toggle_option_elements():
    option_elements = [
        "-Element001-",
        "-Element002-",
        "-Element003-",
        "-Element004-",
        "-Element005-",
        "-Element006-",
        "-Element007-",
        "-Element008-",
        "-ThumbSize-",
        "-HideBorkedImages-",
        "-FilePath-",
        "-FileName-",
        "-HTML_Defaults-",
        "-DeleteFile-",
        "-SelectedBrowser-",
    ]
    if window[option_elements[0]].visible:
        set_visibility = False
    else:
        set_visibility = True
    for element in option_elements:
        window[element].update(visible=set_visibility)


toggle_option_elements()

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # print(values)
    if event == sg.WINDOW_CLOSED or event == " Exit ":
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
        do_it(
            values["-URLMask-"],
            targetfile=values["-FilePath-"] + "/" + values["-FileName-"],
            selected_browser=values["-SelectedBrowser-"],
            thumbsize=values["-ThumbSize-"] + "%",
            hide_missing=values["-HideBorkedImages-"],
        )

    elif event == "-Clear URL mask-":
        window["-URLMask-"].update("")
    elif event == "-HTML_Defaults-":
        window["-FilePath-"].update(home_dir)
        window["-FileName-"].update("rustled.html")
    else:
        print(event, values)

# Finish up by removing from the screen
window.close()
