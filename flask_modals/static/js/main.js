(function () {
  const formEls = document.querySelectorAll('form')

  formEls.forEach(el => {
    const modalBodyEl = el.closest('.modal-body')
    if (modalBodyEl) {
      el.addEventListener('submit', e => {
        e.preventDefault()
        fetchData(el, modalBodyEl, e.submitter)
      })
    }
  })

  function fetchData(el, modalBodyEl, submitter) {
    let url
    const body = new FormData(el)
    let submitterName, submitterValue
    if (submitter) {
      submitterName = submitter.getAttribute('name') || 'form-submit'
      if (submitterName === 'submit') submitterName = 'form-submit'
      submitterValue = submitter.getAttribute('value') || submitter.textContent
      body.append(submitterName, submitterValue)
    }
    body.append('_ajax', true)
    NProgress.start()
    fetch(el.action, {
      method: el.method,
      body: body,
      headers: {
        Accept: 'text/modal-stream.html'
      }
    })
      .then(res => {
        if (res.ok) {
          NProgress.done()
          url = res.url
          return res.text()
        } else {
          throw new Error(`Error fetching data. Status ${res.status}`)
        }
      })
      .then(data => {
        if (data) {
          const doc = new DOMParser().parseFromString(data, "text/html")
          const templateEl = doc.querySelector('template')
          const newModalBodyEl = doc.importNode(templateEl.content, true)
            .firstElementChild
          modalBodyEl.innerHTML = newModalBodyEl.innerHTML
          const el = modalBodyEl.querySelector('form')
          el.addEventListener('submit', e => {
            e.preventDefault()
            fetchData(el, modalBodyEl, e.submitter)
          })
        } else {
          const btn = el.querySelector('#submit, [name="submit"]')
          if (btn) {
            btn.removeAttribute('id')
            btn.removeAttribute('name')
          }
          if (submitter) {
            const inp = document.createElement('input')
            inp.type = 'hidden'
            inp.name = submitterName
            inp.value = submitterValue
            el.appendChild(inp)
          }
          el.submit()
        }
      })
      .catch(err => {
        NProgress.done()
        console.log(err)
      })
  }
})()
