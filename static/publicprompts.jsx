// React file for generating HTML for public prompts template

const ResponseCard = (props) => {
        responseCards = []
        
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
            addResponses(responses_list['prompt']);
        });
    }
    
    React.useEffect(fetchPrompts, [])
      
    return (
        <div>

            <div className="container">
            <ResponseCard responses={responses} />
            </div>

        </div>
    );
  }