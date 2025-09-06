export default function Footer(){
  return (
    <footer>
      <div className="container" style={{display:"flex", justifyContent:"space-between", alignItems:"center"}}>
        <div>© {new Date().getFullYear()} Campus Events • Built with ❤️</div>
        <div style={{color:"var(--muted)"}}>Dark theme • Recruiter-ready UI</div>
      </div>
    </footer>
  );
}
