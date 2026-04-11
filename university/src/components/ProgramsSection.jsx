const ProgramsSection = ({ programs }) => {
  return (
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
  )
}

export default ProgramsSection
