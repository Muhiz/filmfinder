import React from 'react';
import {render} from 'react-dom';
import axios from 'axios';

import ShowsList from './ShowsList.js';
import TheatreSelector from './TheatreSelector';


let apiBase = 'https://filmfinder-api.herokuapp.com/api';


let theatres = [
    {
        id: 0,
        name: 'Loading...',
        city:''
    }
];

let shows = [

];


class App extends React.Component {

    constructor(props) {
        super(props);


        // Set initial location to Helsinki
        this.state = {
            currentTheatre: 0, // Id of current theatre
            shows: shows,
            theatres: theatres,
            location: {
                latitude: 60.1695200,
                longitude: 24.9354500
            }
        }

        // We need to bind to this
        this.handleTheatreChange = this.handleTheatreChange.bind(this);


    }

    componentDidMount(){

        let that = this;
        // Fetch theatres
        axios.get(apiBase+'/theatres').then((response) => {
    
            that.setState({theatres: response.data.theatres});

        }).catch((error) => {
            console.log(error);
        });


        // Ask for user location
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(function(pos){
                that.setState({
                    location: {
                        latitude: pos.coords.latitude,
                        longitude: pos.coords.longitude
                    }
                });
            });
        }


    }

    handleTheatreChange(event){
        

        this.setState({currentTheatre: event.target.value});
        // Fetch shows

        let that = this;
        axios.get(apiBase+'/theatres/'+event.target.value+'/shows').then((response) => {
            that.setState({shows: response.data.shows});
            console.log(response.data.shows);
        });
    }

    render() {
        return (
            <div>
                <div className="header">
                    <h1>FilmFinder</h1>
                </div>
                <div className="content">
                    <select onChange={this.handleTheatreChange}>
                        <option key="0" value="0">Select theatre...</option>
                        {this.state.theatres.map( function(theatre, i) {
                            return (
                                <option key={theatre.id} value={theatre.id}>{theatre.city} - {theatre.name}</option>
                            );
                        })}                
                    </select>
                    <ShowsList shows={this.state.shows} />
                </div>
            </div>
        )
    }
}

render(<App />, document.getElementById('app'));
