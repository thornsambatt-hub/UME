

import umeLogo from './components/UME_Logo_png3.jpg'

const stats = [
  { value: '18K+', label: 'students across undergraduate and postgraduate programs' },
  { value: '120+', label: 'industry and exchange partners in Asia, Europe, and the US' },
  { value: '92%', label: 'graduate employment or further study within six months' },
]

const programs = [
  {
    title: 'Business & Innovation',
    description:
      'Modern management, entrepreneurship, and global finance programs designed around live consulting projects.',
  },
  {
    title: 'Engineering & Computing',
    description:
      'Practice-led study in AI, software engineering, data systems, and sustainable infrastructure.',
  },
  {
    title: 'Health & Life Sciences',
    description:
      'Interdisciplinary pathways in public health, biomedical science, and community-centered research.',
  },
  {
    title: 'Design, Media & Humanities',
    description:
      'Creative and critical programs that blend communication, digital design, culture, and policy.',
  },
]

const highlights = [
  'International foundation, undergraduate, and postgraduate pathways',
  'Scholarships for academic excellence, leadership, and social impact',
  'Hybrid campus model with research labs, startup studios, and global classrooms',
]

const outcomes = [
  {
    title: 'Career-Ready Learning',
    text: 'Every degree includes internships, employer briefs, or capstone projects aligned with real-world practice.',
  },
  {
    title: 'Global Mobility',
    text: 'Students can study abroad, join visiting faculty seminars, and work on collaborative international challenges.',
  },
  {
    title: 'Research With Purpose',
    text: 'Faculty and students focus on applied research in sustainability, digital transformation, and public wellbeing.',
  },
]

const news = [
  {
    category: 'Research',
    title: 'Smart city lab launches new urban resilience initiative',
    text: 'A cross-faculty team is developing data-driven planning models with regional government and industry partners.',
  },
  {
    category: 'Student Life',
    title: 'New makerspace opens for prototyping and digital fabrication',
    text: 'The campus hub brings together robotics, product design, and creative technology under one roof.',
  },
  {
    category: 'Admissions',
    title: 'Applications now open for the next international intake',
    text: 'Prospective students can book virtual advising sessions and scholarship consultations with the admissions team.',
  },
]

const App = () => {
  return (
    <div className="site-shell">
      <header className="hero">
        <div className="hero__glow hero__glow--one" />
        <div className="hero__glow hero__glow--two" />

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

      <main>
        <section className="section section--light" id="about">
          <div className="section-heading">
            <p className="eyebrow">About The University</p>
            <h2>Academic excellence with an international perspective.</h2>
            <p>
              The university is designed around interdisciplinary learning,
              professional readiness, and meaningful collaboration with industry,
              government, and community partners.
            </p>
          </div>

          <div className="grid grid--3">
            {outcomes.map((item) => (
              <article className="info-card" key={item.title}>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="section" id="programs">
          <div className="section-heading">
            <p className="eyebrow">Study Areas</p>
            <h2>Programs aligned with future industries.</h2>
            <p>
              Each faculty combines strong academic foundations with applied
              learning, international exposure, and mentorship from practitioners.
            </p>
          </div>

          <div className="grid grid--2">
            {programs.map((program) => (
              <article className="program-card" key={program.title}>
                <h3>{program.title}</h3>
                <p>{program.description}</p>
                <a href="#contact">Request curriculum details</a>
              </article>
            ))}
          </div>
        </section>

        <section className="section section--feature" id="admissions">
          <div className="feature-layout">
            <div>
              <p className="eyebrow">Admissions</p>
              <h2>A clear pathway from application to enrollment.</h2>
              <p className="feature-copy">
                The admissions process is designed to be fast, transparent, and
                supportive for local and international applicants.
              </p>
            </div>

            <div className="timeline">
              <article>
                <span>01</span>
                <div>
                  <h3>Submit your application</h3>
                  <p>Send academic records, language qualifications, and your preferred intake.</p>
                </div>
              </article>
              <article>
                <span>02</span>
                <div>
                  <h3>Meet an advisor</h3>
                  <p>Receive guidance on program fit, scholarships, visas, and accommodation options.</p>
                </div>
              </article>
              <article>
                <span>03</span>
                <div>
                  <h3>Join the university</h3>
                  <p>Complete enrollment, orientation, and onboarding into your faculty community.</p>
                </div>
              </article>
            </div>
          </div>
        </section>

        <section className="section section--light" id="news">
          <div className="section-heading">
            <p className="eyebrow">Latest Updates</p>
            <h2>Campus stories, research, and upcoming opportunities.</h2>
          </div>

          <div className="grid grid--3">
            {news.map((item) => (
              <article className="news-card" key={item.title}>
                <span>{item.category}</span>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="section section--contact" id="contact">
          <div className="contact-card">
            <div>
              <p className="eyebrow">Contact & Visit</p>
              <h2>Start your application conversation.</h2>
              <p>
                Connect with admissions, schedule a campus visit, or request a
                personalized consultation for international study pathways.
              </p>
            </div>

            <div className="contact-details">
              <p><strong>Email:</strong> admissions@universitasinternational.edu</p>
              <p><strong>Phone:</strong> +62 21 5555 2026</p>
              <p><strong>Location:</strong> Global Academic District, Jakarta</p>
            </div>
          </div>
        </section>
      </main>

      <footer className="footer">
        <p>© 2026 University of Management and Economics. Professional education for global futures.</p>
      </footer>
    </div>
  )
}

export default App
