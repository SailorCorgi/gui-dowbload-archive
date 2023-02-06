import PySimpleGUI as sg
import requests
import os
import concurrent.futures
import io

CHUNK_SIZE = 7 * 1024 * 1024  # 7 MB vs 1 MB
# I saw that 3-10 mb is best for big download or performance focused downloads so 7 is a good middle ground.
# also tested and seven was better than 1mb so ya
THREAD_POOL = concurrent.futures.ThreadPoolExecutor()

sg.theme('Dark Grey 13')  # black blue color scheme

# All the stuff inside the window.
layout = [[sg.Text('Archive downloader')],
          [sg.Text('For multiple urls please separate them with a comma followed by a space(https://example.org, '
                   'https://example.org)')],
          [sg.Text('Enter links'), sg.InputText()],
          [sg.Text('Enter folder name'), sg.InputText()],
          [sg.Button('Select Folder'), sg.InputText()],
          [sg.Button('Download'), sg.Button('Check'), sg.Button('Close')]]

# Create the Window
window = sg.Window('BULK Archive downloader', layout)


def download_file(link, folder_name, chunk_size):
    try:
        r = requests.get(link, stream=True)
        if r.status_code == requests.codes.ok:
            r.raw.decode_content = True  # Handling compression
            file = io.BytesIO()
            for chunk in r.iter_content(chunk_size):
                file.write(chunk)
            with open(os.path.join(folder_name, link.split("/")[-1]), 'wb') as f:
                f.write(file.getvalue())
    except requests.exceptions.RequestException as e:
        sg.popup("Error downloading the file " + link + ": " + str(e))


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == 'Select Folder':
        folder_path = sg.popup_get_folder('Select folder to save the downloaded files')
        if folder_path:
            window['Select Folder'].update(folder_path)
    if event == 'Download':
        sg.popup_auto_close('   -Please wait this may take a while-   ',
                            auto_close_duration=3)
        links = values[0].split(", ")
        folder_name = values[1]
        folder_path = values[2]
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # submit all the download tasks to the thread pool

        download_tasks = [THREAD_POOL.submit(download_file, link, folder_path, CHUNK_SIZE) for link in links]
        # wait for all the download tasks to complete
        concurrent.futures.wait(download_tasks)
          sg.popup('Downloads complete')
    if event == sg.WIN_CLOSED or event == 'Close':  # if the user closes window or clicks close
        break
    if event == 'Check': a
        sortedlink = values[0].split(', ')
        sg.popup('Theres the links you have inputted:' + sortedlink)


window.close()
