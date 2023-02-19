// React component to update username in navbar

const UsernameCorner = (props) => {
    const [username, updateUsername] = React.useState('');

    const fetchUsername = () => {
        fetch('/username-corner.json')
        .then((response) => response.text())
        .then((usernameJSON) => {
            updateUsername(usernameJSON)
        })
    };

    React.useEffect(fetchUsername, []);

    return (
        <React.Fragment>
            {username}
        </React.Fragment>
    );
}

ReactDOM.render(<UsernameCorner />, document.querySelector('#username-corner'));
