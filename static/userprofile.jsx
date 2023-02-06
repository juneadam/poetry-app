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
                <a href='#' className="bookmarked-poem-link">{poem[1]} by {poem[2]}</a>
                <input type="hidden" name="bk_poem_id" value={poem[0]}></input>
                <input type="submit" method="POST" value="View/Edit Comments"></input>
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
                <div className="view-prompt">
                    <form action="/savedprompt" method="POST">
                        <a href='#' className="saved-prompt-link">{prompt[2]}</a>
                        <div className="promptList">
                            <ul>
                                <li>{prompt[1]}</li>
                                <li>
                                    <input type="hidden" name="prompt_id" value={prompt[0]} />
                                    <input type="submit" method="POST" value="View/Edit Response" />
                                </li>
                            </ul>
                        </div>
                    </form>
                </div>
                <div className="make-public-prompt">
                    <form action="/update-public-prompt" method="POST">
                        <input type="checkbox" name="public-check" checked={prompt[3]} />Make your response public, so other users can search for it?
                        <input type="hidden" name="mashup_public" value={prompt[4]}/>
                        <input type="submit" method="POST" value="Update"/>
                    </form>
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
    console.log(props.savedMashups);
    for (const mashup of props.savedMashups) {
        MashupCards.push(
            <div key={mashup[0]} className="mashup-card">
                <div className="view-mashup">
                <a href='#' className="saved-mashup-link">{mashup[1]}</a>
                    <form action="/savedmashup" method="POST">
                        <input type="hidden" name="mashup_id" value={mashup[0]}/>
                        <input type="submit" method="POST" value="View/Edit Response"/>
                    </form>
                </div>
                <div className="make-public-mashup">
                    <form action="/update-public-mashup" method="POST">
                        <input type="checkbox" name="public-check" checked={mashup[2]} />Make this mashup public, so other users can search for it?
                        <input type="hidden" name="mashup_public" value={mashup[3]}/>
                        <input type="submit" method="POST" value="Update"/>
                    </form>
                </div>
            </div>
            
        )
    }
    console.log(MashupCards);
    return <section id="MashupCards">{MashupCards}</section>;
}

const UserSavedMashups = (props) => {
    const [savedMashups, updateMashups] = React.useState([]);

    const fetchMashups = () => {
        fetch('/user-saved-mashups.json')
        .then((response) => response.json())
        .then((savedMashupsJSON) => {
            console.log(savedMashupsJSON)
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