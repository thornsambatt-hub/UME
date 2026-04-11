const HeroSection = ({ children, highlights, stats }) => {
  return (
    <header className="hero">
      <div className="hero__glow hero__glow--one" />
      <div className="hero__glow hero__glow--two" />
      {children}

      <section className="hero__content" id="home">
        <div className="hero__copy">
          <p className="eyebrow">International University Website</p>
          <h1>Professional education built for a connected world.</h1>
          <p className="hero__lead">
            Universitas International combines academic rigor, global partnerships,
            and career-focused learning to prepare students for leadership across
            industries and borders.
          </p>

          <div className="hero__actions">
            <a className="button" href="#programs">
              Explore Programs
            </a>
            <a className="button button--secondary" href="#contact">
              Book a Consultation
            </a>
          </div>

          <ul className="hero__list">
            {highlights.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="hero__panel">
          <div className="hero-card hero-card--accent">
            <span>2026 Intake</span>
            <strong>Admissions & Scholarships Open</strong>
            <p>Application review in 7 working days for selected programs.</p>
          </div>

          <div className="hero-card">
            <span>Campus Snapshot</span>
            <strong>Ranked for employability and industry engagement</strong>
            <p>Built for ambitious students seeking a modern international learning environment.</p>
          </div>
        </div>
      </section>

      <section className="stats">
        {stats.map((stat) => (
          <article className="stat-card" key={stat.label}>
            <h2>{stat.value}</h2>
            <p>{stat.label}</p>
          </article>
        ))}
      </section>
    </header>
  )
}

export default HeroSection
