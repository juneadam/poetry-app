//Javascript file to control updating data on poems.html via API updates

const poemTitle = document.querySelector('#poem-title')

const poemAuthor = document.querySelector('#poem-author')

const poemText = document.querySelector('#poem-text')


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

