import { Link } from "react-router-dom";

export default function Header(){
  return (
    <header className="header">
      <div className="brand">
        <div className="logo">CE</div>
        <div>
          <h1>Campus Events</h1>
          <div className="kicker">College event reporting & management</div>
        </div>
      </div>

      <nav className="nav">
        <Link to="/">Home</Link>
        <Link to="/registrations">My Registrations</Link>
        <Link to="/checkin">Check-In</Link>
        <Link to="/reports">Reports</Link>
      </nav>
    </header>
  )
}
