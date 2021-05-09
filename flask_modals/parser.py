from html.parser import HTMLParser
import re


class ModalParser(HTMLParser):
    '''The parser gives the modal body an id and filters it out as the
    turbo stream element. I could have used `beautifulsoup` to do the
    parsing but chose not to in order to keep the extension lightweight.
    (All it does is support modals.)
    '''

    def __init__(self, html, modal, redirect, show_modal):
        '''Initialize the parser and call method to insert ids for
        modal bodies.

        id_num: A unique integer for each modal body.
        div_count: Keep track of all divs in the modal body.
        found_modal: Flag to indicate the modal with id passed to
                     render_template_modal function was found.
        found_body: Flag to indicate that the body of the specific
                    modal was found.
        html: The render_template output string. Will be modified with
              id attributes.
        modal: The id of the modal
        redirect: If rendering a template instead of redirecting, this will
                  be False.
        body: If True, parse the body out of the html string if redirect is
              False.
        stream: The modal body element with the id set.
        target: The id of the stream element.
        '''

        super().__init__()
        self.id_num = 0
        self.div_count = 0
        self.found_modal = False
        self.found_body = False
        self.html = html
        self.modal = modal
        self.redirect = redirect
        self.body = not show_modal
        self.stream = ''
        self.target = ''
        self.insert_id()

    def insert_id(self):

        def repl(matchobj):

            self.id_num += 1
            return f'class="modal-body" id="turbo-stream__{self.id_num}"'

        self.html = re.sub(r'class\s*=\s*"modal-body"', repl, self.html)

        if not self.redirect:
            self.html = self.html.replace('<body',
                                          '<body id="turbo-stream__body"')

    def handle_starttag(self, tag, attrs):

        if self.body and not self.redirect:
            if tag == 'body':
                self.stream_start = self.getpos()
            return

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

        if self.body and not self.redirect:
            if tag == 'body':
                self.stream_end = self.getpos()
                self.get_stream(endtaglen=len('</body>'))
            return

        if self.found_body:
            if tag == 'div':
                self.div_count -= 1
                if self.div_count == 0:
                    self.stream_end = self.getpos()
                    self.get_stream()
                    self.found_body = False
                    self.found_modal = False

    def get_stream(self, endtaglen=6):
        '''Get the modal body element.'''

        lines = self.html.splitlines(keepends=True)
        start_line_no = self.stream_start[0] - 1
        start_line = lines[start_line_no]
        start_pos = self.stream_start[1]
        end_line_no = self.stream_end[0] - 1
        end_line = lines[end_line_no]
        end_pos = self.stream_end[1] + endtaglen    # </div> or </body>
        self.stream += start_line[start_pos:]
        for line in lines[start_line_no + 1:end_line_no]:
            self.stream += line
        self.stream += end_line[:end_pos]


def add_turbo_stream_ids(html, modal, redirect, show_modal):
    '''Add turbo stream ids and parse the resulting html string.'''

    parser = ModalParser(html, modal, redirect, show_modal)
    parser.feed(parser.html)
    return parser.html, parser.stream, parser.target
