// when a logged-in user clicks on the heart icon, it should add or delete a favorite for this user
// if the album is already favorited, then we want to remove it as a favorite
//      that means we want to send a DELETE request
//.if it is NOT already favorited, then we want to add it as a favorite
//      that means we want to send a POST

// I need to know when a user clicks on the heart icon
const heartIcon = document.getElementById('fav-link')

heartIcon.addEventListener('click', (e) => {
  // disable default behavior -- i.e., don't follow the link
  e.preventDefault()
  // we need to know whether we want to send a POST or a DELETE
  // I stored that information as a data attribute on the link element
  // "data-favorited" holds a STRING that is either true or false
  const request_method =
    heartIcon.dataset.favorited == 'true' ? 'DELETE' : 'POST'
  // Django requires me to send the CSRF token with this request, so I need to get it from cookies
  // https://docs.djangoproject.com/en/4.0/ref/csrf/#ajax
  // I'll use a JS library to make this easier (it's included in the js block on the template)
  const csrfToken = Cookies.get('csrftoken')
  // Now I'm ready to make an ajax request to add or remove this favorite.
  fetch(heartIcon.href, {
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrfToken,
    },
    mode: 'same-origin',
    method: request_method,
  })
    .then((res) => res.json())
    .then((data) => {
      // now I can update the page to reflect that the album was favorited or unfavorited
      console.log(data) // This is my JSON data I'm sending back from my view function!
      if (data.favorited) {
        // replace the heart icon to solid to indicate that it IS favorited
        // all I have to do is swap classes from Font Awesome
        e.target.classList.replace('far', 'fas')
        // update state in the DOM to show that it is favorited
        heartIcon.dataset.favorited = 'true'
      } else {
        // replace the heart icon class to outline to indicate that it's NOT favorited
        e.target.classList.replace('fas', 'far')
        // update state in the DOM to show that it is not favorited
        heartIcon.dataset.favorited = 'false'
      }
    })
})
