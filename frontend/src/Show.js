import React from 'react';
import moment from 'moment';
import tz from 'moment-timezone';

const Show = ({show}) =>
  <div className="show-container">
    <div className="show-title">
        <h3>{show.title}</h3>
    </div>
    <div className="show-poster-container">
        <img className="show-poster" src="TODO" />
    </div>
    <div className="show-details">
        <div><i className="icon fa fa-clock-o"></i><span className="show-time">{moment(show.start_time, moment.ISO_8601).tz('Europe/Helsinki').calendar() }</span></div>
        <div><strong>IMDb rating:</strong> {show.rating}</div>
        <div><strong>Genres:</strong> {show.genre}</div>
        <div><strong>Duration:</strong> {show.runtime} min</div>
        <div>
            <a className="btn" href={"http://www.finnkino.fi/Event/"+ show.id +"/"}>Buy Tickets &raquo;</a>
        </div>

    </div>
    <div className="clear"></div>

  </div>

export default Show;
