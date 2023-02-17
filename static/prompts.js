// JS File for updating prompts

// Sets an event listener on the new prompt button that requests
// random prompt text from the database.

const promptHole = document.querySelector('#prompt-hole strong')

const randomPrompt = document.querySelector('#prompt-btn').addEventListener('click', () => {
    fetch('/prompt-hole.json')
      .then((response) => response.text())
      .then((responseData) => {
          promptHole.innerHTML = responseData
      })
  });


const randomPromptOnLoad = window.addEventListener('load', () => {
    fetch('/prompt-hole.json')
      .then((response) => response.text())
      .then((responseData) => {
          promptHole.innerHTML = responseData
      })
  });



// Sets an event listener on the save prompt/response button that captures all the relevant
// text on the page and sends it via AJAX to the server to be saved to the 
// database.

const savePrompt = document.querySelector('#save-prompt').addEventListener('click', () => {
    const promptText = document.querySelector('#prompt-hole').innerText
    const userResponse = document.querySelector('#prompt-response').value
    
    // console.log(promptText)
    // console.log(userResponse)

    const dataPacket = {
        'prompt_text': promptText,
        'user_response': userResponse
    }

    fetch('/save-prompt.json', {
        method: 'POST',
        body: JSON.stringify(dataPacket),
        headers: {
            'Content-Type': 'application/json',
        }
      })
      .then((response) => response.text())
      .then((responseData) => {
        // console.log(responseData)
        if (responseData == 'fine') {
            alert('Prompt and response saved!');
        }
        else if (responseData == 'update') {
             alert('Response updated and saved! (FUNCTIONALITY NOT YET BUILT)');
        }
        else if (responseData === 'not logged in') {
            alert('Only users who are logged in can save prompts and responses!');
        }
        else if (responseData === "error") {
            alert('Error, please try again.')
        }
    })
}); 