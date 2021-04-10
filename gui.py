import PySimpleGUI as sg

# Define the window's contents
window_title = "Sequential Links Rustler"

left_buttons = [[sg.Button("1")], [sg.Button("2")], [sg.Button("3")]]
# left_layout = sg.Column(left_buttons)

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
        # ],
        # [
        sg.Column(
            [
                [sg.Text("Enter/paste original URL:"), sg.Input(key="-Resource-")],
                [sg.Text("Edit URL mask:"), sg.Input(key="-ResourceMask-")],
                [sg.Text("Enter/paste original URL:"), sg.Input(key="-Thumbnail-")],
                [sg.Text("Edit URL mask:"), sg.Input(key="-ThumbnailMask-")],
            ]
        ),
    ],
    # [
    #     sg.Column(
    #         [
    #             [sg.Frame("Resource", resource_frame)],
    #             [sg.Frame("Thumbnail", thumbnail_frame)],
    #         ]
    #     ),
    # ],
    # [sg.Text("Paste URL for resource here")],
    # [sg.Input(key="-Resource-")],
    # [sg.Text("Edit URL mask for resource here:")],
    # [sg.Input(key="-ResourceMask-")],
    # [sg.Text("Paste original URL for thumbnail here")],
    # [sg.Input(key="-Thumbnail-")],
    # [sg.Text("Edit URL mask for thumbnail here:")],
    # [sg.Input(key="-ThumbnailMask-")],
    # [sg.Text(size=(40, 1), key="-OUTPUT-")],
    [sg.Button("Generate, Save, and Open File"), sg.Button("Quit")],
]

# Create the window
window = sg.Window(window_title, layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == "Quit":
        break
    else:
        print(event, values)
    # # Output a message to the window
    # window["-OUTPUT-"].update(
    #     "Hello " + values["-INPUT-"] + "! Thanks for trying PySimpleGUI"
    # )

# Finish up by removing from the screen
window.close()
