# security_tx.py: exec'd by security.py. SAMPLE DATA for the Sites tab site transfers, recreated from the mobile
# screenshots in "secuirty/site transfer" (Animal / Egg / Egg Discard / Hospital / Carcass transfer lists and details).
# Deterministic (seeded) so a rebuild gives the same data. Sites, departments and buildings come from security-data.json.
import random as _rnd

_R = _rnd.Random(38)
TX_PEOPLE = ['Reena Patil', 'Shambhavi Kulkarni', 'Carol Steve', 'Sourav Tambe', 'Kiran Joshi', 'Neha Bansal', 'Arjun Mehta', 'Lata Rao']
TX_INCHARGE = {'S1': 'Mahesh Rathod', 'S2': 'Dilip Vaghela', 'S3': 'Kavya Nair', 'S4': 'Harish Solanki', 'S5': 'Pooja Trivedi'}
TX_GUARDS = ['Mahesh Rathod', 'Dilip Vaghela', 'Ravi Naik']
TX_ANIMALS = [('Indian Peafowl', 'Pavo cristatus'), ('Spotted Deer', 'Axis axis'), ('Sloth Bear', 'Melursus ursinus'),
              ('Indian Star Tortoise', 'Geochelone elegans'), ('Great Hornbill', 'Buceros bicornis'), ('Asiatic Lion', 'Panthera leo persica'),
              ('Indian Rock Python', 'Python molurus'), ('Mugger Crocodile', 'Crocodylus palustris'), ('Blackbuck', 'Antilope cervicapra'),
              ('Hyacinth Macaw', 'Anodorhynchus hyacinthinus'), ('Red Panda', 'Ailurus fulgens'), ('Corn Snake', 'Pantherophis guttatus')]
TX_MARK = ['Chiki', 'Raja', 'Tara', 'Moti', 'Bijli', 'Kavi', 'Sona', '']
TX_HOSP = ['Wildlife Hospital', 'Elephant Hospital', 'Quarantine Hospital']
TX_NURSERY = ['Nursery 1', 'Nursery 2', 'Hatchery']
TX_REASON = ['Shifted', 'Breeding loan', 'Space management', 'Exchange programme']
TX_VISIT = ['Check-up', 'Surgery', 'Follow-up', 'Quarantine']
TX_PURPOSE = ['Routine health check', 'Wound dressing', 'Dental review', 'Post-surgery observation', 'X-ray and bloods']
TX_ENCL = ['Aviary 03', 'Deer Paddock 2', 'Bear Wing B', 'Reptile House', 'Hornbill Aviary', 'Lion Enclosure A', 'Enc 123']
TX_DISCARD_NOTE = ['Infertile on candling', 'Cracked shell', 'Dead in shell at day 18', 'Not viable after 30 days']

# status keys: [label, tone, pending] pending is 'in' (check-in), 'out' (checkout) or '' (nothing for security to do)
TX_ST = {
    'out': ['Security checkout pending', 'pend', 'out'],
    'in': ['Security check-in pending', 'pend', 'in'],
    'transit': ['In transit', 'pend', ''],
    'cleared': ['Security cleared', 'pend', ''],
    'done': ['Completed', 'done', ''],
    'initiated': ['Transfer initiated', 'pend', ''],
    'dpend': ['Security check pending', 'muted', 'out'],
    'dchecked': ['Security checked', 'pend', ''],
}
TX_TYPES = [['animal', 'Animal Transfer', 'INT-'], ['egg', 'Egg Transfer', 'EGGTRANS-'], ['discard', 'Egg Discard', 'EGGDIS-'],
            ['hospital', 'Hospital Transfer', 'HT38-'], ['carcass', 'Carcass Transfer', 'CT38-']]
TX_STEPS = {
    'animal': ['Transfer requested', 'Approved by both sites', 'Security checkout', 'In transit', 'Security check-in', 'Completed'],
    'egg': ['Transfer requested', 'Security checkout', 'In transit', 'Security check-in', 'Delivered'],
    'discard': ['Discard requested', 'Security check', 'Discarded'],
    'hospital': ['Transfer requested', 'Security checkout', 'In transit', 'Security check-in', 'Transfer completed'],
    'carcass': ['Transfer initiated', 'Security checkout', 'In transit', 'Security check-in', 'Transfer completed'],
}
# step index each status has reached
TX_AT = {'animal': {'out': 2, 'transit': 3, 'in': 4, 'done': 5}, 'egg': {'out': 1, 'transit': 2, 'cleared': 2, 'in': 3, 'done': 4},
         'discard': {'dpend': 1, 'dchecked': 2}, 'hospital': {'out': 1, 'transit': 2, 'in': 3, 'done': 4},
         'carcass': {'initiated': 0, 'out': 1, 'transit': 2, 'in': 3, 'done': 4}}
TX_MIX = {'animal': ['out', 'out', 'in', 'transit', 'done'], 'egg': ['done', 'done', 'cleared', 'transit', 'out', 'in'],
          'discard': ['dpend', 'dpend', 'dchecked'], 'hospital': ['done', 'out', 'out', 'in', 'transit'],
          'carcass': ['out', 'done', 'out', 'initiated', 'in']}
TX_COUNTS = {'animal': (2, 5), 'egg': (5, 9), 'discard': (3, 7), 'hospital': (5, 9), 'carcass': (3, 6)}


def _tx_when(i):   # newest first, back from 30 Sep 2026 (the mock status bar date)
    day = 30 - (i * 2 + _R.randint(0, 1))
    mon = 9
    while day < 1: day += 31 if mon - 1 in (1, 3, 5, 7, 8, 10, 12) else 30; mon -= 1
    return f'2026-{mon:02d}-{day:02d}T{_R.randint(8, 18):02d}:{_R.choice([5, 12, 23, 37, 41, 56]):02d}'


def _tx_build():
    out, n = {}, {'animal': 3070, 'egg': 289, 'discard': 226, 'hospital': 616, 'carcass': 323}
    sites = SEC['sites']
    for s in sites:
        others = [x['name'] for x in sites if x['id'] != s['id']]
        lst = []
        for key, label, pre in TX_TYPES:
            lo, hi = TX_COUNTS[key]
            for i in range(_R.randint(lo, hi)):
                st = TX_MIX[key][i % len(TX_MIX[key])] if i < len(TX_MIX[key]) else _R.choice(TX_MIX[key])
                n[key] -= _R.randint(1, 4)
                by = _R.choice(TX_PEOPLE)
                t = {'id': pre + f'{n[key]:05d}', 'type': key, 'site': s['id'], 'at': _tx_when(i), 'by': by, 'st': st}
                if key == 'animal':
                    t.update(fr=s['name'], to=_R.choice(others), qty=_R.randint(1, 4), reason=_R.choice(TX_REASON), team=_R.randint(4, 29),
                             approvers=[[_R.choice(TX_PEOPLE), 'Originating site', s['name']], [_R.choice(TX_PEOPLE), 'Destination site', None]],
                             checklist=_R.randint(0, 7))
                    t['approvers'][1][2] = t['to']
                    t['animals'] = [list(_R.choice(TX_ANIMALS)) + [str(_R.randint(220000, 240000)), _R.choice(TX_ENCL)] for _ in range(t['qty'])]
                elif key == 'egg':
                    out_ = _R.random() < .7
                    t.update(fr=s['name'], to=_R.choice(TX_NURSERY), toSite=s['name'] if not out_ else _R.choice(others), qty=_R.randint(1, 6),
                             species=_R.choice(TX_ANIMALS[:5] + TX_ANIMALS[9:10]))
                elif key == 'discard':
                    t.update(fr=s['name'], qty=_R.randint(1, 4), note=_R.choice(TX_DISCARD_NOTE), photos=_R.randint(1, 3))
                    if st == 'dchecked': t['check'] = {'name': _R.choice(TX_GUARDS), 'note': _R.choice(['Shells counted and bagged', 'Matches the request', 'Witnessed disposal'])}
                else:
                    a = _R.choice(TX_ANIMALS)
                    inbound = _R.random() < .3
                    place = _R.choice(TX_HOSP) if key == 'hospital' else _R.choice(TX_HOSP[:1] + ['National Necropsy Centre'])
                    t.update(fr=place if inbound and key == 'hospital' else (s['name'] if key == 'hospital' else _R.choice(TX_HOSP)),
                             to=s['name'] if inbound and key == 'hospital' else (place if key == 'hospital' else 'National Necropsy Centre'),
                             qty=1, animal=[a[0], a[1], str(_R.randint(220000, 240000)), _R.choice(TX_ENCL), _R.choice(TX_MARK), _R.choice(['M', 'F', 'UD'])])
                    if key == 'hospital': t.update(med='MED38-' + str(_R.randint(18000, 19999)), visit=_R.choice(TX_VISIT), purpose=_R.choice(TX_PURPOSE), checklist=_R.randint(0, 7))
                lst.append(t)
        out[s['id']] = lst
    return out


TX = _tx_build()
TX_META = {'types': TX_TYPES, 'st': TX_ST, 'steps': TX_STEPS, 'at': TX_AT, 'incharge': TX_INCHARGE}
