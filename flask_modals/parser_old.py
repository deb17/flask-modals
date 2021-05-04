from html.parser import HTMLParser


class ModalParser(HTMLParser):
    def __init__(self, html, modal):
        super().__init__()
        self.id_num = 1
        self.div_count = 0
        self.found = False
        self.found_modal = False
        self.html = html
        self.modal = modal
        self.stream = ''
        self.target = ''

    def handle_starttag(self, tag, attrs):

        if self.modal:
            if tag == 'div':
                for attr in attrs:
                    if attr[0] == 'id' and attr[1] == self.modal:
                        self.found_modal = True
        if tag == 'div':
            if self.found:
                self.div_count += 1
            else:
                for attr in attrs:
                    if attr[0] == 'class' and attr[1] == 'modal-body':
                        self.found = True
                        self.div_count += 1
                        tag_to_insert = (
                            '<turbo-stream action="replace"'
                            f' target="turbo-stream__{self.id_num}">'
                            '<template>'
                        )
                        id_to_insert = f"turbo-stream__{self.id_num}"
                        self.html = self.insert_id_and_tag(
                            id_to_insert,
                            tag_to_insert
                        )
                        self.id_num += 1

    def handle_endtag(self, tag):

        if self.found:
            if tag == 'div':
                self.div_count -= 1
                if self.div_count == 0:
                    adjust = len(tag) + 3
                    tag_to_insert = '</template></turbo-stream>'
                    self.html = self.insert_id_and_tag(
                        None,
                        tag_to_insert,
                        adjust
                    )
                    self.found = False

    def insert_id_and_tag(self, id, tag, adjust=0):

        lineno, pos = self.getpos()
        lines = self.html.splitlines(keepends=True)
        line = lines[lineno - 1]
        if id:
            line = self.insert_id(line, id)
            if self.found_modal:
                self.target = id
                self.stream_start = (lineno, pos)
        elif self.found_modal:
            self.found_modal = False
            self.stream_end = (lineno, pos)
            self.get_stream(lines)

        # line = self.insert_tag(line, pos, tag, adjust)
        lines[lineno - 1] = line
        return ''.join(lines)

    def get_stream(self, lines):

        start_line_no = self.stream_start[0] - 1
        start_line = lines[start_line_no]
        start_pos = start_line.index('<div')
        end_line_no = self.stream_end[0] - 1
        self.stream += start_line[start_pos:]
        for line in lines[start_line_no + 1:end_line_no + 1]:
            self.stream += line

    def insert_id(self, line, id):

        line = line.replace(
            'class="modal-body"',
            f'class="modal-body" id="{id}"'
        )
        return line

    def insert_tag(self, line, pos, tag, adjust):

        pos += adjust
        line = line[:pos] + tag + line[pos:]
        return line


def add_turbo_stream_tags(html, modal):

    parser = ModalParser(html, modal)
    parser.feed(html)
    return parser.html, parser.stream, parser.target
