"use client";

export default function Home() {
  const getComments = async() => {
    const youtubeLink = (document.querySelector('input[type="text"]') as HTMLInputElement).value;
    const noOfComments = (document.querySelector('input[type="number"]') as HTMLInputElement).value;

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
    console.log(data);
    console.log("Clicked");
  };

  return (
    <div>
      <p>Enter the inputs : </p>
      <label htmlFor="youtube-link">Youtube link : </label>
      <input type="text" className="text-black"/>
      <br />
      <br />
      <label htmlFor="no-comments">No of comments : </label>
      <input type="number" className="text-black"/>
      <br />
      <button onClick={getComments}>Submit</button>
    </div>
  );
}
