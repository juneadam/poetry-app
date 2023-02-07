// JS File to control button functionality on add-prompt template.

const userPrompt = document.querySelector('#user-prompt-add')

const saveButton = document.querySelector('#save-prompt-btn').addEventListener('click', () => {
    const newPrompt = userPrompt.value;

    const dataPacket = {
        'new_prompt': newPrompt
    }

    fetch ('/save-prompt-to-db.json', {
        method: 'POST',
        body: JSON.stringify(dataPacket),
        headers: {
            'Content-Type': 'application/json',
        }
      })
    .then((response) => response.text())
    .then((responseJSON) => {
        if (responseJSON == 'not logged in') {
            alert('Only users who are logged in can add prompts to the database.')
        }
        else if (responseJSON == 'not ok') {
            alert('Please enter a prompt below.')
        }
        else if (responseJSON == 'ok') {
            alert('New prompt saved to the database!')
        }

    })
})