const AdmissionsSection = () => {
  return (
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
  )
}

export default AdmissionsSection
