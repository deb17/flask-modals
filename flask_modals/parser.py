from html.parser import HTMLParser


class ModalParser(HTMLParser):
    '''Parse the output of `render_template` to get the modal body.'''

    def __init__(self, html, modal):
        '''Initialize the parser.

        Parameters:
        html - The html document string
        modal - The id of the modal
        '''

        super().__init__()
        self.html = html
        self.modal = modal
        self.stream = ''
        self.found_modal = False
        self.found_body = False
        self.div_count = 0

    def handle_starttag(self, tag, attrs):

        if tag == 'div':
            if self.found_modal:
                if self.found_body:
                    self.div_count += 1
                else:
                    for attr in attrs:
                        if attr[0] == 'class' and 'modal-body' in attr[1]:
                            self.found_body = True
                            self.div_count += 1
                            self.stream_start = self.getpos()
            else:
                for attr in attrs:
                    if attr[0] == 'id' and attr[1] == self.modal:
                        self.found_modal = True

    def handle_endtag(self, tag):

        if tag == 'div':
            if self.found_body:
                self.div_count -= 1
                if self.div_count == 0:
                    self.stream_end = self.getpos()
                    self.get_stream()
                    self.found_modal = False
                    self.found_body = False

    def get_stream(self):
        '''Get the modal body element.'''

        lines = self.html.splitlines(keepends=True)
        start_line_no = self.stream_start[0] - 1
        start_line = lines[start_line_no]
        start_pos = self.stream_start[1]
        end_line_no = self.stream_end[0] - 1
        end_line = lines[end_line_no]
        end_pos = self.stream_end[1] + 6  # len('</div>') = 6
        self.stream += start_line[start_pos:]
        for line in lines[start_line_no + 1:end_line_no]:
            self.stream += line
        self.stream += end_line[:end_pos]
