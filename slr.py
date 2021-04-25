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
                    sg.Text((10 * " ") + "Image Options   " + "Image thumbnail size:"),
                    sg.Spin(
                        thumbsize_percentages,
                        initial_value="13",
                        size=(4, 4),
                        key="-ThumbSize-",
                    ),
                    sg.Text("(% of browser window width)"),
                ],
                [
                    sg.Text(24 * " "),
                    sg.Checkbox(
                        " Hide empty links (images only)",
                        default=True,
                        key="-HideBorkedImages-",
                    ),
                ],
                [
                    sg.Text((11 * " ") + "File Options "),
                    sg.Text("Path:"),
                    sg.Input(key="-FilePath-", size=(33, 1), default_text=home_dir),
                    sg.Text("Name:"),
                    sg.Input(
                        key="-FileName-", size=(17, 1), default_text="rustled.html"
                    ),
                ],
                [
                    sg.Text(24 * " "),
                    sg.Checkbox(
                        " Delete file on Exit", default=True, key="-DeleteFile-",
                    ),
                ],
                [
                    sg.Text((12 * " ") + "Use browser  "),
                    sg.Combo(
                        supported_browsers,
                        default_value="system_default",
                        size=(20, 1),
                        pad=(1, 1),
                        readonly=True,
                        key="-SelectedBrowser-",
                    ),
                ],
                [
                    sg.Button("Rustle Up Them Links", size=(0, 3), key="-DoIt-",),
                    sg.Text((67 * " ")),
                    # sg.Text((50 * " ")),
                    # sg.Button("Show Options", size=(0, 3), key="-Options-"),
                    sg.Button(" Exit ", size=(0, 3)),
                ],
            ]
        ),
    ],
]

# Create the window
window = sg.Window(window_title, layout, icon=icon_file)

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
    else:
        print(event, values)

# Finish up by removing from the screen
window.close()
