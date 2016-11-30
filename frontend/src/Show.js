import React from 'react';

const Show = ({show}) =>
  <div className="show-container">
    <h3>{show.title}</h3>
    <p>Starts at {show.start_time}</p>
    <p>IMDb: {show.rating}</p>
    <p>Runtime: {show.runtime} min</p>
  </div>

export default Show;
