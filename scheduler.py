import datetime

def is_time(connections):
    now = datetime.now()
    tasks = [c for c in connections if now > datetime.fromtimestamp(c["time"])]
# feed it its relevant connections and their info
cmd = [tasks]

# Dont do this here: instead filter the db directly

updatetime