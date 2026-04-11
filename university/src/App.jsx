import AboutSection from './components/AboutSection'
import AdmissionsSection from './components/AdmissionsSection'
import ContactSection from './components/ContactSection'
import Footer from './components/Footer'
import HeroSection from './components/HeroSection'
import Navbar from './components/Navbar'
import NewsSection from './components/NewsSection'
import ProgramsSection from './components/ProgramsSection'
import { highlights, news, outcomes, programs, stats } from './data/siteContent'

const App = () => {
  return (
    <div className="site-shell">
      <HeroSection highlights={highlights} stats={stats}>
        <Navbar />
      </HeroSection>

      <main>
        <AboutSection outcomes={outcomes} />
        <ProgramsSection programs={programs} />
        <AdmissionsSection />
        <NewsSection news={news} />
        <ContactSection />
      </main>

      <Footer />
    </div>
  )
}

export default App

