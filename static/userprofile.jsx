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
    const PromptCards = [];
    for (const prompt of props.savedPrompts) {
        PromptCards.push(
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
                            <p><div className="collapse" id={`collapseBody${prompt[0]}`}>
                                <div className="card card-body">
                                    {prompt[1]}
                                </div>
                            </div></p>
                            <p>
                                <input type="hidden" name="prompt_id" value={prompt[0]} />
                                <button type="submit" className="btn btn-outline-secondary" method="POST">Edit Response</button>
                            </p>
                        </form>
                    </div>
                    <div className="make-public-prompt">
                    <form action="/update-public-prompt" method="POST">
                        <div>
                            <input type="checkbox" name="public-check" checked={prompt[3]} /> Public
                            <div><input type="hidden" name="mashup_public" value={prompt[4]}/>
                            <input type="submit" className="btn-outline-secondary" method="POST" value="Update"/>                                
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
    return <section id="PromptCards">{PromptCards}</section>;
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


    return (
        <div className='container'>
        
        <PromptCard savedPrompts={savedPrompts}/>

        </div>
    )
}


// ------------ Mashup Container ------------ //

const MashupCard = (props) => {
    let MashupCards = [];
    // console.log(props.savedMashups);
    for (const mashup of props.savedMashups) {
        MashupCards.push(
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
                        <div><input type="checkbox" name="public-check" checked={mashup[2]} />
                            <input type="hidden" name="mashup_public" value={mashup[3]}/> Public
                        </div>
                        <div>
                            <input type="submit" method="POST" value="Update"/>
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
    // console.log(MashupCards);
    return <section id="MashupCards">{MashupCards}</section>;
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


    return (
        <div className='container'>
        
        <MashupCard savedMashups={savedMashups}/>

        </div>
    )
}


ReactDOM.render(<UsernameCard />, document.querySelector('#username'))
ReactDOM.render(<UserSavedPoems />, document.querySelector('#saved_poems'));
ReactDOM.render(<UserSavedPrompts />, document.querySelector('#saved_prompts'));  
ReactDOM.render(<UserSavedMashups />, document.querySelector('#saved_mashups'));    