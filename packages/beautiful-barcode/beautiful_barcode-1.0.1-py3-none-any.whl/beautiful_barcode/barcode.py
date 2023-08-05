from . import renderers


class Barcode:
    def to_modules(self) -> str:
        """ Convert the Barcode to modules (1 or 0) """
        raise NotImplementedError

    def render(self, renderer='auto') -> bytes:
        """ Renders the barcode as a bytes object """

        rend = renderers.make_renderer(renderer)
        self._paint(rend)
        return rend.to_bytes()

    def write(self, filename, renderer='auto'):
        data = self.render(renderer=renderer)
        with open(filename, 'wb') as out_file:
            out_file.write(data)
