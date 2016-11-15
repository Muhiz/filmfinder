import React from 'react';

class TheatreSelector extends React.Component {

    // Set initial state
    
    constructor(props) {
        super(props);
        this.state = {
            selectedTheatre: null
        }
    }

    render(){
        return (
            <select>
                {this.props.theatres.map( function(theatre, i) {
                    return (
                        <option key={theatre.id} value={theatre.id}>{theatre.name}</option>
                    );
                })}                
            </select>
            /*<p>Theatre: {this.state.selectedTheatre}</p>*/
        );
    }

}

export default TheatreSelector;
