import pickle, sys, time
from concurrent.futures import ThreadPoolExecutor
from src.pit import data
from src.pit.universe import all_tickers, region
F = pickle.loads((data.ROOT / 'fundamentals.pkl').read_bytes())
import os
START = os.environ.get('PIT_START', '2025-01-15')
jobs = [(t, d) for t in all_tickers() for d in data.decision_dates(start=START, region_code=region(t))]
done = [0]
def one(j):
    t, d = j
    try:
        r = data.news_asof(t, d, F[t].get('name'))
    except Exception as e:
        r = None; print('ERR', t, d, repr(e)[:80], flush=True)
    done[0] += 1
    if done[0] % 100 == 0: print(done[0], '/', len(jobs), time.strftime('%H:%M:%S'), flush=True)
    return (t, str(d.date()), None if r is None else len(r))
with ThreadPoolExecutor(4) as ex: res = list(ex.map(one, jobs))
empty = [r for r in res if not r[2]]
print('DONE', len(res), 'empty', len(empty), empty[:20])
