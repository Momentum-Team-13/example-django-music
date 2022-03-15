const searchSelect = document.querySelector('#search-type-select')

searchSelect.addEventListener('input', (e) => {
  const searchType = e.target.value
  document.querySelector('#search-input').name = searchType
})
