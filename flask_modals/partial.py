from lxml import etree, html
from flask import render_template


def get_partial(modal_id, *args, **kwargs):
    '''Return the modal body.'''

    doc = render_template(*args, **kwargs)
    root_node = html.fromstring(doc)
    xpath = f'//div[@id="{modal_id}"]'      # modal window
    modal_node = root_node.xpath(xpath)[0]
    xpath = './/div[@class="modal-body"]'    # modal body
    body_node = modal_node.xpath(xpath)[0]
    body = str(etree.tostring(body_node)).replace('\\n', '').replace('\n', '')
    return body
