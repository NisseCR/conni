async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return await response.json();
}

function toMediaUrl(path) {
  return `/media/${path.replaceAll('\\', '/')}`;
}


function renderCard(item, kind) {
  const card = document.createElement('div');
  card.className = 'card';

  const image = document.createElement('img');
  image.className = 'thumb';
  image.alt = item.title;

  if (item.thumbnail) {
    image.src = toMediaUrl(item.thumbnail);
  } else {
    image.style.display = 'none';
  }

  const title = document.createElement('div');
  title.className = 'title';
  title.textContent = item.title;

  const meta = document.createElement('div');
  meta.className = 'meta';
  meta.textContent = kind === 'playlist'
    ? item.path
    : `${item.tracks?.length || 0} ambience track(s)`;

  card.appendChild(image);
  card.appendChild(title);
  card.appendChild(meta);

  return card;
}

async function loadLibrary() {
  const data = await fetchJson('/api/library');

  const playlists = document.getElementById('playlists');
  playlists.innerHTML = '';
  for (const item of data.playlists || []) {
    playlists.appendChild(renderCard(item, 'playlist'));
  }

  const ambience = document.getElementById('ambience');
  ambience.innerHTML = '';
  for (const item of data.ambience || []) {
    ambience.appendChild(renderCard(item, 'ambience'));
  }
}

async function loadState() {
  const state = await fetchJson('/api/state');
  document.getElementById('state').textContent = JSON.stringify(state, null, 2);
}

async function bootstrap() {
  try {
    await Promise.all([loadLibrary(), loadState()]);
  } catch (error) {
    document.getElementById('state').textContent = `Failed to load: ${error}`;
  }
}

bootstrap();