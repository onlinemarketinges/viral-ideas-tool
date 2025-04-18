from flask import Flask, render_template, request, jsonify
import sqlite3, os
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from scrapers.instagram import collect_instagram_videos
from scrapers.youtube import collect_youtube_videos
from scrapers.tiktok import collect_tiktok_videos
from scrapers.facebook import collect_facebook_videos

# Paths
db_path = os.path.join(os.path.dirname(__file__), 'data', 'videos.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Initialize DB
def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
      CREATE TABLE IF NOT EXISTS videos (
        id TEXT PRIMARY KEY,
        platform TEXT,
        title TEXT,
        url TEXT,
        thumbnail TEXT,
        views INTEGER,
        performance_ratio REAL,
        post_date TEXT,
        date_collected TEXT
      )
    ''')
    conn.commit()
    conn.close()

# Collect and store top 10 viral videos per day
def collect_and_store():
    today = datetime.now().date().isoformat()
    vids = []
    vids += collect_instagram_videos(days=7)
    vids += collect_youtube_videos(days=7)
    vids += collect_tiktok_videos(days=7)
    vids += collect_facebook_videos(days=7)
    vids.sort(key=lambda v: v['performance_ratio'], reverse=True)
    top10 = vids[:10]
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for v in top10:
        c.execute('''INSERT OR REPLACE INTO videos VALUES (?,?,?,?,?,?,?,?,?)''', (
            v['id'], v['platform'], v['title'], v['url'],
            v['thumbnail'], v['views'], v['performance_ratio'],
            v['post_date'], today
        ))
    conn.commit()
    conn.close()

# Flask setup
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/videos')
def api_videos():
    day = request.args.get('day', '0')
    target = (datetime.now() - timedelta(days=int(day))).date().isoformat()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM videos WHERE date_collected=? ORDER BY performance_ratio DESC LIMIT 10', (target,))
    cols = [d[0] for d in c.description]
    data = [dict(zip(cols,row)) for row in c.fetchall()]
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_and_store, 'cron', hour=0, minute=0)
    scheduler.start()
    collect_and_store()
    app.run(host='0.0.0.0', port=8000)
