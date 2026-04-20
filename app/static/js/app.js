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
    await refreshAll();
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

function bindSliderScrollAdjust(slider) {
  slider.addEventListener('wheel', (event) => {
    event.preventDefault();

    const step = Number(slider.step || 0.01);
    const sensitivity = 4;
    const delta = event.deltaY < 0 ? step * sensitivity : -step * sensitivity;
    const nextValue = Math.max(
      Number(slider.min || 0),
      Math.min(Number(slider.max || 1), Number(slider.value) + delta),
    );

    slider.value = String(nextValue);
    slider.dispatchEvent(new Event('input', { bubbles: true }));
  }, { passive: false });
}

function createVolumeSlider(id, target, value) {
  const slider = document.createElement('input');
  slider.id = id;
  slider.type = 'range';
  slider.min = '0';
  slider.max = '1';
  slider.step = '0.01';
  slider.value = value ?? 1.0;

  bindSliderScrollAdjust(slider);

  slider.addEventListener('input', async () => {
    await postJson('/api/volume', {
      target,
      value: Number(slider.value),
    });
  });

  return slider;
}

function renderSidebar(state) {
  const sidebar = document.getElementById('sidebar-content');
  sidebar.innerHTML = '';

  const nowPlaying = document.createElement('section');
  nowPlaying.className = 'sidebar-section';

  const nowPlayingTitle = document.createElement('h2');
  nowPlayingTitle.textContent = 'Now Playing';

  const playlistLabel = document.createElement('div');
  playlistLabel.className = 'panel-label';
  playlistLabel.textContent = 'Playlist';

  const playlistValue = document.createElement('div');
  playlistValue.className = 'panel-value';
  playlistValue.textContent = state.current_playlist || 'None';

  const trackLabel = document.createElement('div');
  trackLabel.className = 'panel-label';
  trackLabel.textContent = 'Current Track';

  const trackValue = document.createElement('div');
  trackValue.className = 'panel-value';
  trackValue.textContent = state.current_track_title || 'None';

  nowPlaying.appendChild(nowPlayingTitle);
  nowPlaying.appendChild(playlistLabel);
  nowPlaying.appendChild(playlistValue);
  nowPlaying.appendChild(trackLabel);
  nowPlaying.appendChild(trackValue);

  const musicSection = document.createElement('section');
  musicSection.className = 'sidebar-section';

  const musicTitle = document.createElement('h2');
  musicTitle.textContent = 'Music Volume';

  const musicLabel = document.createElement('div');
  musicLabel.className = 'panel-label';
  musicLabel.textContent = 'Music';

  const musicSlider = createVolumeSlider('music-volume', 'music', state.music_volume);

  musicSection.appendChild(musicTitle);
  musicSection.appendChild(musicLabel);
  musicSection.appendChild(musicSlider);

  const masterSection = document.createElement('section');
  masterSection.className = 'sidebar-section';

  const masterTitle = document.createElement('h2');
  masterTitle.textContent = 'Master Volume';

  const masterLabel = document.createElement('div');
  masterLabel.className = 'panel-label';
  masterLabel.textContent = 'Master';

  const masterSlider = createVolumeSlider('master-volume', 'master', state.master_volume);

  masterSection.appendChild(masterTitle);
  masterSection.appendChild(masterLabel);
  masterSection.appendChild(masterSlider);

  const ambienceSection = document.createElement('section');
  ambienceSection.className = 'sidebar-section';

  const ambienceTitle = document.createElement('h2');
  ambienceTitle.textContent = 'Active Ambience';

  const ambienceList = document.createElement('div');
  ambienceList.id = 'active-ambience';
  ambienceList.className = 'sidebar-list';

  for (const layer of state.active_ambience || []) {
    const row = document.createElement('div');
    row.className = 'sidebar-item';

    const label = document.createElement('div');
    label.className = 'sidebar-item-title';
    label.textContent = layer.name;

    const slider = createVolumeSlider(`ambience-${layer.name}`, 'ambience', layer.volume ?? 1.0);

    slider.addEventListener('input', async () => {
      await postJson('/api/volume', {
        target: 'ambience',
        ambience_name: layer.name,
        value: Number(slider.value),
      });
    });

    row.appendChild(label);
    row.appendChild(slider);
    ambienceList.appendChild(row);
  }

  ambienceSection.appendChild(ambienceTitle);
  ambienceSection.appendChild(ambienceList);

  sidebar.appendChild(nowPlaying);
  sidebar.appendChild(musicSection);
  sidebar.appendChild(masterSection);
  sidebar.appendChild(ambienceSection);
}

async function loadLibrary() {
  const data = await fetchJson('/api/library');
  const state = await fetchJson('/api/state');

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
  renderSidebar(state);
}

async function refreshAll() {
  await Promise.all([loadLibrary(), loadState()]);
}

async function bootstrap() {
  try {
    await refreshAll();
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