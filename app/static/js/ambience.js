async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return await response.json();
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

function toMediaUrl(path) {
  return `/media/${path.replaceAll('\\', '/')}`;
}

function getFolderName() {
  const parts = window.location.pathname.split('/').filter(Boolean);
  return parts[1] || '';
}

function isTrackActive(state, folderName, trackTitle) {
  const targetName = `${folderName}/${trackTitle}`;
  return (state.active_ambience || []).some(layer => layer.name === targetName);
}

function renderTrackCard(folderName, track, active) {
  const card = document.createElement('button');
  card.className = active ? 'card card-active' : 'card';
  card.type = 'button';

  const title = document.createElement('div');
  title.className = 'title';
  title.textContent = track.title;

  const meta = document.createElement('div');
  meta.className = 'meta';
  meta.textContent = active ? 'Active ambience layer' : 'Toggle ambience layer';

  card.appendChild(title);
  card.appendChild(meta);

  card.addEventListener('click', async () => {
    await postJson('/api/ambience/toggle', {
      name: `${folderName}/${track.title}`,
      path: track.path,
    });
    await bootstrap();
  });

  return card;
}

function renderFolderHeader(folder) {
  const header = document.getElementById('folder-header');
  header.innerHTML = '';

  const wrapper = document.createElement('div');
  wrapper.className = 'folder-header-card';

  if (folder.thumbnail) {
    const image = document.createElement('img');
    image.className = 'folder-thumb';
    image.alt = folder.title;
    image.src = toMediaUrl(folder.thumbnail);
    wrapper.appendChild(image);
  }

  const title = document.createElement('div');
  title.className = 'folder-title';
  title.textContent = folder.title;

  const meta = document.createElement('div');
  meta.className = 'folder-meta';
  meta.textContent = `${folder.tracks?.length || 0} track(s)`;

  wrapper.appendChild(title);
  wrapper.appendChild(meta);
  header.appendChild(wrapper);
}

async function bootstrap() {
  const folderName = getFolderName();
  const [folder, state] = await Promise.all([
    fetchJson(`/api/library/ambience/${folderName}`),
    fetchJson('/api/state'),
  ]);

  document.getElementById('page-title').textContent = `${folder.title} ambience`;

  renderFolderHeader(folder);

  const tracks = document.getElementById('tracks');
  tracks.innerHTML = '';

  for (const track of folder.tracks || []) {
    tracks.appendChild(renderTrackCard(folder.title, track, isTrackActive(state, folder.title, track.title)));
  }
}

bootstrap().catch(error => {
  document.body.innerHTML = `<p>Failed to load ambience folder: ${error}</p>`;
});