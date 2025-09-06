import { Link } from "react-router-dom";

export default function EventCard({ event }) {
  return (
    <div className="card">
      <h2 style={{ color: "#facc15" }}>{event.title}</h2>
      <p>{event.description}</p>
      <p><b>Type:</b> {event.event_type}</p>
      <p><b>Status:</b> {event.status}</p>
      <Link to={`/events/${event.id}`}>
        <button>View Details</button>
      </Link>
    </div>
  );
}
