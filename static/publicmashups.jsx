// React file for generating HTML for public mashups template

const MashupCard = (props) => {
    const mashupCards = []
    for (const mashup of props.mashups) {
        mashupCards.push(
            <div className="mashupCard" key={mashup[0]}>
                <form action="/savedmashup" method="POST">
                    <p><strong>{mashup[1]}</strong> by {mashup[2]}</p>
                    <input type="hidden" name="mashup_id" value={mashup[0]}></input>
                    <input type="submit" method="POST" value="View"></input>
                </form>
            </div>
        )
    }
    return <section id="mashupCards">{mashupCards}</section>;
};



const PublicMashups = (props) => {
const [mashups, addMashups] = React.useState('');

const fetchMashups = () => {
    fetch('/public-mashups.json')
    .then((response) => response.json())
    .then((mashups_list) => {
        addMashups(mashups_list['mashups']);
    });
}

React.useEffect(fetchMashups, [])
  
return (
        <div className="container">
        <MashupCard mashups={mashups} />
        </div>
);
}



ReactDOM.render(<PublicMashups />, document.querySelector('#display-results')); 