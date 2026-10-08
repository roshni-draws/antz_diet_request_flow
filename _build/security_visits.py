# security_visits.py: exec'd by security.py. SAMPLE DATA gate visits for every building, 1 to 30 Sep 2026 (30 Sep is the
# mock "today"), for the Security Admin building Dashboard (entries, exits, exits with and without a challan) and the
# Security gate page. The Tab prototype's flow-data.js activity at Antz Kitchen is kept and moved a week on (23 Sep to 30 Sep).
import random as _rv

_V = _rv.Random(808)
V_VENDORS = ['Jamnagar Fresh Farms', 'Saurashtra Meat Suppliers', 'AquaLive Feeders', 'GreenLeaf Fodder Co-op', 'Mahalaxmi Hardware',
             'Coastal Cold Chain', 'Patel Grain Traders', 'City Linen Services', 'Shree Gas Agency', 'BioWaste Solutions', 'Estate Facilities']
V_DRIVERS = ['Hitesh Parmar', 'Imran Shaikh', 'Prakash Menon', 'Devji Bhai', 'Suresh Rana', 'Ramesh Bhai', 'Nitin Bhatt', 'Kalpesh Joshi', 'Bharat Solanki']
V_NOCH = ['Chef unavailable, released without the sealed DC', 'Empty return, no challan issued', 'Challan left with the store, copy to follow',
          'Service visit, no goods out', 'Driver lost the gate pass']
V_PURP = {'Entry': 'DELIVERY', 'Service': 'SERVICE', 'Staff': 'STAFF', 'Waste removal': 'WASTE', 'Emergency': 'EMERGENCY', 'Exit': 'DELIVERY'}


def _plate():
    return f"GJ-{_V.choice(['10', '03', '01', '12'])}-{_V.choice('ABKLMNPQTXY')}{_V.choice('ABKLMNPQTXY')}-{_V.randint(1000, 9999)}"


def _visits():
    out, n = [], 9100
    for b in SEC['buildings']:
        gs = [g for g in SEC['gates'] if g['bld'] == b['id'] and g['active']]
        ins = [g for g in gs if set(g['purposes']) & {'Entry', 'Service', 'Staff', 'Emergency'}] or gs
        outs = [g for g in gs if set(g['purposes']) & {'Exit', 'Service', 'Waste removal'}] or gs
        if not gs: continue
        busy = 6 if b['id'] in ('B01', 'B07') else _V.randint(2, 4)
        for day in range(1, 31):
            for _ in range(_V.randint(max(1, busy - 2), busy + 1)):
                g = _V.choice(ins); n += 1
                h, m = _V.randint(6, 17), _V.choice([2, 8, 15, 21, 34, 40, 47, 53])
                if day == 30: h, m = min(h, 15), (m if h < 15 else min(m, 34))   # nothing after the mock 3:42 PM
                inn = f'2026-09-{day:02d}T{h:02d}:{m:02d}'
                v = {'id': f'GV-{n}', 'bld': b['id'], 'gate': g['id'], 'vehicleNo': _plate(), 'vendor': _V.choice(V_VENDORS),
                     'driver': _V.choice(V_DRIVERS), 'purpose': V_PURP.get(_V.choice(g['purposes']), 'DELIVERY'), 'enteredAt': inn,
                     'challanNo': f"DC-{_V.choice(['JFF', 'SMS', 'AQL', 'GLF', 'MLH', 'CCC', 'PGT'])}-{_V.randint(1000, 9999)}", 'lines': _V.randint(1, 9)}
                today_late = day == 30 and h >= 13
                if today_late and _V.random() < .6:
                    v['state'] = 'INSIDE'
                else:
                    dwell = _V.randint(25, 150)
                    if day == 30: dwell = min(dwell, (15 * 60 + 40) - (h * 60 + m))
                    eh, em = h + (m + dwell) // 60, (m + dwell) % 60
                    v.update(state='EXITED', exitGate=_V.choice(outs)['id'], exitedAt=f'2026-09-{day:02d}T{min(eh, 21):02d}:{em:02d}')
                    v['exitChallan'] = _V.random() > .12
                    if not v['exitChallan']: v['exitNote'] = _V.choice(V_NOCH)
                out.append(v)
    for b in SEC['buildings']:   # expected later today (Upcoming on the admin dashboard)
        gs = [g for g in SEC['gates'] if g['bld'] == b['id'] and g['active'] and set(g['purposes']) & {'Entry', 'Service'}]
        for k in range(_V.randint(2, 4) if gs else 0):
            n += 1; h, m = _V.choice([15, 16, 16, 17, 18]), _V.choice([5, 20, 35, 50])
            if h == 15: m = 55
            out.append({'id': f'GV-{n}', 'bld': b['id'], 'gate': _V.choice(gs)['id'], 'state': 'UPCOMING', 'vehicleNo': _plate(), 'vendor': _V.choice(V_VENDORS), 'driver': _V.choice(V_DRIVERS),
                        'purpose': 'DELIVERY', 'eta': f'2026-09-30T{h:02d}:{m:02d}', 'challanNo': f"DC-{_V.choice(['JFF', 'SMS', 'AQL', 'GLF', 'CCC', 'PGT'])}-{_V.randint(1000, 9999)}", 'lines': _V.randint(1, 9)})
    for a in SEC.get('activity', []):   # the flow-data.js gate activity, on 30 Sep
        v = dict(a, bld='B01'); v['id'] = a['id']
        if v.get('vendor') == 'Vantara Facilities': v['vendor'] = 'Estate Facilities'   # keep sample vendors generic
        for k in ('eta', 'atGateAt', 'enteredAt', 'exitedAt'):
            if v.get(k): v[k] = ('2026-09-30' if v[k][:10] == '2026-09-23' else '2026-09-29') + v[k][10:16]   # 23 Sep was the prototype's today
        if v['state'] == 'EXITED':
            v['exitGate'] = 'G03' if a['gate'] == 'G03' else 'G01'
            v['exitChallan'] = 'released without' not in (a.get('note') or '')
            if not v['exitChallan']: v['exitNote'] = 'Chef unavailable, released without the sealed DC'
        out.append({k: x for k, x in v.items() if x not in (None, '')})
    return out


VISITS = _visits()
