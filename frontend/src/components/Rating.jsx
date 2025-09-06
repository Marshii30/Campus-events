import { useState } from "react";

export default function Rating({ value=0, onChange }) {
  const [rating, setRating] = useState(value);
  const stars = [1,2,3,4,5];
  function setVal(n){
    setRating(n);
    if(onChange) onChange(n);
  }
  return (
    <div style={{display:"flex", gap:8, alignItems:"center"}}>
      {stars.map(s => (
        <div key={s} onClick={()=>setVal(s)} style={{cursor:"pointer", fontSize:22, color: s<=rating ? "#facc15" : "rgba(255,255,255,0.12)"}}>
          ★
        </div>
      ))}
    </div>
  );
}
