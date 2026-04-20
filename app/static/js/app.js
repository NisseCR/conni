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

function isPlaylistActive(state, playlistTitle) {
  return state.current_playlist === playlistTitle;
}

function isAmbienceFolderActive(state, folderTitle) {
  return (state.active_ambience || []).some(layer =>
    layer.name.startsWith(`${folderTitle}/`)
  );
}

function renderPlaylistCard(item, state) {
  const card = document.createElement('button');
  card.className = isPlaylistActive(state, item.title) ? 'card card-active' : 'card';
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
  meta.textContent = isPlaylistActive(state, item.title) ? 'Current playlist' : 'Play playlist';

  card.appendChild(image);
  card.appendChild(title);
  card.appendChild(meta);

  card.addEventListener('click', async () => {
    await postJson('/api/play', { playlist_name: item.title });
    await loadState();
    await loadLibrary();
  });

  return card;
}

function renderAmbienceCard(item, state) {
  const card = document.createElement('a');
  card.className = isAmbienceFolderActive(state, item.title) ? 'card card-active' : 'card';
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
  meta.textContent = isAmbienceFolderActive(state, item.title)
    ? 'Active ambience folder'
    : `${item.tracks?.length || 0} track(s)`;

  card.appendChild(image);
  card.appendChild(title);
  card.appendChild(meta);

  return card;
}

async function loadLibrary() {
  const [data, state] = await Promise.all([
    fetchJson('/api/library'),
    fetchJson('/api/state'),
  ]);

  const playlists = document.getElementById('playlists');
  playlists.innerHTML = '';
  for (const item of data.playlists || []) {
    playlists.appendChild(renderPlaylistCard(item, state));
  }

  const ambience = document.getElementById('ambience');
  ambience.innerHTML = '';
  for (const item of data.ambience || []) {
    ambience.appendChild(renderAmbienceCard(item, state));
  }
}

async function loadState() {
  const state = await fetchJson('/api/state');
  document.getElementById('state').textContent = JSON.stringify(state, null, 2);
}

async function bootstrap() {
  try {
    await loadLibrary();
    await loadState();
  } catch (error) {
    document.getElementById('state').textContent = `Failed to load: ${error}`;
    return;
  }

  setInterval(async () => {
    try {
      await loadState();
      await loadLibrary();
    } catch (error) {
      console.warn('Refresh failed:', error);
    }
  }, 1000);
}
bootstrap();