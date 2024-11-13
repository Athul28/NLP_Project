"use client";

import { useState } from "react";

export default function Home() {
  const [positive,setPositive]=useState(0)
  const [negative,setNegative]=useState(0)
  const [neutral,setNeutral]=useState(0)
  const [loading,setLoading]=useState(false)


  const getComments = async() => {
    const youtubeLink = (document.querySelector('input[type="text"]') as HTMLInputElement).value;
    const noOfComments = (document.querySelector('input[type="number"]') as HTMLInputElement).value;

    setLoading(true)

    const response = await fetch('http://localhost:5000/predictComments', {
      method: 'POST',
      headers: {
      'Content-Type': 'application/json'
      },
      body: JSON.stringify({
      "url":youtubeLink,
      "noComments":noOfComments
      })
    });

    const data = await response.json();
    console.log(data["Sentimental Analysis"]);
    const sentiments=data["Sentimental Analysis"]
    setPositive(sentiments.positive)
    setNegative(sentiments.negative)
    setNeutral(sentiments.neutral)
    setLoading(false)
  };

  return (
    <div>
      <p>Enter the inputs : </p>
      <label htmlFor="youtube-link">Enter the app id : </label>
      <input type="text" className="text-black"/>
      <br />
      <br />
      <label htmlFor="no-comments">No of reviews : </label>
      <input type="number" className="text-black"/>
      <br />
      <button onClick={getComments}>Submit</button>
      {!loading ? (
        <div>
          <p>Sentiments</p>
          <p>Positive : {positive}</p>
          <p>Negative : {negative}</p>
          <p>Neutral : {neutral}</p>
        </div>
      ) : (
        <p>Loading</p>
      )}
    </div>
  );
}
