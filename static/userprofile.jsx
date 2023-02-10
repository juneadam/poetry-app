// React test to generate HTML for user profile

  // ------------ Username Container ------------ //

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

  

  // ------------ Poem Container ------------ //


  // creating a PoemCard React object, which will be a
  // child component of the UserSavedPoems React Object
  // and will take in the parent's state value of an array
  // of bookmarks and create divs using the information in each.
  // The divs inside the form contain a hidden input 
  // that we can use to send the bk_poem_id value back
  // to the server.


const PoemCard = (props) => {
    const PoemCards = [];
    for (const poem of props.bookmarks) {

        PoemCards.push(
            <div className="col" key = {poem[0]}>
            <form action="/savedpoem" className="saved-poem-card" method="POST">
                <div className="bookmarked-poem-link"><strong>{poem[1]}</strong></div> 
                <div>by {poem[2]}</div>
                <input type="hidden" name="bk_poem_id" value={poem[0]}></input>
                <button type="submit" className="btn btn-outline-secondary" method="POST"> View/Edit Comments</button>
            </form>
            </div>
        ); 
    }

    return <section className="PoemCards">{PoemCards}</section>;
};


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
      
    return (
        <div>

            <div className="container">
            <PoemCard bookmarks={bookmarks} />
            </div>

        </div>
    );
  }


  // ------------ Prompt Container ------------ //


const PromptCard = (props) => {

    const [publicPromptBool, updatePublicPromptBool] = React.useState(props.prompt[3]);
    const prompt = props.prompt;

    function updatePromptBoolInDB () {
        let publicCheck = document.querySelector(`#${prompt[0]}-public-check`).checked

        fetch('/update-prompt-bool', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "public_check": publicCheck,
                "saved_prompt_id": prompt[0]
                })
            })
        .then((response) => response.json())
        .then((responseJSON) => {
            alert("hold on")
        })
    }

    return (
        <div className="prompt-card" key={prompt[0]}>
            <div>    
                <div className="view-prompt">
                    <form action="/savedprompt" method="POST">
                        <p><strong>{prompt[2]}</strong></p>
                        <p>
                            <button className="btn btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target={`#collapseBody${prompt[0]}`} aria-expanded="false" aria-controls={`collapseBody${prompt[0]}`}>
                                View
                            </button>
                        </p>
                        <div className="collapse" id={`collapseBody${prompt[0]}`}>
                            <div className="card card-body">
                                {prompt[1]}
                            </div>
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
                        <input type="checkbox" name="public-check" id={`${prompt[0]}-public-check`} checked={publicPromptBool} onChange={(event) => updatePublicPromptBool(event.target.checked)}/> Public
                        <div><input type="hidden" name="mashup_public" value={prompt[4]}/>
                        <input type="button" className="update-btn" method="POST" value="Update" onClick={updatePromptBoolInDB}/>                                
                            <a className="btn btn-secondary-outline" data-bs-toggle="collapse" href={`#moreInfo${prompt[0]}`} role="button" aria-expanded="false" aria-controls={`moreInfo${prompt[0]}`}>
                            ?
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
        <section id="PromptCards">
        <div className='container'>
        
            {promptCards}

        </div>
        </section>
    )
}


// ------------ Mashup Container ------------ //

const MashupCard = (props) => {

    let mashup = props.mashup
    const [publicMashupBool, updatePublicMashupBool] = React.useState(mashup[0])

    function updateMashupBoolInDB () {
        let publicCheck = document.querySelector(`#${mashup[0]}-public-check`).checked

        fetch('/update-prompt-bool', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "public_check": publicCheck,
                "saved_mashup_id": mashup[0]
                })
            })
        .then((response) => response.json())
        .then((responseJSON) => {
            alert("hold on")
        })
    }

    return (
            <div key={mashup[0]} className="mashup-card">
                <div className="view-mashup">
                <div className="saved-mashup-title"><strong>{mashup[1]}</strong></div>
                    <form action="/savedmashup" method="POST">
                        <input type="hidden" name="mashup_id" value={mashup[0]}/>
                        <button type="submit" className="btn btn-outline-secondary" method="POST">View Mashup</button>
                    </form>
                </div>
                <div className="make-public-mashup">
                    <form action="/update-public-mashup" method="POST">
                        <div>
                            <input type="checkbox" id={`${mashup[0]}-public-check`} name="public-check" checked={publicMashupBool} onChange={(event) => updatePublicMashupBool(event.target.checked)} />
                            <input type="hidden" name="mashup_public" value={mashup[3]}/> Public
                        </div>
                        <div>
                            <input type="button" method="POST" onClick={updateMashupBoolInDB} value="Update"/>
                            <a className="btn btn-secondary-outline" data-bs-toggle="collapse" href={`#moreInfo${mashup[0]}`} role="button" aria-expanded="false" aria-controls={`moreInfo${mashup[0]}`}>
                                ?
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
        <div className='container'>

            <section id="MashupCards">
                {mashupCards}
            </section>

        </div>
    )
}


ReactDOM.render(<UsernameCard />, document.querySelector('#username'))
ReactDOM.render(<UserSavedPoems />, document.querySelector('#saved_poems'));
ReactDOM.render(<UserSavedPrompts />, document.querySelector('#saved_prompts'));  
ReactDOM.render(<UserSavedMashups />, document.querySelector('#saved_mashups'));    