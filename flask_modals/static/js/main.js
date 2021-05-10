// The .modal-backdrop div appears mutliple times when the form is 
// submitted via ajax. We need to keep only one occurrence.
document.documentElement.addEventListener('turbo:render', () => {
  $('.modal').unbind('shown.bs.modal')
  $('.modal').on('shown.bs.modal', function() {
    const els = document.querySelectorAll('.modal-backdrop')
    for (let i=0; i < els.length - 1; i++) {
      els[i].remove()
    }
  })
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
