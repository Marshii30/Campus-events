import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { getEvent, registerEvent, sendFeedback } from "../api/api";
import Rating from "../components/Rating";

export default function EventDetails(){
  const { id } = useParams();
  const [event, setEvent] = useState(null);
  const [studentUid, setStudentUid] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [regMsg, setRegMsg] = useState("");
  const [rating, setRating] = useState(5);
  const [comments, setComments] = useState("");
  const [feedbackMsg, setFeedbackMsg] = useState("");

  useEffect(()=>{
    getEvent(id).then(res => setEvent(res.data)).catch(()=>setEvent(null));
  },[id]);

  const handleRegister = async () => {
    if(!studentUid) { setRegMsg("Enter student UID"); return; }
    const payload = { student_uid: studentUid, college_id:1, name, email };
    try {
      const res = await registerEvent(id, payload);
      setRegMsg(res.data.message || "Registered");
    } catch(e){
      setRegMsg(e?.response?.data?.error || "Error");
    }
  };

  const handleFeedback = async () => {
    if(!studentUid){ setFeedbackMsg("Enter student UID to submit feedback"); return; }
    const payload = { student_uid: studentUid, college_id:1, rating, comments };
    try {
      const res = await sendFeedback(id, payload);
      setFeedbackMsg(res.data.message || "Thanks for feedback");
    } catch(e){
      setFeedbackMsg(e?.response?.data?.error || "Error");
    }
  };

  if(!event) return <div className="card">Loading event...</div>;

  return (
    <div>
      <div className="card">
        <h2 className="event-title">{event.title}</h2>
        <div className="event-meta">{event.event_type} • {event.location || 'TBA'}</div>
        <p style={{color:"var(--muted)"}}>{event.description}</p>
      </div>

      <div className="card">
        <h3>Register for this event</h3>
        <label className="label">Student UID</label>
        <input className="input" placeholder="e.g. S123" value={studentUid} onChange={e=>setStudentUid(e.target.value)} />
        <label className="label">Name</label>
        <input className="input" placeholder="Your name" value={name} onChange={e=>setName(e.target.value)} />
        <label className="label">Email</label>
        <input className="input" placeholder="you@college.edu" value={email} onChange={e=>setEmail(e.target.value)} />
        <div style={{marginTop:12}}>
          <button className="btn" onClick={handleRegister}>Register</button>
          <div style={{marginTop:8,color:"var(--muted)"}}>{regMsg}</div>
        </div>
      </div>

      <div className="card">
        <h3>Submit Feedback (rating 1–5)</h3>
        <label className="label">Your UID (to identify)</label>
        <input className="input" placeholder="Student UID" value={studentUid} onChange={e=>setStudentUid(e.target.value)} />
        <label className="label">Rating</label>
        <Rating value={rating} onChange={setRating} />
        <label className="label">Comments (optional)</label>
        <textarea className="input" rows="4" value={comments} onChange={e=>setComments(e.target.value)} />
        <div style={{marginTop:12}}>
          <button className="btn" onClick={handleFeedback}>Submit Feedback</button>
          <div style={{marginTop:8,color:"var(--muted)"}}>{feedbackMsg}</div>
        </div>
      </div>
    </div>
  )
}
