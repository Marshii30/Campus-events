import { useEffect, useState } from "react";
import { eventPopularity, studentParticipation, mostActive } from "../api/api";

export default function Reports(){
  const [popularity, setPopularity] = useState([]);
  const [students, setStudents] = useState([]);
  const [top, setTop] = useState([]);

  useEffect(()=>{
    const collegeId = 1;
    eventPopularity(collegeId).then(res => setPopularity(res.data)).catch(()=>setPopularity([]));
    studentParticipation(collegeId).then(res => setStudents(res.data)).catch(()=>setStudents([]));
    mostActive(collegeId,3).then(res => setTop(res.data)).catch(()=>setTop([]));
  },[]);

  return (
    <div>
      <div className="card">
        <h3>Event Popularity</h3>
        {popularity.length===0 ? <div className="kicker">No data</div> :
          popularity.map(ev => (
            <div key={ev.event_id} style={{display:"flex", justifyContent:"space-between", padding:"8px 0", borderBottom:"1px solid rgba(255,255,255,0.02)"}}>
              <div>
                <div style={{fontWeight:700}}>{ev.title}</div>
                <div className="kicker">{ev.event_type}</div>
              </div>
              <div style={{alignSelf:"center", fontWeight:700, color:"#a3e635"}}>{ev.registrations}</div>
            </div>
          ))
        }
      </div>

      <div className="card">
        <h3>Student Participation (events attended)</h3>
        {students.length===0 ? <div className="kicker">No data</div> :
          students.slice(0,10).map(s => (
            <div key={s.student_id} style={{display:"flex", justifyContent:"space-between", padding:"8px 0", borderBottom:"1px solid rgba(255,255,255,0.02)"}}>
              <div>
                <div style={{fontWeight:700}}>{s.name || s.student_uid}</div>
                <div className="kicker">UID: {s.student_uid}</div>
              </div>
              <div style={{alignSelf:"center", fontWeight:700, color:"#60a5fa"}}>{s.events_attended}</div>
            </div>
          ))
        }
      </div>

      <div className="card">
        <h3>Top 3 Most Active Students</h3>
        {top.length===0 ? <div className="kicker">No data</div> :
          top.map(t => (
            <div key={t.student_id} style={{display:"flex", justifyContent:"space-between", padding:"8px 0", borderBottom:"1px solid rgba(255,255,255,0.02)"}}>
              <div>
                <div style={{fontWeight:700}}>{t.name || t.student_uid}</div>
                <div className="kicker">UID: {t.student_uid}</div>
              </div>
              <div style={{alignSelf:"center", fontWeight:700, color:"#f97316"}}>{t.events_attended}</div>
            </div>
          ))
        }
      </div>
    </div>
  )
}
