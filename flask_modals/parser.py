from html.parser import HTMLParser
import re


class ModalParser(HTMLParser):
    def __init__(self, html, modal):
        super().__init__()
        self.id_num = 0
        self.div_count = 0
        self.found_body = False
        self.found_modal = False
        self.html = html
        self.modal = modal
        self.stream = ''
        self.target = ''
        self.insert_id()

    def insert_id(self):

        def repl(matchobj):

            self.id_num += 1
            return f'class="modal-body" id="turbo-stream__{self.id_num}"'

        self.html = re.sub(r'class\s*=\s*"modal-body"', repl, self.html)

    def handle_starttag(self, tag, attrs):

        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'id' and attr[1] == self.modal:
                    self.found_modal = True
            if self.found_body:
                self.div_count += 1
            else:
                for attr in attrs:
                    if attr[0] == 'class' and attr[1] == 'modal-body':
                        if self.found_modal:
                            self.found_body = True
                            self.div_count += 1
                            self.stream_start = self.getpos()
                            for a in attrs:
                                if a[0] == 'id':
                                    self.target = a[1]

    def handle_endtag(self, tag):

        if self.found_body:
            if tag == 'div':
                self.div_count -= 1
                if self.div_count == 0:
                    self.stream_end = self.getpos()
                    self.get_stream()
                    self.found_body = False
                    self.found_modal = False

    def get_stream(self):

        lines = self.html.splitlines(keepends=True)
        start_line_no = self.stream_start[0] - 1
        start_line = lines[start_line_no]
        start_pos = self.stream_start[1]
        end_line_no = self.stream_end[0] - 1
        end_line = lines[end_line_no]
        end_pos = self.stream_end[1] + 6    # </div>
        self.stream += start_line[start_pos:]
        for line in lines[start_line_no + 1:end_line_no]:
            self.stream += line
        self.stream += end_line[:end_pos]


def add_turbo_stream_ids(html, modal):

    parser = ModalParser(html, modal)
    parser.feed(parser.html)
    return parser.html, parser.stream, parser.target
