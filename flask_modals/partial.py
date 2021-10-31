import re

from flask import render_template


def get_partial(modal, *args, **kwargs):
    '''Return the modal body.'''

    html = render_template(*args, **kwargs)
    lines = html.splitlines(keepends=True)

    found_modal = False
    found_modal_body = False
    div_count = 0
    partial = ''
    for line in lines:
        if f'id="{modal}"' in line:
            found_modal = True
        if found_modal:
            if 'class="modal-body' in line:
                found_modal_body = True
            if found_modal_body:
                partial += line
                startdivs = re.findall(r'<div.*?>', line, re.IGNORECASE)
                enddivs = re.findall(r'</div>', line, re.IGNORECASE)
                div_count += len(startdivs) - len(enddivs)
                if div_count <= 0:
                    break
    return partial
