document.documentElement.addEventListener('turbo:render', () => {
  $('.modal').unbind('shown.bs.modal')
  $('.modal').on('shown.bs.modal', function() {
    const els = document.querySelectorAll('.modal-backdrop')
    console.log(els)
    for (let i=0; i < els.length - 1; i++) {
      els[i].remove()
    }
  })
})
