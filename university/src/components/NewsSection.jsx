const NewsSection = ({ news }) => {
  return (
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
  )
}

export default NewsSection
