import React from 'react';

const Show = ({show}) =>
  <div className="show-container">
    <h3>{show.name}</h3>
    <p>IMDb: {show.rating}</p>
    <p>Runtime: {show.runtime} min</p>
  </div>

export default Show;
