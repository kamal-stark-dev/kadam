import AppShell from '../components/AppShell'

export default function HomePage() {
  return (
    <AppShell>
      <section>
        <p className="text-sm font-medium uppercase tracking-widest text-indigo-600">
          Kadam
        </p>
        <h1 className="mt-3 text-4xl font-bold tracking-tight sm:text-5xl">
          Frontend scaffold ready.
        </h1>
        <p className="mt-4 max-w-xl text-lg text-slate-600">
          Build pages in <code>src/pages</code>, reusable UI in{' '}
          <code>src/components</code>, and browser-facing utilities in{' '}
          <code>src/lib</code>.
        </p>
      </section>
    </AppShell>
  )
}
