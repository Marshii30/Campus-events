import { useEffect, useState } from "react";
import { fetchEvents } from "../api/api";
import EventCard from "../components/EventCard";

export default function Home(){
  const [events, setEvents] = useState([]);
  const [query, setQuery] = useState("");
  const [type, setType] = useState("");

  useEffect(()=>{
    fetchEvents().then(res => setEvents(res.data)).catch(()=>setEvents([]));
  },[]);

  const filtered = events.filter(e => {
    if(type && e.event_type !== type) return false;
    if(query && !(`${e.title} ${e.description}`.toLowerCase().includes(query.toLowerCase()))) return false;
    return true;
  });

  return (
    <div>
      <div style={{display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:18}}>
        <div>
          <h2 style={{margin:0}}>Upcoming Events</h2>
          <div className="kicker">Browse and register for events at your college</div>
        </div>
        <div style={{display:"flex", gap:8}}>
          <input className="input" placeholder="Search events..." value={query} onChange={e=>setQuery(e.target.value)} style={{width:220}} />
          <select className="input" value={type} onChange={e=>setType(e.target.value)}>
            <option value="">All types</option>
            <option value="Workshop">Workshop</option>
            <option value="Hackathon">Hackathon</option>
            <option value="Seminar">Seminar</option>
            <option value="Fest">Fest</option>
            <option value="Talk">Talk</option>
          </select>
        </div>
      </div>

      <div className="event-grid">
        {filtered.map(ev => <EventCard key={ev.id} event={ev} />)}
      </div>
    </div>
  )
}
