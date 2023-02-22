// React file to generate HTML for user profile

  // ============ Username Container ============ //

const UsernameCard = (props) => {
    const [username, setUsername] = React.useState('');

    const fetchUsername = () => {
        fetch('/username.json')
        .then((response) => response.text())
        .then((username_text) => {
            setUsername(username_text);
        })
    };

    React.useEffect(fetchUsername, [])

    return (
        <div>
            <div className="row">
                <section id="user-header">
                    <h1>{username}</h1>
                </section>
            </div>
        </div>
            );
  }

  

  // ============ Poem Container ============ //


  // creating a PoemCard React object, which will be a
  // child component of the UserSavedPoems React Object
  // and will take in the parent's state value of an array
  // of bookmarks and create divs using the information in each.
  // The divs inside the form contain a hidden input 
  // that we can use to send the bk_poem_id value back
  // to the server.


const PoemCard = (props) => {
    let poem = props.poem
    return (
            <div className="col-md-4 col-sm-6 col-12 saved-poem-card purple" key = {poem[0]}>
                <form action="/savedpoem" method="POST">
                    <div className="bookmarked-poem-title"><strong>{poem[1]}</strong></div> 
                    <div>by {poem[2]}</div>
                    <input type="hidden" name="bk_poem_id" value={poem[0]}></input>
                    <button type="submit" className="btn btn-outline-secondary" method="POST"> View/Edit Comments</button>
                </form>
            </div>
        ); 
    }

// Creating a container for the poem cards, that sets bookmarks
// as a state variable, uses a fetch request in a function to
// call the server for this data, then instantiates a child
// PoemCard object and passes the bookmark data to it as a prop.

const UserSavedPoems = (props) => {
    const [bookmarks, addBookmarks] = React.useState('');

    const fetchBookmarks = () => {
        fetch('/user-saved-bookmarks.json')
        .then((response) => response.json())
        .then((bookmarks_list) => {
            addBookmarks(bookmarks_list['bookmarks']);
        });
    }
    
    React.useEffect(fetchBookmarks, [])

    const poemCards = []

    for (let bookmark of bookmarks) {
        poemCards.push(<PoemCard key={bookmark[0]} poem={bookmark} />);
    }
      
    return (
        <section className="col-12 d-flex flex-wrap justify-content-evenly align-items-stretch" id="PoemCards">

            {poemCards}

        </section>
    );
  }


  // ============ Prompt Container ============ //


const PromptCard = (props) => {

    const [publicPromptBool, updatePublicPromptBool] = React.useState(props.prompt[3]);
    const prompt = props.prompt;

    function updatePromptBoolInDB () {

        fetch('/update-prompt-bool.json', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "public_check": publicPromptBool,
                "saved_prompt_id": prompt[0]
                })
            })
        .then((response) => response.text())
        .then((responseJSON) => {
            // console.log(responseJSON)
            // console.log(publicPromptBool)
            if (responseJSON === "wrong user") {
                alert("There appears to be an error - please confirm you are logged in to the correct account.")
            }
            if (responseJSON == "ok" && publicPromptBool == true) {
                alert("Your response has been set to public - other users can now view it.")
            }
            else if (responseJSON == "ok" && publicPromptBool == false) {
                alert("Your response has been set to private - only you can see it.")
            }
        });
    }

    return (
        <div className="prompt-card col-md-4 col-sm-6 col-12" key={prompt[0]}>
            <div>    
                <div className="view-prompt purple">
                    <form action="/savedprompt" method="POST">
                        <p>
                            <strong>{prompt[2]}</strong>
                        </p>
                        <p>
                            <button className="btn btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target={`#collapseBody${prompt[0]}`} aria-expanded="false" aria-controls={`collapseBody${prompt[0]}`}>
                                View
                            </button>
                        </p>
                        <div className="collapse" id={`collapseBody${prompt[0]}`}>
                            <div className="card card-body">
                                {prompt[1]}
                            </div><br></br>
                        </div>
                        <p>
                            <input type="hidden" name="prompt_id" value={prompt[0]} />
                            <button type="submit" className="btn btn-outline-secondary" method="POST">Edit Response</button>
                        </p>
                    </form>
                </div>
                <div className="make-public-prompt">
                    <form action="/update-public-prompt" method="POST">
                        <div>
                            <input type="checkbox" name="public-check" id={`${prompt[0]}-public-check`} checked={publicPromptBool} onChange={(event) => updatePublicPromptBool(event.target.checked)}/> 
                            Public
                            <div>
                                <input type="hidden" name="mashup_public" value={prompt[4]}/>
                                <input type="button" className="update-btn btn btn-outline-secondary" method="POST" value="Update" onClick={updatePromptBoolInDB}/>                                
                                <a className="btn btn-secondary-outline q" data-bs-toggle="collapse" href={`#moreInfo${prompt[0]}`} role="button" aria-expanded="false" aria-controls={`moreInfo${prompt[0]}`}>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info-circle" viewBox="0 0 16 16">
                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                    <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
                                    </svg>
                                </a>
                                <div className="collapse" id={`moreInfo${prompt[0]}`}>
                                    <div className="card card-body">
                                        Make your response public, so other users can search for it.
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}


const UserSavedPrompts = (props) => {
    const [savedPrompts, updatePrompts] = React.useState([]);

    const fetchPrompts = () => {
        fetch('/user-saved-prompts.json')
        .then((response) => response.json())
        .then((savedPromptsJSON) => {
            updatePrompts(savedPromptsJSON['user_prompts'])
        })
    }

    React.useEffect(fetchPrompts, [])

    let promptCards = [];
    for (let prompt of savedPrompts) {
        promptCards.push(<PromptCard key={prompt[0]} prompt={prompt} />);
    }

    return (
        <section className="col-12 d-flex flex-wrap justify-content-evenly align-items-stretch" id="PromptCards">
            {promptCards}
        </section>
    )
}


// ============ Mashup Container ============ //

const MashupCard = (props) => {

    const mashup = props.mashup
    const [publicMashupBool, updatePublicMashupBool] = React.useState(mashup[2])

    // console.log(mashup[0])
    function updateMashupBoolInDB () {

        fetch('/update-mashup-bool.json', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "public_check": publicMashupBool,
                "saved_mashup_id": mashup[0]
                })
            })
        .then((response) => response.text())
        .then((responseJSON) => {
            // console.log(responseJSON)
            // console.log(publicMashupBool)
            if (responseJSON === "wrong user") {
                alert("There appears to be an error - please confirm you are logged in to the correct account.")
            }
            if (responseJSON == "ok" && publicMashupBool == true) {
                alert("This mashup has been set to public - other users can now view it.")
            }
            else if (responseJSON == "ok" && publicMashupBool == false) {
                alert("This mashup has been set to private - only you can see it.")
            }
        })
    }

    return (
            <div key={mashup[0]} className="mashup-card col-md-4 col-sm-6 col-12">
                <div className="view-mashup purple">
                    <div className="saved-mashup-title"><strong>{mashup[1]}</strong></div>
                        <form action="/savedmashup" method="POST" className="mashup-form">
                            <input type="hidden" name="mashup_id" value={mashup[0]}/>
                            <button type="submit" className="btn btn-outline-secondary mashup-form-button" method="POST">View Mashup</button>
                        </form>
                </div>
                <div className="make-public-mashup">
                    <form action="/update-public-mashup" method="POST">
                        <div>
                            <input type="checkbox" id={`${mashup[0]}-public-check`} name="public-check" checked={publicMashupBool} onChange={(event) => updatePublicMashupBool(event.target.checked)} />
                            Public
                        </div>
                        <div>
                            <input type="button" method="POST" className="update-btn btn btn-outline-secondary" onClick={updateMashupBoolInDB} value="Update"/>
                            <a className="btn btn-secondary-outline q" data-bs-toggle="collapse" href={`#moreInfo${mashup[0]}`} role="button" aria-expanded="false" aria-controls={`moreInfo${mashup[0]}`}>
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info-circle" viewBox="0 0 16 16">
                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                    <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
                                </svg>
                            </a>
                            <div className="collapse" id={`moreInfo${mashup[0]}`}>
                                <div className="card card-body">
                                    Make your response public, so other users can search for it.
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        )
    }

const UserSavedMashups = (props) => {
    const [savedMashups, updateMashups] = React.useState([]);

    const fetchMashups = () => {
        fetch('/user-saved-mashups.json')
        .then((response) => response.json())
        .then((savedMashupsJSON) => {
            // console.log(savedMashupsJSON)
            updateMashups(savedMashupsJSON['user_mashups'])
        })
    }

    React.useEffect(fetchMashups, [])

    let mashupCards = []
    for (let mashup of savedMashups) {
        mashupCards.push(<MashupCard key={mashup[0]} mashup={mashup}/>)
    };

    return (
        <React.Fragment>

            <section className="col-12 d-flex flex-wrap justify-content-evenly align-items-stretch" id="MashupCards">
                {mashupCards}
            </section>

        </ React.Fragment>
    )
}


// ============ Deactivate Component ============ //

const DeactivateAccount = (props) => {

    return (
    <React.Fragment>
        <p>
            Would you like to deactivate your account?
        </p>
        <form action="/deactivate-account-check">
            <button className="btn btn-outline-danger" id="deactivate-button">Deactivate</button>
        </form>
    </React.Fragment>
    )
}



ReactDOM.render(<UsernameCard />, document.querySelector('#username'))
ReactDOM.render(<UserSavedPoems />, document.querySelector('#saved_poems'));
ReactDOM.render(<UserSavedPrompts />, document.querySelector('#saved_prompts'));  
ReactDOM.render(<UserSavedMashups />, document.querySelector('#saved_mashups'));
ReactDOM.render(<DeactivateAccount />, document.querySelector('#account-settings'))    