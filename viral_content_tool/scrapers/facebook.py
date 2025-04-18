import random, time
from datetime import datetime, timedelta

def collect_facebook_videos(days=7, count=20):
    vids = []
    base_avg = 50000
    for i in range(count):
        post = datetime.now() - timedelta(days=random.random()*days)
        views = int(base_avg * random.uniform(1, 10))
        vids.append({
            'id': f'fb{i}',
            'platform': 'facebook',
            'title': f'Facebook Reel {i}',
            'url': 'https://facebook.com',
            'thumbnail': '',
            'views': views,
            'performance_ratio': round(views/base_avg,1),
            'post_date': post.isoformat(),
        })
    return [v for v in vids if v['performance_ratio']>=2.0]
