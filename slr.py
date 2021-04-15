import multiprocessing, random

import PySimpleGUI as sg

from main import rustle_up_some_links as do_it


# Define the window's contents
window_title = "Sequential Links Rustler"

logo_image = sg.Image(
    filename="logo.png",
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
                    sg.Input(key="-URLMask-", size=(65, 1)),
                    sg.Button("Clear", key="-Clear URL mask-"),
                ],
                # [sg.Text("Enter/paste original URL:"), sg.Input(key="-Thumbnail-")],
                # [sg.Text("Edit URL mask:"), sg.Input(key="-ThumbnailMask-")],
                [sg.Text("")],
                [sg.Text("")],
                [sg.Text("")],
                [sg.Text("")],
                [sg.Text("")],
                [sg.Button("Rustle Up Some Links", key="-DoIt-"), sg.Button("Quit"),],
            ]
        ),
    ],
    # [sg.Button("Generate, Save, and Open File"), sg.Button("Quit")],
]

# Create the window
window = sg.Window(window_title, layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == "Quit":
        break
    elif event == "-DoIt-":
        proc_id = "slr_" + str(int(random.random() * 1000000000000))
        d = multiprocessing.Process(
            name=proc_id, target=do_it(values["-URLMask-"], targetfile="rustled.html"),
        )
        d.daemon = True
        d.start()
        # do_it(values["-URLMask-"], targetfile="rustled.html")
    elif event == "-Clear URL mask-":
        window["-URLMask-"].update("")
    else:
        print(event, values)

# Finish up by removing from the screen
window.close()
