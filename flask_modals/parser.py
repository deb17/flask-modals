'''I decided to switch to beautiful soup in version 0.2.7 from the
built-in parser as it takes a lot less code to accomplish the same.
Finding nested tags is easy.
'''

from bs4 import BeautifulSoup


def parse_html(html, modal, redirect, update, show_modal):
    '''Parse the rendered template.

    Add ids to the modal bodies. If modal body contains a form, set
    `data-turbo="true"` attribute on the form.

    If rendering a template by setting the `redirect` argument to
    `False`, set an id on the body element for the update operation.
    Turbo requires a redirect on form submission, so we cannot normally
    render a template (unless streaming). To overcome this and refresh
    the page, we stream an update operation on the body element.

    If streaming, return the html fragment (either the modal body or the
    body element itself).
    '''
    soup = BeautifulSoup(html, 'html.parser')

    modal_bodies = soup.find_all('div', class_='modal-body')

    for index, body in enumerate(modal_bodies, 1):
        body['id'] = f'turbo-stream__{index}'
        form = body.find('form')
        if form:
            form['data-turbo'] = 'true'

    if not redirect:
        soup.body['id'] = 'turbo-stream__body'

    stream = ''
    target = ''
    output = ''

    if update or show_modal:
        if update:
            stream = soup.body.decode(formatter='html')
            target = soup.body['id']
        else:
            target_modal = soup.find('div', id=modal)
            modal_body = target_modal.find('div', class_='modal-body')
            stream = modal_body.decode(formatter='html')
            target = modal_body['id']
    else:
        # Turbo merges the changes to the head. If asset html is not
        # identical, it gets repeated. So instead of decoding the
        # entire document, we decode the body and add the head part
        # from the html string.
        body = soup.body.decode(formatter='html')
        pos = html.index('</head>') + 7
        head = html[:pos]
        output = head + body

    return output, stream, target
