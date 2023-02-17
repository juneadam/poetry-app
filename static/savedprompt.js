// JS file to allow for saving updates to user comments.

const updateComments = document.querySelector('#save-changes').addEventListener('click', () => {
    const updated_response = document.querySelector('#saved-prompt-response').value;
    console.log(updated_response)
    prompt_text = document.querySelector('#saved-prompt-hole').innerText
  
    dataPacket = {
      'updated_response' : updated_response,
      'prompt_text' : prompt_text,
    }

    // console.log(dataPacket)
  
    fetch('/update-response', {
      method: 'POST',
      body: JSON.stringify(dataPacket),
      headers: {
          'Content-Type': 'application/json',
      }
    })
      .then((response) => response.text())
      .then((responseUpdateResponse) => {
          if (responseUpdateResponse == 'ok') {
            alert("Your comment was updated!")
          }
          if (responseUpdateResponse == 'error') {
            alert("There was a problem saving your comment.")
          }
      })
  });