import { useState } from "react";
import { markAttendance } from "../api/api";
import "../styles/main.css"; // ensure styles are loaded

export default function CheckIn(){
  const [studentUid, setStudentUid] = useState("");
  const [eventId, setEventId] = useState("");
  const [msg, setMsg] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [toast, setToast] = useState(null); // { type: 'success'|'error', text }

  // show a popup toast for n seconds
  const showToast = (type, text, ms = 3500) => {
    setToast({ type, text });
    // auto hide after ms unless user hovers (simple)
    const id = setTimeout(() => {
      setToast(null);
      clearTimeout(id);
    }, ms);
  };

  const handleCheckin = async () => {
    setMsg("");
    if(!eventId || !studentUid){
      showToast("error", "Enter both Event ID and Student UID");
      return;
    }

    setIsLoading(true);
    try {
      const payload = { student_uid: studentUid, college_id:1, method: "manual" };
      const res = await markAttendance(eventId, payload);
      console.log("Attendance response:", res);
      // backend returns { message: "attendance marked", attendance_id: X } on success
      const body = res?.data || {};
      const successText = body.message || "Attendance marked";
      showToast("success", successText);
      setMsg(successText);
      // optionally clear inputs after success:
      // setStudentUid(""); setEventId("");
    } catch (err) {
      console.error("Attendance error:", err?.response || err);
      const errorText = err?.response?.data?.error || err?.message || "Unknown error";
      showToast("error", `Error: ${errorText}`);
      setMsg(`Error: ${errorText}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <div className="card" style={{maxWidth:700, margin:"0 auto"}}>
        <h3>Admin Check-In</h3>
        <div style={{marginTop:8}}>
          <label className="label">Event ID</label>
          <input
            className="input"
            placeholder="Event ID (e.g. 1)"
            value={eventId}
            onChange={(e) => setEventId(e.target.value)}
          />
        </div>

        <div style={{marginTop:12}}>
          <label className="label">Student UID</label>
          <input
            className="input"
            placeholder="Student UID (e.g. S123)"
            value={studentUid}
            onChange={(e) => setStudentUid(e.target.value)}
          />
        </div>

        <div style={{marginTop:16, display:"flex", gap:12, alignItems:"center"}}>
          <button className="btn" onClick={handleCheckin} disabled={isLoading}>
            {isLoading ? "Marking..." : "Mark Attendance"}
          </button>

          <div style={{color:"var(--muted)", fontSize:13}}>
            {msg}
          </div>
        </div>

        <div style={{marginTop:14, color:"var(--muted)", fontSize:13}}>
          Tip: Use the event ID from the event details page. For production you can integrate a QR scanner.
        </div>
      </div>

      {/* Toast popup */}
      {toast && (
        <div
          onMouseEnter={() => {}}
          onMouseLeave={() => {}}
          style={{
            position: "fixed",
            right: 20,
            top: 20,
            minWidth: 260,
            zIndex: 9999,
            borderRadius: 10,
            padding: "12px 16px",
            boxShadow: "0 8px 30px rgba(0,0,0,0.6)",
            background: toast.type === "success" ? "linear-gradient(90deg,#10b981,#34d399)" : "linear-gradient(90deg,#ef4444,#fb7185)",
            color: "#021118",
            fontWeight: 700,
          }}
        >
          {toast.text}
        </div>
      )}
    </div>
  );
}
