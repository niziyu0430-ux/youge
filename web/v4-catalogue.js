/** Offline name lookup. Edition IDs remain separate even when aliases overlap. */
export function normalizeGameQuery(value) {
  return String(value ?? '').replace(/[™®©]/gu, '').normalize('NFKC').toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, '');
}

export function createGameIndex(games) {
  return games.map((game, order) => ({
    game, order,
    title: normalizeGameQuery(game.title),
    original: normalizeGameQuery(game.original_title),
    terms: [...new Set([game.title, game.original_title, ...(game.aliases || [])]
      .map(normalizeGameQuery).filter(Boolean))],
  }));
}

export function searchGames(index, query = '', {category = '', featured = []} = {}) {
  const needle = normalizeGameQuery(query);
  const words = String(query).trim().split(/\s+/u).map(normalizeGameQuery).filter(Boolean);
  const shortLatin = /^[a-z0-9]{1,3}$/u.test(needle);
  const featuredOrder = new Map(featured.map((id, position) => [id, position]));
  const results = [];
  for (const item of index) {
    if (category && !item.game.category_ids.includes(category)) continue;
    let score = 0;
    if (needle) {
      if (item.title === needle) score = 1000;
      else if (item.original === needle) score = 980;
      else if (item.terms.includes(needle)) score = 960;
      else if (item.terms.some(term => term.startsWith(needle))) score = 850;
      else if (!shortLatin && item.terms.some(term => term.includes(needle))) score = 750;
      else if (words.length > 1 && words.every(word => word.length >= 3) &&
               words.every(word => item.terms.some(term => term.includes(word)))) score = 650;
      else continue;
    }
    results.push({...item, score});
  }
  results.sort((a, b) => b.score - a.score ||
    (featuredOrder.get(a.game.id) ?? Number.MAX_SAFE_INTEGER) -
      (featuredOrder.get(b.game.id) ?? Number.MAX_SAFE_INTEGER) || a.order - b.order);
  return results.map(item => item.game);
}
