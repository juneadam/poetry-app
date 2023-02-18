// React file for generating HTML for public prompts template

const ResponseCard = (props) => {
    const response = props.response 
        return (
            <div className="responseCard  col-md-3 col-sm-10 purple" key={response[0]}>
                <p><strong>{response[1]}</strong></p>
                <p>by {response[2]}</p>
                <p>
                    <button className="btn btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target={`#collapseBody${response[0]}`} aria-expanded="false" aria-controls={'collapseBody{response[0]'}>
                        View
                    </button>
                </p>
                <div className="collapse" id={`collapseBody${response[0]}`}>
                    <div className="card card-body">
                        {response[3]}
                    </div>
                </div>
            </div>
        )
    };


// Creating a container for the poem cards, that sets bookmarks
// as a state variable, uses a fetch request in a function to
// call the server for this data, then instantiates a child
// PoemCard object and passes the bookmark data to it as a prop.

const PublicResponses = (props) => {
    const [responses, addResponses] = React.useState('');

    const fetchPrompts = () => {
        fetch('/public-prompts.json')
        .then((response) => response.json())
        .then((responses_list) => {
            addResponses(responses_list['responses']);
        });
    }
    
    React.useEffect(fetchPrompts, [])
    const responseCards = []
    for (const response of responses) {
        responseCards.push(<ResponseCard response={response} />)
    }
      
    return (
        <div>

            <section id="public-response-cards" className="d-flex flex-wrap justify-content-between align-items-stretch">
                {responseCards}
            </section>

        </div>
    );
  }


  ReactDOM.render(<PublicResponses />, document.querySelector('#display-responses')); 

