import subprocess
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import ItemEnterEvent


class ItemEnterEventListener(EventListener):

    def on_event(self, event: ItemEnterEvent, extension: Extension):
        """ Handles the click on an item of the extension """
        data = event.get_data()

        code_executable = extension.preferences['code_executable_path']
        subprocess.run([code_executable, '--folder-uri', data['path']])
