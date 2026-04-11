import umeLogo from '../assets/UME_Logo_png3.jpg'

const Navbar = () => {
  return (
    <nav className="topbar">
      <a className="brand" href="#home">
        <img className="brand__mark" src={umeLogo} alt="UME Cambodia logo" />
        <span>
          <strong>University of Management and Economics</strong>
          <small>U.M.E Cambodia</small>
        </span>
      </a>

      <div className="nav-links">
        <a href="#programs">Programs</a>
        <a href="#about">About</a>
        <a href="#admissions">Admissions</a>
        <a href="#news">News</a>
        <a href="#contact">Contact</a>
      </div>

      <a className="button button--ghost" href="#admissions">
        Apply Now
      </a>
    </nav>
  )
}

export default Navbar
