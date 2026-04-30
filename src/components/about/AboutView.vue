<template>
  <section class="about-view">
    <article class="about-hero">
      <div class="hero-copy">
        <span class="eyebrow">About SubTrack</span>
        <h2>Recurring payment management, designed to stay readable.</h2>
        <p>
          SubTrack centralizes renewals, account controls, spending caps, and
          archived history so recurring expenses stay visible without forcing
          users to reconstruct timelines manually.
        </p>
      </div>

      <div class="hero-metrics">
        <div class="metric-card">
          <strong>Calendar-first</strong>
          <span>Recurring schedules are rendered as actual occurrences, not one-off dates.</span>
        </div>
        <div class="metric-card">
          <strong>Cap-aware</strong>
          <span>Soft and hard limits help prevent overspending before it compounds.</span>
        </div>
        <div class="metric-card">
          <strong>History-safe</strong>
          <span>Deleted subscriptions remain visible in archive views instead of disappearing outright.</span>
        </div>
      </div>
    </article>

    <article class="team-card">
      <div class="team-header">
        <span class="eyebrow">Development Team</span>
        <h3>Built across frontend, backend, and database workstreams.</h3>
      </div>

      <div class="team-grid">
        <article class="team-member">
          <span class="member-role">Database</span>
          <h4>De Los Reyes, Xian Humphrey S.</h4>
          <p>Database structure, persistence layer support, and schema-side implementation.</p>
        </article>

        <article class="team-member">
          <span class="member-role">Frontend</span>
          <h4>Jacob, John Paul A.</h4>
          <p>Frontend interface implementation, interaction flows, and presentation layer delivery.</p>
        </article>

        <article class="team-member featured">
          <span class="member-role">Backend</span>
          <h4>Pavia, Karl Austin B.</h4>
          <p>Backend integration, API behavior, and application flow coordination.</p>
        </article>
      </div>
    </article>
  </section>
</template>

<style scoped>
.about-view {
  display: grid;
  gap: 26px;
  padding-bottom: 24px;
}

.about-hero,
.team-card {
  border-radius: 30px;
  overflow: hidden;
  border: 1px solid var(--app-border);
  box-shadow: var(--app-shadow-soft);
}

.about-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.3fr) minmax(320px, 0.9fr);
  background:
    linear-gradient(135deg, rgba(0, 77, 38, 0.95), rgba(13, 106, 69, 0.9)),
    var(--app-surface);
  color: #f6fbf8;
}

.hero-copy {
  padding: 34px 34px 38px;
}

.eyebrow {
  display: inline-block;
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  margin-bottom: 16px;
}

.hero-copy .eyebrow {
  color: rgba(246, 251, 248, 0.66);
}

.hero-copy h2 {
  font-size: clamp(2rem, 3vw, 3rem);
  line-height: 1;
  letter-spacing: -0.04em;
}

.hero-copy p {
  max-width: 720px;
  margin-top: 18px;
  font-size: 1rem;
  line-height: 1.8;
  color: rgba(246, 251, 248, 0.86);
}

.hero-metrics {
  display: grid;
  gap: 1px;
  background: rgba(255, 255, 255, 0.14);
}

.metric-card {
  padding: 28px 26px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
}

.metric-card strong {
  display: block;
  font-size: 1rem;
  margin-bottom: 8px;
}

.metric-card span {
  font-size: 0.9rem;
  line-height: 1.7;
  color: rgba(246, 251, 248, 0.82);
}

.team-card {
  background: var(--app-surface);
  padding: 30px;
}

.team-header .eyebrow {
  color: var(--app-text-muted);
}

.team-header h3 {
  color: var(--app-heading);
  font-size: clamp(1.7rem, 2.4vw, 2.4rem);
  line-height: 1.06;
  letter-spacing: -0.03em;
  max-width: 760px;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 26px;
}

.team-member {
  border-radius: 22px;
  padding: 22px 20px;
  background: linear-gradient(180deg, var(--app-surface-alt) 0%, var(--app-surface) 100%);
  border: 1px solid color-mix(in srgb, var(--app-border) 90%, transparent);
}

.team-member.featured {
  background:
    radial-gradient(circle at top right, rgba(13, 106, 69, 0.14), transparent 26%),
    linear-gradient(180deg, color-mix(in srgb, var(--app-accent) 10%, var(--app-surface)) 0%, var(--app-surface) 100%);
}

.member-role {
  display: inline-flex;
  padding: 7px 12px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--app-accent) 14%, var(--app-surface));
  color: var(--app-accent);
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.team-member h4 {
  margin-top: 18px;
  color: var(--app-text);
  font-size: 1.08rem;
  line-height: 1.4;
}

.team-member p {
  margin-top: 10px;
  color: var(--app-text-muted);
  line-height: 1.72;
  font-size: 0.9rem;
}

@media (max-width: 1024px) {
  .about-hero {
    grid-template-columns: 1fr;
  }

  .team-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {
  .hero-copy,
  .team-card {
    padding: 22px 18px;
  }

  .metric-card {
    padding: 22px 18px;
  }
}
</style>
