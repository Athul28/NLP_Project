"use client";

import { useState } from "react";
import LoadingIcons from 'react-loading-icons'
import { apps_array } from "@/lib/data";



export default function Home() {
  const [positive,setPositive]=useState(0)
  const [negative,setNegative]=useState(0)
  const [neutral,setNeutral]=useState(0)
  const [loading,setLoading]=useState(false)
  const [keyWords,setKeyWords]=useState<string[]>([])
  const BASE_URL=process.env.BASE_URL || 'http://localhost:5000'

  console.log(BASE_URL)

  console.log(apps_array)


  const getComments = async() => {
    const id = (document.querySelector('select') as HTMLSelectElement).value;
    console.log(id)
    const noOfComments = (document.querySelector('input[type="number"]') as HTMLInputElement).value;

    setLoading(true)

    const response = await fetch(`${BASE_URL}/predictComments`, {
      method: 'POST',
      headers: {
      'Content-Type': 'application/json'
      },
      body: JSON.stringify({
      "url":id,
      "noComments":noOfComments
      })
    });

    const data = await response.json();
    console.log(data)
    console.log(data["Sentimental Analysis"]);
    const sentiments=data["Sentimental Analysis"]
    setPositive(sentiments.positive)
    setNegative(sentiments.negative)
    setNeutral(sentiments.neutral)
    setLoading(false)
    setKeyWords(data["Key Words"])
  };

  return (
    <div>
      <div className="border border-white p-10 m-auto w-fit rounded-lg mt-10">
      <p className="text-xl">Google Play Store reviews analysis</p>
      <br />
      <label htmlFor="youtube-link">Enter the app id : </label>
      {/* <input type="text" className="text-black p-2 rounded-xl" /> */}
      <select name="" id="" className="text-black p-2">
        <option value="" disabled selected>Select an option</option>
        {
          apps_array.map((item, i) => {
        return <option key={i} value={item.package} className="text-black">{item.name}</option>
          })
        }
      </select>
      <br />
      <br />
      <label htmlFor="no-comments">No of reviews : </label>
      <input type="number" className="text-black p-2 rounded-xl" />
      <br />
      <div className="w-fit m-auto">

      <button onClick={getComments} className="bg-purple-700 px-4 py-3 mt-3 rounded-md">Submit</button>
      </div>
      </div>
      {!loading ? (
      <div>
        <div className="border border-white w-fit m-auto mt-5 p-5 flex flex-col items-center">
        <p className="text-xl font-bold underline">Sentiments</p>
        <p className="text-green-500">Positive : {positive}</p>
        <p className="text-red-500">Negative : {negative}</p>
        <p className="text-blue-400">Neutral : {neutral}</p>
        </div>

        <div className="p-5">
          <p className="text-center my-5 text-xl font-bold underline">Key Words:</p>
          <ul className="flex flex-wrap">
          {keyWords.map((word, index) => (
            <li key={index} className=" bg-slate-700 m-2 p-3">{word}</li>
          ))}
          </ul>
        </div>
      </div>
      ) : (
      <div className="w-fit m-auto"><LoadingIcons.Bars /></div>
      )}
    </div>
  );
}
