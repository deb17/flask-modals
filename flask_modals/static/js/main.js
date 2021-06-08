// The .modal-backdrop div appears mutliple times when the form is 
// submitted via ajax and the response is a redirect to the same page.
// This happens in Bootstrap 4. We need to keep only one occurrence.
function removeBackdrop() {
  const els = document.querySelectorAll('.modal-backdrop')
  for (let i=0; i < els.length - 1; i++) {
    els[i].remove()
  }
}

document.documentElement.addEventListener('turbo:render', () => {
  if (window.jQuery) {
    $('.modal').unbind('shown.bs.modal')
    $('.modal').on('shown.bs.modal', removeBackdrop)
  }
})

document.documentElement.addEventListener('turbo:submit-start', () => {
  NProgress.start()
})

document.documentElement.addEventListener('turbo:submit-end', () => {
  NProgress.done()
})

document.documentElement.addEventListener('turbo:before-stream-render', (e) => {
  if (e.target.attributes.action.value === 'update') {
    const body = document.querySelector('body')
    body.classList.remove('modal-open')
    body.style.paddingRight = '0px'
  }
})

document.documentElement.addEventListener('turbo:load', () => {
  document.body.dataset.turbo = false
})
