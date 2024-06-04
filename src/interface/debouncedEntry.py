import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GLib


class DebouncedEntry(Gtk.Entry):
    __gsignals__ = {"debounced": (GObject.SignalFlags.RUN_LAST, None, ())}

    def __init__(
        self, text=None, on_changed_callback=None, timeout=500, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.on_changed_callback = on_changed_callback
        self.timeout_id = None
        self.timeout = timeout
        if text:
            self.set_text(text)
        self.connect("changed", self.on_changed)

    def set_timeout(self, timeout):
        self.timeout = timeout

    def set_on_changed_callback(self, on_changed_callback):
        self.on_changed_callback = on_changed_callback

    def on_changed(self, entry):
        if self.on_changed_callback:
            self.on_changed_callback(entry)

        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
        self.timeout_id = GLib.timeout_add(self.timeout, self.emit_debounced)

    def emit_debounced(self):
        self.emit("debounced")
        self.timeout_id = None
        return False


def on_debounced(entry):
    print("Debounced Entry:", entry.get_text())


def main():
    win = Gtk.Window()
    win.connect("destroy", Gtk.main_quit)

    entry = DebouncedEntry()
    entry.connect("debounced", on_debounced)
    win.add(entry)

    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
