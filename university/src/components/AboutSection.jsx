const AboutSection = ({ outcomes }) => {
  return (
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
  )
}

export default AboutSection
