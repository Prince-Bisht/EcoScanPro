import time,feedparser
_cache={'at':0,'items':[]}
URL='https://news.google.com/rss/search?q=waste+management+recycling+India&hl=en-IN&gl=IN&ceid=IN:en'
def get_news(ttl=1800):
    if time.time()-_cache['at']<ttl: return {'articles':_cache['items'],'cached':True}
    try:
        feed=feedparser.parse(URL,request_headers={'User-Agent':'EcoScanPro/1.0'})
        if getattr(feed,'bozo',False) and not feed.entries: raise RuntimeError('Feed unavailable')
        items=[]
        for e in feed.entries[:9]:
            items.append({'title':e.get('title','Untitled'),'source':e.get('source',{}).get('title','Google News RSS'),'published':e.get('published',''), 'description':'Open the original article for details.','url':e.get('link',''),'thumbnail':None})
        if not items: raise RuntimeError('No news available')
        _cache.update(at=time.time(),items=items)
        return {'articles':items,'cached':False,'source':'Live Google News RSS'}
    except Exception: return {'articles':_cache['items'],'cached':bool(_cache['items']),'error':'Live news is temporarily unavailable. Showing cached results if available.'}
