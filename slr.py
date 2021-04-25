import multiprocessing, platform, random

import PySimpleGUI as sg

from main import rustle_up_some_links as do_it
from lookup import supported_browsers


# Define the window's contents
window_title = "Sequential Links Rustler"
thumbsize_percentages = [str(each) for each in range(1, 101)]
icon_file = {
    "linux": "assets/logo.png",
    "windows": "assets/rustler.ico",
    "darwin": "assets/logo.png",  # I _think_ this will work
}[platform.system().lower()]

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

left_buttons = [
    [sg.Text("")],
    [logo_image],
    [sg.Text("")],
    [sg.Text("")],
    # [sg.Button("2")],
    # [sg.Button("3")],
]

# resource_frame = [
#     [sg.Text("Enter/paste original URL:"), sg.Input(key="-Resource-")],
#     [sg.Text("Edit URL mask:"), sg.Input(key="-ResourceMask-")],
# ]
#
# thumbnail_frame = [
#     [sg.Text("Enter/paste original URL:"), sg.Input(key="-Thumbnail-")],
#     [sg.Text("Edit URL mask:"), sg.Input(key="-ThumbnailMask-")],
# ]
#
# url_frames = [resource_frame, thumbnail_frame]

layout = [
    [
        sg.Column(left_buttons,),
        sg.Column(
            [
                # [sg.Text("Enter/paste original URL:"), sg.Input(key="-Resource-")],
                # [sg.Button("Copy above URL below")],
                [
                    sg.Text("Enter and edit URL mask:"),
                    # sg.Input(key="-URLMask-", size=(65, 1)),
                    sg.Multiline(key="-URLMask-", size=(65, 3)),
                    sg.Button("Clear", key="-Clear URL mask-"),
                ],
                # [sg.Text("Enter/paste original URL:"), sg.Input(key="-Thumbnail-")],
                # [sg.Text("Edit URL mask:"), sg.Input(key="-ThumbnailMask-")],
                # [sg.Text("")],
                [
                    sg.Text((26 * " ") + "Image thumbnail size:"),
                    # sg.Input(size=(3, 1), default_text="13", key="-ThumbSizeNum-"),
                    sg.Spin(
                        thumbsize_percentages,
                        initial_value="13",
                        size=(4, 4),
                        key="-ThumbSize-",
                    ),
                    sg.Text("(% of browser window width)"),
                    # sg.Radio(
                    #     "% window width",
                    #     default=True,
                    #     group_id="-ThumbSizeUnits-",
                    #     key="-PercentWidth-",
                    # ),
                    # sg.Radio("# pixels", group_id="-ThumbSizeUnits-", key="-Pixels-",),
                ],
                [
                    sg.Text(24 * " "),
                    sg.Checkbox(
                        " Hide empty links (images only)",
                        default=True,
                        key="-HideBorkedImages-",
                    ),
                ],
                # [sg.Text("")],
                [
                    sg.Text((9 * " ") + "Choose browser: "),
                    sg.Combo(
                        supported_browsers,
                        default_value="system_default",
                        # default_values="system_default",
                        # select_mode="LISTBOX_SELECT_MODE_SINGLE",
                        size=(20, 1),
                        pad=(1, 1),
                        readonly=True,
                        key="-SelectedBrowser-",
                    ),
                ],
                [sg.Text("")],
                [sg.Button("Rustle Up Some Links", key="-DoIt-"), sg.Button("Quit"),],
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
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == "Quit":
        break
    elif event == "-DoIt-":
        # thumbsize = values["-ThumbSize-"] + "%"
        # if values["-PercentWidth-"]:
        #     thumbsize += "%"
        # else:
        #     thumbsize += "px"
        do_it(
            values["-URLMask-"],
            targetfile="rustled.html",
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
