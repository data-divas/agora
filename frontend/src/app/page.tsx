export default function Home() {
  return (
    <div className="min-h-screen bg-[#FAFAFA] overflow-x-hidden">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-black/5 bg-[#FAFAFA]/95 backdrop-blur-sm">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-5">
          <a href="/" className="text-lg font-medium text-[#1a1a1a]">
            Agora
          </a>
          <div className="flex items-center gap-10">
            <a href="#how-it-works" className="text-sm text-[#6b7280] hover:text-[#1a1a1a] transition-colors">
              How it works
            </a>
            <a href="/discover" className="text-sm text-[#6b7280] hover:text-[#1a1a1a] transition-colors">
              Discover
            </a>
            <a
              href="#"
              className="rounded-lg bg-agora-medium px-4 py-2 text-sm font-medium text-white hover:bg-agora-dark transition-colors"
            >
              Get started
            </a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative px-6 pt-32 pb-24">
        {/* Background orbs */}
        <div className="pointer-events-none absolute inset-0 overflow-hidden">
          <div
            className="absolute -right-40 -top-20 h-96 w-96 rounded-full bg-agora-light/40 blur-3xl animate-float"
            aria-hidden
          />
          <div
            className="absolute right-1/4 top-1/2 h-64 w-64 rounded-full bg-agora-medium/20 blur-3xl animate-float"
            aria-hidden
            style={{ animationDelay: "-4s" }}
          />
          <div
            className="absolute -left-20 top-1/3 h-72 w-72 rounded-full bg-agora-light/30 blur-3xl animate-float"
            aria-hidden
            style={{ animationDelay: "-2s" }}
          />
        </div>

        <div className="relative mx-auto max-w-5xl flex flex-col lg:flex-row lg:items-center lg:justify-between lg:gap-16">
          <div className="max-w-2xl animate-fade-up">
            <p className="mb-3 text-sm italic text-[#6b7280]">
              Crowdfunding for urban transformation
            </p>
            <h1 className="font-serif text-4xl font-semibold leading-tight text-[#1a1a1a] sm:text-5xl">
              Parking lots become third places.
            </h1>
            <p className="mt-6 max-w-lg text-lg leading-relaxed text-[#6b7280]">
              Invest in the transformation of underutilized parking into parks, plazas, and community spaces. Retail investors. Real impact. Shared ownership.
            </p>
            <a
              href="#"
              className="mt-10 inline-block rounded-lg bg-agora-medium px-6 py-3 text-base font-medium text-white hover:bg-agora-dark transition-colors"
            >
              Explore projects
            </a>
          </div>

          {/* Abstract geometric graphic */}
          <div
            className="relative mt-16 lg:mt-0 lg:min-w-[380px] lg:max-w-[420px] aspect-[4/3] animate-fade-up"
            style={{ animationDelay: "0.15s" }}
          >
            <svg
              viewBox="0 0 400 300"
              fill="none"
              className="w-full h-full"
              aria-hidden
            >
              {/* Grid/urban base (parking lot feel) */}
              <rect x="40" y="180" width="120" height="80" rx="4" fill="#13714C" fillOpacity="0.15" transform="rotate(-2 100 220)" />
              <rect x="180" y="160" width="100" height="100" rx="4" fill="#13714C" fillOpacity="0.1" transform="rotate(3 230 210)" />
              <rect x="260" y="140" width="80" height="120" rx="4" fill="#3AB67D" fillOpacity="0.2" transform="rotate(-4 300 200)" />
              {/* Overlapping shapes - transformation */}
              <rect x="80" y="60" width="140" height="100" rx="8" fill="#A2E494" fillOpacity="0.6" transform="rotate(-8 150 110)" />
              <rect x="140" y="80" width="120" height="90" rx="8" fill="#3AB67D" fillOpacity="0.5" transform="rotate(6 200 125)" />
              <rect x="200" y="50" width="100" height="110" rx="8" fill="#13714C" fillOpacity="0.35" transform="rotate(-3 250 105)" />
              <rect x="250" y="90" width="90" height="80" rx="8" fill="#A2E494" fillOpacity="0.5" transform="rotate(5 295 130)" />
            </svg>
          </div>
        </div>
      </section>

      {/* Value props */}
      <section className="relative border-t border-black/5 bg-white py-20">
        <div className="mx-auto max-w-5xl px-6">
          <div className="grid gap-16 md:grid-cols-3">
            {[
              { title: "Crowdfunding", desc: "Community-funded projects. Every dollar turns concrete into gathering spaces." },
              { title: "Retail investors", desc: "Anyone can invest. No accredited investor gatekeeping." },
              { title: "Third places", desc: "Cafés, plazas, parks. Not home, not work—spaces where community happens." },
            ].map((item, i) => (
              <div
                key={item.title}
                className="group rounded-2xl border border-black/5 bg-[#FAFAFA]/50 p-8 transition-all duration-300 hover:border-agora-medium/30 hover:shadow-lg hover:shadow-agora-light/20"
                style={{ animationDelay: `${i * 0.1}s` }}
              >
                <div className="mb-4 h-10 w-10 rounded-xl bg-gradient-to-br from-agora-light to-agora-medium opacity-80 group-hover:opacity-100 transition-opacity" />
                <h3 className="text-base font-medium text-[#1a1a1a]">{item.title}</h3>
                <p className="mt-2 text-[#6b7280] leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="relative border-t border-black/5 py-20 overflow-hidden">
        {/* Subtle gradient accent */}
        <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-agora-medium/30 to-transparent" />
        <div className="mx-auto max-w-5xl px-6">
          <h2 className="text-xl font-medium text-[#1a1a1a]">How it works</h2>
          <div className="mt-10 grid gap-8 sm:grid-cols-4 sm:gap-4">
            {[
              { title: "Identify", desc: "Find underutilized parking lots." },
              { title: "Design", desc: "Community shapes each project." },
              { title: "Fund", desc: "Investors crowdfund. You own a piece." },
              { title: "Transform", desc: "Concrete becomes community." },
            ].map((item, i) => (
              <div key={item.title} className="flex items-start gap-4">
                <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-agora-light/60 text-sm font-medium text-agora-dark">
                  {i + 1}
                </span>
                <div>
                  <h3 className="text-base font-medium text-[#1a1a1a]">{item.title}</h3>
                  <p className="mt-1 text-[#6b7280] text-sm">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-black/5 py-8">
        <div className="mx-auto flex max-w-5xl flex-col items-center justify-between gap-4 px-6 sm:flex-row">
          <span className="text-sm font-medium text-[#1a1a1a]">Agora</span>
          <div className="flex gap-8 text-sm text-[#6b7280]">
            <a href="#" className="hover:text-[#1a1a1a] transition-colors">About</a>
            <a href="#" className="hover:text-[#1a1a1a] transition-colors">Projects</a>
            <a href="#" className="hover:text-[#1a1a1a] transition-colors">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  )
}
