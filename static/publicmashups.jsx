// React file for generating HTML for public mashups template

const MashupCard = (props) => {
    const mashup = props.mashup
        return (
            <div className="mashupCard col-md-3 col-sm-6 col-auto purple" key={mashup[0]}>
                <form action="/savedmashup" method="POST">
                    <p><strong>{mashup[1]}</strong> by {mashup[2]}</p>
                    <input type="hidden" name="mashup_id" value={mashup[0]}></input>
                    <input type="submit" method="POST" value="View"></input>
                </form>
            </div>
        )
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

const mashupCards = []

for (const mashup of mashups) {
    mashupCards.push(<MashupCard mashup={mashup} />)
}
  
return (
    <React.Fragment>
        <section id="public-mashup-cards" className="d-flex flex-wrap justify-content-between align-items-stretch">
            {mashupCards}
        </section>
    </ React.Fragment>
);
}



ReactDOM.render(<PublicMashups />, document.querySelector('#display-results')); 