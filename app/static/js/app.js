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

async function postJson(url, data) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return await response.json();
}

function renderPlaylistCard(item) {
  const card = document.createElement('button');
  card.className = 'card';
  card.type = 'button';

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
  meta.textContent = 'Play playlist';

  card.appendChild(image);
  card.appendChild(title);
  card.appendChild(meta);

  card.addEventListener('click', async () => {
    await postJson('/api/play', { playlist_name: item.title });
    await loadState();
  });

  return card;
}

function renderAmbienceCard(item) {
  const card = document.createElement('a');
  card.className = 'card';
  card.href = `/ambience/${item.title}`;
  card.style.textDecoration = 'none';
  card.style.color = 'inherit';

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
  meta.textContent = `${item.tracks?.length || 0} track(s)`;

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
    playlists.appendChild(renderPlaylistCard(item));
  }

  const ambience = document.getElementById('ambience');
  ambience.innerHTML = '';
  for (const item of data.ambience || []) {
    ambience.appendChild(renderAmbienceCard(item));
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