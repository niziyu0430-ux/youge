const revisedPortraits = new Set(['practice_seeker', 'style_director']);

export function portraitFor(persona) {
  const suffix = revisedPortraits.has(persona.id) ? '-r2' : '';
  return `/assets/personas-v2/${persona.id}${suffix}.png`;
}

export function ribbonPortraitFor(persona) { return `/assets/personas-ribbon/v2/${persona.id}.webp`; }
export function heroPortraitFor(persona) { return `/assets/personas-hero/v2/${persona.id}.webp`; }
export function styledPersona(persona) { return {...persona, portrait: portraitFor(persona)}; }
export function styledReport(report) { return {...report, persona: styledPersona(report.persona)}; }
