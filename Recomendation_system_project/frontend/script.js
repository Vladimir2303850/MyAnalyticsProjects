const API_URL = "http://127.0.0.1:8000";
let currentUserId = 1; // можно сделать авторизацию позже

async function login() {
  const username = document.getElementById("username").value;
  if (!username) return alert("Введите имя пользователя");

  // простая имитация входа — создаём пользователя
  const res = await fetch(`${API_URL}/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password: "12345" })
  });
  const data = await res.json();
  currentUserId = data.user_id || 1;
  alert(`Вход выполнен как ${username}`);
  loadMovies();
}

async function loadMovies() {
  const res = await fetch(`${API_URL}/movies`);
  const movies = await res.json();

  const container = document.getElementById("movies");
  container.innerHTML = "";
  movies.forEach(m => {
    const div = document.createElement("div");
    div.className = "movie";
    div.innerHTML = `${m.title} (${m.genre}, ${m.year})
      <button onclick="rateMovie(${m.movie_id}, 5)">⭐ 5</button>
      <button onclick="rateMovie(${m.movie_id}, 4)">👍 4</button>`;
    container.appendChild(div);
  });
}

async function rateMovie(movieId, rating) {
  await fetch(`${API_URL}/ratings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: currentUserId, movie_id: movieId, rating })
  });
  alert(`Фильм ${movieId} оценён на ${rating}`);
}

async function getRecommendations() {
  const res = await fetch(`${API_URL}/recommendations/${currentUserId}`);
  const data = await res.json();

  const container = document.getElementById("recommendations");
  container.innerHTML = "";
  if (data.message) {
    container.innerHTML = `<p>${data.message}</p>`;
  } else {
    data.forEach(m => {
      const div = document.createElement("div");
      div.className = "movie";
      div.textContent = `${m.title} (${m.genre}, ${m.year})`;
      container.appendChild(div);
    });
  }
}
