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
    if (submitter) {
      const name = submitter.getAttribute('name')
      const value = submitter.getAttribute('value')
      body.append(name, value)
    }
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
        if (data.startsWith('<template>')) {
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
          if (location.href !== url) {
            history.replaceState({ modal: true }, '')
            history.pushState(null, '', url)
          }
          const doc = new DOMParser().parseFromString(data, "text/html")
          document.documentElement.replaceWith(doc.documentElement)
          activateScripts()
          removeExtraBackdrops()
        }
      })
      .catch(err => {
        NProgress.done()
        console.log(err)
      })
  }

  // Need to activate inert scripts in new document.
  function activateScripts() {
    const scriptEls = document.querySelectorAll('script')

    scriptEls.forEach(el => {
      const newScriptEl = document.createElement('script')
      newScriptEl.textContent = el.textContent
      newScriptEl.async = false
      for (const { name, value } of [...el.attributes]) {
        newScriptEl.setAttribute(name, value)
      }
      el.replaceWith(newScriptEl)
    })

  }

  // The .modal-backdrop div gets repeated on ajax load of the same
  // modal page.
  function removeExtraBackdrops() {
    if (window.jQuery) {
      // remove possible duplicate
      $('.modal').unbind('shown.bs.modal')
      $('.modal').on('shown.bs.modal', removeBackdrop)
    } else {
      const modals = document.querySelectorAll('.modal')
      modals.forEach(m => {
        // remove possible duplicate
        m.removeEventListener('shown.bs.modal', removeBackdrop)
        m.addEventListener('shown.bs.modal', removeBackdrop)
      })
    }
  }

  function removeBackdrop() {
    const els = document.querySelectorAll('.modal-backdrop')
    for (let i = 0; i < els.length - 1; i++) {
      els[i].remove()
    }
  }

  window.onpopstate = function (e) {
    if (typeof e.state === 'object' && e.state !== null && 'modal' in e.state) {
      location.reload()
    }
  }
})()
