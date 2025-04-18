let day = 0;
function load() {
  document.getElementById('day-label').innerText =
    day===0 ? 'Today' : `${-day} days ago`;
  fetch(`/api/videos?day=${day}`)
    .then(r=>r.json())
    .then(data=>{
      const ul = document.getElementById('list'); ul.innerHTML='';
      data.forEach(v=>{
        const li = document.createElement('li');
        li.innerHTML = `
          <h3><a href="${v.url}" target="_blank">${v.title}</a></h3>
          <p>${v.views.toLocaleString()} views (<span class="performance">${v.performance_ratio}×</span>)</p>
        `;
        ul.appendChild(li);
      });
    });
}
function change(dir){ day = Math.max(0, day+dir); load(); }
window.onload = load;
