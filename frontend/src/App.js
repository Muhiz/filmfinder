import React from 'react';
import {render} from 'react-dom';
import axios from 'axios';

import ShowsList from './ShowsList.js';


let apiBase = 'https://filmfinder-api.herokuapp.com/api';


let theatres = [];
let shows = [];

let Loader = function(props){
    if(!props.isReady){
        return (<div className="loader"></div>);
    }
    else{
        return (<div className="loader-ready"></div>);
    }
}



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
        this.setClosestTheatre = this.setClosestTheatre.bind(this);
        //this.loadTheatres = this.loadTheatres.bind(this);
    }

    componentDidMount(){

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


        let that = this;
        // Fetch theatres
        axios.get(apiBase+'/theatres').then((response) => {
    
            var newTheatres = response.data.theatres;
            that.setState({theatres: newTheatres});

            that.setClosestTheatre();

        }).catch((error) => {
            console.log(error);
        });
    }

    handleTheatreChange(event){
        
        this.setState({currentTheatre: event.target.value});
        // Clear shows
        this.setState({shows:[]});

        // Fetch shows
        let that = this;
        axios.get(apiBase+'/theatres/'+event.target.value+'/shows').then((response) => {
            that.setState({shows: response.data.shows});
        });
    }

    setClosestTheatre(){

        var closestId = 0;
        var minDistance = 360;
        
        var newTheatres = this.state.theatres.slice();

        for (var i = newTheatres.length - 1; i >= 0; i--) {
            newTheatres.isClosest = false;

            if(newTheatres[i].location == null){
                continue;
            }

            var x0 = this.state.location.latitude;
            var x1 = newTheatres[i].location.lat;
            var y0 = this.state.location.longitude;
            var y1 = newTheatres[i].location.lng;

            var dist = Math.sqrt((x0-x1)*(x0-x1) + (y0-y1)*(y0-y1));

            if(dist < minDistance){
                minDistance = dist;
                closestId = i;
            }
        }
        newTheatres[closestId].isClosest = true;

        this.setState({theatres: newTheatres});

        // trigger fake event to update shows
        var fakeEvent = {
            target: {
                value: newTheatres[closestId].id
            }
        };
        this.handleTheatreChange(fakeEvent);


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
                                <option key={theatre.id} value={theatre.id} selected={theatre.isClosest == true}>{theatre.city} - {theatre.name}</option>
                            );
                        })}                
                    </select>
                    <ShowsList shows={this.state.shows} />
                    <Loader isReady={this.state.shows.length} />
                </div>
            </div>
        );
        
    }
}

render(<App />, document.getElementById('app'));
