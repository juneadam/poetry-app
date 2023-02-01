// JS file to allow for saving updates to user comments.

const updateComments = document.querySelector('#update-comments').addEventListener('click', () => {
  const new_text = document.querySelector('#updating-comments').value;
//   console.log(new_text)
  title = document.querySelector('#saved-poem-title').innerText
  author = document.querySelector('#saved-poem-author').innerText

  dataPacket = {
    'updated_text' : new_text,
    'title' : title,
    'author' : author,
  }

  fetch('/update-comments', {
    method: 'POST',
    body: JSON.stringify(dataPacket),
    headers: {
        'Content-Type': 'application/json',
    }
  })
    .then((response) => response.text())
    .then((responseUpdateComments) => {
        if (responseUpdateComments == 'ok') {
            alert("Your comment was updated!")
        }
    })
});