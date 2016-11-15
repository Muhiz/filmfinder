import React from 'react';
import Show from './Show';

class ShowsList extends React.Component {

    // Set initial state
    constructor(props) {
        super(props);
        this.state = {
            search: '',
            shows: props.shows
        }
    }

    _updateSearch(event) {
        this.setState({search: event.target.value});
    }

    render() {

        // Filter shows by searched keywords
        // TODO: Search for genres etc.

        let filteredShows = this.state.shows.filter(
            (show) => {
                return show.name.toLowerCase().indexOf( this.state.search.toLowerCase() ) >= 0;
            }
        );
        return (
            <div>
                <input type="text" placeholder="Filter name..." value={this.state.search} onChange={this._updateSearch.bind(this)} />

                <div>
                    {filteredShows.map((show) => {
                        return <Show show={show} key={show.id} />
                    })}
                </div>
            </div>
        )
    }
}

export default ShowsList;
