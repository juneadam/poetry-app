// JS file to handle mashing up poems from Poetry DB

const mashupTitle = document.querySelector('#mashup-title')
const mashupAuthor = document.querySelector('#mashup-author')
const mashupText = document.querySelector('#mashup-text')
const lineCountEntry = document.querySelector('#linecount-input-mashup')


const mashupButton = document.querySelector('#mashup-poem').addEventListener('click', () => {
    linecount = lineCountEntry.value;

    dataPacket = {
        'linecount' : linecount
    };

    fetch('/mashup-generator', {
        method: 'POST',
        body: JSON.stringify(dataPacket),
        headers: {
            'Content-Type': 'application/json',
        }
      })
    .then((response) => response.json())
    .then((mashupDataJson) => {
        mashupTitle.innerHTML = `<h1>${mashupDataJson['title']}`

        mashupAuthor.innerHTML = `<h2>by ${mashupDataJson['username']} and <a href='https://www.poetrydb.org'>PoetryDB</a></h2>`;

        mashupText.innerHTML = ''
        for (poem of mashupDataJson['data']) {
            mashupText.insertAdjacentHTML('beforeend', 
            `<div id="${poem[2]}">
            <div hidden class="hidden">${poem[0]}@${poem[1]}@${poem[2]}</div>
            ${poem[2]}
            </div>`
            )
        }
    })
})


const saveMashupButton = document.querySelector('#save-mashup').addEventListener('click', () => {
    const hiddenData = document.querySelectorAll('#mashup-text .hidden')

    const dataList = []
    for (const hiddenDiv of hiddenData) {
        dataList.push(hiddenDiv.innerText)
    };
    const title = mashupTitle.innerText;
    const author = mashupAuthor.innerText;

    dataPacket = {
        'dataList' : dataList,
        'title' : title,
        'author' : author
    };

    fetch('/save-mashup', {
        method: 'POST',
        body: JSON.stringify(dataPacket),
        headers: {
            'Content-Type': 'application/json',
        }
      })
    .then((response) => response.text())
    .then((mashupDataJson) => {
        if (mashupDataJson === 'ok') {
            alert('fine.')
        }
    }   
  )
})