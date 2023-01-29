//Javascript file to control updating data on poems.html via API updates


// set variables to corresponding HTML elements by ID, 
// in order to later update the innerHTML with API data

const poemTitle = document.querySelector('#poem-title')
const poemAuthor = document.querySelector('#poem-author')
const poemText = document.querySelector('#poem-text')


// using an event listener set on a button click, AJAX request to server.py
// to call the API, receive a JSON file containing poem data from a random poem,
// unpack that data, and fill in the HTML elements with the corresponding data 
// (title, author, poetry text in the form of individual lines)

const randomPoem = document.querySelector('#random-poem').addEventListener('click', () => {
  fetch('/random-poem')
    .then((response) => response.json())
    .then((responseData) => {
        poemTitle.innerHTML = `<h1>${responseData.data[0].title}</h1>`;
        poemAuthor.innerHTML = `<h3>by ${responseData.data[0].author}</h3>`;
        poemText.innerHTML = '';
        for (line in responseData.data[0].lines) {
            poemText.insertAdjacentHTML('beforeend', `<div>${responseData.data[0].lines[line]}</div>`)
        }
    })
});



// Sets an event listener on the bookmark button that captures all the relevant
// text on the page and sends it via AJAX to the server to be saved to the 
// database.


const bookmarkPoem = document.querySelector('#bookmark-poem').addEventListener('click', () => {
  const poemTitleFromDoc = document.querySelector('#poem-title').innerText;
  const poemAuthorFromDoc = document.querySelector('#poem-author').innerText;
  const poemTextFromDoc = document.querySelector('#poem-text').innerText;
  const comments = document.querySelector('#comments').value; 

  const dataPacket = {
    'title': poemTitleFromDoc,
    'author': poemAuthorFromDoc,
    'lines': poemTextFromDoc,
    'comments': comments
  }

  console.log(dataPacket)

  fetch('/bookmark', {
    method: 'POST',
    body: JSON.stringify(dataPacket),
    headers: {
        'Content-Type': 'application/json',
    }
  })
    .then((response) => response.text())
    .then((responseBookmark) => {
        if (responseBookmark === 'ok') {
            alert('Poem bookmarked and comment saved!')
        }
        if (responseBookmark === 'not ok') {
            alert('Only users who are logged in can save poems and comments!')
        }
        else {
            alert('Error, please try again.')
        }
    })
})
