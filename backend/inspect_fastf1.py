import fastf1
import pandas as pd

print('fastf1 version:', getattr(fastf1, '__version__', 'unknown'))
print('has get_session:', hasattr(fastf1, 'get_session'))
print('has get_event_schedule:', hasattr(fastf1, 'get_event_schedule'))

sched = fastf1.get_event_schedule(2026)
print('schedule shape:', sched.shape)
print('columns:', list(sched.columns))
print('head rows:')
print(sched.head(6).to_string(index=True))
print('---')
print('row2 keys:', dict(sched.iloc[2]))
