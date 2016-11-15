import React from 'react';
import {render} from 'react-dom';
import ShowsList from './ShowsList.js';
import TheatreSelector from './TheatreSelector';

// TODO: Fetch Theatres and shows from server

let theatres = [
    {
        id: 1,
        name: 'Helsinki'
    },
    {
        id: 2,
        name: 'Tampere'
    }
];

let shows = [
    {
        id: 1,
        name: 'Inferno',
        runtime: 194,
        rating: '6.4'
    },
    {
        id: 2,
        name: 'Luokkakokous 2',
        runtime: 99,
        rating: '5.1'
    },
    {
        id:3,
        name: 'Trolls',
        runtime: 92,
        rating: '6.7'
    }
];



class App extends React.Component {

    constructor(props) {
        super(props);


        // Set initial location to Helsinki
        this.state = {
            location: {
                latitude: 60.1695200,
                longitude: 24.9354500
            }
        }
    }

    // Ask for user location
    componentDidMount(){
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(function(pos){
                console.log( "Latitude: " + pos.coords.latitude);
                console.log( "Longitude: " + pos.coords.longitude); 
            });
        }
    }


    render() {
        return (
            <div>
                <div className="header">
                    <h1>FilmFinder</h1>
                </div>
                <div className="content">
                    <TheatreSelector theatres={this.props.theatres} />
                    <ShowsList shows={this.props.shows} />
                </div>
            </div>
        )
    }
}

render(<App theatres={theatres} shows={shows} />, document.getElementById('app'));
