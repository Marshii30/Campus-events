import { useState } from "react";
import { getStudentRegistrations } from "../api/api";

export default function MyRegistrations(){
  const [studentId, setStudentId] = useState("");
  const [regs, setRegs] = useState([]);
  const [msg, setMsg] = useState("");

  const fetchRegs = async () => {
    if(!studentId){ setMsg("Enter numeric student id"); return; }
    try {
      const res = await getStudentRegistrations(studentId);
      setRegs(res.data);
      setMsg("");
    } catch(e){
      setMsg("Error fetching registrations");
      setRegs([]);
    }
  };

  return (
    <div>
      <div className="card">
        <h3>View your registrations</h3>
        <label className="label">Student DB id (example: 1)</label>
        <input className="input" value={studentId} onChange={e=>setStudentId(e.target.value)} placeholder="DB student id (not UID)" />
        <div style={{marginTop:10}}>
          <button className="btn" onClick={fetchRegs}>Fetch</button>
          <div style={{marginTop:8,color:"var(--muted)"}}>{msg}</div>
        </div>
      </div>

      <div>
        {regs.map(r => (
          <div key={r.registration_id} className="card">
            <div style={{display:"flex", justifyContent:"space-between"}}>
              <div>
                <div style={{fontWeight:700}}>Event ID: {r.event_id}</div>
                <div className="kicker">Registered at: {new Date(r.registered_at).toLocaleString()}</div>
              </div>
              <div style={{alignSelf:"center"}}>
                <div style={{color:"#60a5fa", fontWeight:700}}>{r.status}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
