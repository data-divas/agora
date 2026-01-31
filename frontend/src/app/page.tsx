export default function Home() {
  return (
    <div className="min-h-screen bg-[#0f1419] text-[#e8e6e3]">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/5 bg-[#0f1419]/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <a href="/" className="text-xl font-semibold tracking-tight">
            Agora
          </a>
          <div className="flex items-center gap-8">
            <a href="#how-it-works" className="text-sm text-[#9ca3af] hover:text-white transition-colors">
              How it works
            </a>
            <a href="#invest" className="text-sm text-[#9ca3af] hover:text-white transition-colors">
              Invest
            </a>
            <a
              href="#"
              className="rounded-full bg-[#e8a838] px-4 py-2 text-sm font-medium text-[#0f1419] hover:bg-[#c4902a] transition-colors"
            >
              Get started
            </a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-6 pt-20">
        {/* Grid background */}
        <div
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage: `
              linear-gradient(to right, #e8e6e3 1px, transparent 1px),
              linear-gradient(to bottom, #e8e6e3 1px, transparent 1px)
            `,
            backgroundSize: "64px 64px",
          }}
        />
        <div className="relative mx-auto max-w-4xl text-center">
          <p className="mb-4 text-sm font-medium uppercase tracking-widest text-[#e8a838]">
            Crowdfunding for Urban Transformation
          </p>
          <h1 className="mb-6 text-5xl font-bold leading-tight tracking-tight sm:text-6xl lg:text-7xl">
            Parking lots →
            <br />
            <span className="text-[#e8a838]">Third places</span>
          </h1>
          <p className="mx-auto mb-10 max-w-2xl text-lg leading-relaxed text-[#9ca3af]">
            Invest in the transformation of underutilized parking into parks, popups, and community spaces.
            Retail investors. Real impact. Shared ownership.
          </p>
          <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
            <a
              href="#"
              className="rounded-full bg-[#e8a838] px-8 py-4 text-base font-semibold text-[#0f1419] hover:bg-[#c4902a] transition-colors"
            >
              Explore projects
            </a>
            <a
              href="#how-it-works"
              className="rounded-full border border-white/20 px-8 py-4 text-base font-medium hover:border-white/40 hover:bg-white/5 transition-colors"
            >
              Learn more
            </a>
          </div>
        </div>
      </section>

      {/* Value props */}
      <section className="border-t border-white/5 py-24">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid gap-12 md:grid-cols-3">
            <div className="rounded-2xl border border-white/5 bg-[#1a1f26]/50 p-8">
              <div className="mb-4 text-2xl">🏛️</div>
              <h3 className="mb-2 text-lg font-semibold">Crowdfunding</h3>
              <p className="text-[#9ca3af]">
                Community-funded projects. Every dollar goes toward turning concrete into gathering spaces.
              </p>
            </div>
            <div className="rounded-2xl border border-white/5 bg-[#1a1f26]/50 p-8">
              <div className="mb-4 text-2xl">👥</div>
              <h3 className="mb-2 text-lg font-semibold">Retail investors</h3>
              <p className="text-[#9ca3af]">
                Anyone can invest. No accredited investor gatekeeping. Build the places you want to see.
              </p>
            </div>
            <div className="rounded-2xl border border-white/5 bg-[#1a1f26]/50 p-8">
              <div className="mb-4 text-2xl">🌳</div>
              <h3 className="mb-2 text-lg font-semibold">Third places</h3>
              <p className="text-[#9ca3af]">
                Cafés, plazas, parks. Not home, not work—spaces where community happens.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="border-t border-white/5 py-24">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="mb-16 text-center text-3xl font-bold">How it works</h2>
          <div className="grid gap-8 md:grid-cols-4">
            {[
              { step: "01", title: "Identify", desc: "We find underutilized parking lots ripe for transformation." },
              { step: "02", title: "Design", desc: "Community input shapes each project—parks, plazas, markets." },
              { step: "03", title: "Fund", desc: "Retail investors crowdfund the build. You own a piece." },
              { step: "04", title: "Transform", desc: "Concrete becomes community. Revenue flows back to investors." },
            ].map((item) => (
              <div key={item.step}>
                <span className="text-4xl font-bold text-[#e8a838]/30">{item.step}</span>
                <h3 className="mt-2 text-lg font-semibold">{item.title}</h3>
                <p className="mt-2 text-[#9ca3af]">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="border-t border-white/5 py-24">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="mb-4 text-3xl font-bold">Ready to invest in your neighborhood?</h2>
          <p className="mb-8 text-[#9ca3af]">
            Join thousands of retail investors transforming parking lots into places people actually want to be.
          </p>
          <a
            href="#"
            className="inline-block rounded-full bg-[#e8a838] px-8 py-4 text-base font-semibold text-[#0f1419] hover:bg-[#c4902a] transition-colors"
          >
            Get started
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-12">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-6 px-6 sm:flex-row">
          <span className="font-semibold">Agora</span>
          <div className="flex gap-8 text-sm text-[#9ca3af]">
            <a href="#" className="hover:text-white transition-colors">About</a>
            <a href="#" className="hover:text-white transition-colors">Projects</a>
            <a href="#" className="hover:text-white transition-colors">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
