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
        mashupText.innerHTML = ''
        for (poem of mashupDataJson['data']) {
            mashupText.insertAdjacentHTML('beforeend', 
            `<div id="${poem[2]}">
            <div hidden class="hidden">${poem[0]}@${poem[1]}@${poem[2]}></div>
            ${poem[2]}
            </div>`
            )
        }

    })

})

