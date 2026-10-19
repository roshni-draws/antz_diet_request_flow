# sample.py: exec'd by sp3.py before embedding. SAMPLE DATA (not from the source system): bulks up the
# scope breakdown of Coypu (135332) and Common Buttonquail (229408) so the Scope card's scroll, search and
# filters have enough rows to be meaningful. Same shapes and ID styles as by-species.data.js.
import random as _r
_r.seed(7)
_NAMES = ['Nutmeg', 'Bramble', 'Pebble', 'Willow', 'Hazel', 'Juniper', 'Clover', 'Sorrel', 'Moss', 'Fern', 'Thistle', 'Rowan', 'Basil', 'Sage']
def _sp(t): return [x for x in BS['species'] if x['tsn'] == t][0]
def _plan(pid, tsn, scope, ref, name, items, reason, detail):
    BS['plans'][str(pid)] = {'id': pid, 'species': tsn, 'scope': scope, 'ref': ref, 'scopeName': name, 'active': True, 'verified': False, 'update': 'none',
        'reason': reason, 'reasonDetail': detail, 'dietitian': None, 'created': '2026-09-26', 'by': 'Narendra M', 'kind': 'base', 'sharers': [[tsn, pid]],
        'schedule': [{'time': 'any time', 'days': [{'day': 'Daily', 'items': items}]}]}

# ---- Coypu: 14 enclosures in 3 sections of Cow Land, 38 animals (SAMPLE DATA) ----
_c = _sp(135332)
_secs = [(190, 'Coypu Land'), (196, 'Coypu Marsh'), (197, 'Coypu Burrows')]
_counts = [4, 3, 3, 4, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2]
_enc = []
for i, n in enumerate(_counts):
    sec = _secs[0] if i < 5 else _secs[1] if i < 10 else _secs[2]
    _enc.append({'id': 15224 + i, 'name': 'Coypu ' + str(i + 1), 'sectionId': sec[0], 'section': sec[1], 'siteId': 57, 'site': 'Cow Land', 'animals': n})
_old = {a['id']: a for a in _c['animalList']}
_al, _nid = [], 215952
for e in _enc:
    keep = [a for a in _old.values() if a['enclosure'] == e['id']]
    for a in keep[:e['animals']]: _al.append(a)
    for k in range(e['animals'] - len(keep[:e['animals']])):
        a = {'id': _nid, 'sex': _r.choice(['m', 'f', 'f', 'm', 'u']), 'enclosure': e['id']}
        if _nid % 3 == 0: a['label'] = _NAMES[(_nid // 3) % len(_NAMES)]
        _al.append(a); _nid += 1
if not any(a['id'] == 215920 for a in _al): _al.insert(0, {'id': 215920, 'sex': 'm', 'enclosure': 15224})
_c['enclosures'], _c['animalList'], _c['animals'] = _enc, _al, len(_al)
_plan(150, 135332, 'animal', 215936, '#215936', [{'name': 'Sweet Potato', 'amount': '1.5 kg', 'prep': 'Steamed'}, {'name': 'Carrot', 'amount': '1 kg'}], 'Senior', 'Older female with worn teeth: steamed roots only.')
_plan(151, 135332, 'animal', 215961, '#215961', [{'name': 'Apple', 'amount': '2 kg'}, {'name': 'Spinach', 'amount': '0.5 kg'}], 'Recovery', 'Post-quarantine ration for four weeks.')
_plan(152, 135332, 'enclosure', 15232, 'Coypu 9', [{'name': 'Maize', 'amount': '6 kg'}, {'name': 'Carrot', 'amount': '4 kg'}], 'Shared Enclosure', 'Coypu 9 is shared with the marsh birds: grain is scattered, not bowled.')
_plan(154, 135332, 'enclosure', 15232, 'Coypu 9', [{'name': 'Sweet Potato', 'amount': '3 kg'}, {'name': 'Carrot', 'amount': '3 kg'}], 'Seasonal', 'Monsoon ration for Coypu 9: more roots while the marsh floods.')
BS['plans']['154'].update({'kind': 'seasonal', 'recurring': True, 'from': '2026-10-01', 'to': '2026-11-15'})   # SAMPLE DATA: seasonal overlap case for DR-00430
_c['plans'] = [150, 151, 152, 154] + _c['plans']

# ---- Common Buttonquail: 8 extra pens in a new Quail Yard section, 26 extra animals (SAMPLE DATA) ----
_q = _sp(229408)
_pens = [3, 4, 3, 2, 4, 3, 4, 3]
_qid = 216100
for i, n in enumerate(_pens):
    eid = 15300 + i
    _q['enclosures'].append({'id': eid, 'name': 'Quail Pen ' + str(i + 1), 'sectionId': 198, 'section': 'Quail Yard', 'siteId': 29, 'site': 'LSET FARM', 'animals': n})
    for k in range(n):
        _q['animalList'].append({'id': _qid, 'sex': _r.choice(['m', 'f', 'u']), 'enclosure': eid}); _qid += 1
_q['animals'] = _q['animals'] + sum(_pens)
_plan(153, 229408, 'enclosure', 15302, 'Quail Pen 3', [{'name': 'Mealworm', 'amount': '60 g'}, {'name': 'Ragi', 'amount': '120 g'}], 'Breeding', 'Laying pen: extra protein through the season.')
_q['plans'] = [153] + _q['plans']

# ---- No-diet species: sample holdings for the "Who is this diet for?" pickers (SAMPLE DATA) ----
_eid, _aid = [19990], [280001]
_NAMES2 = ['Kiri', 'Tano', 'Mara', 'Juno', 'Pip', 'Odi', 'Lumi', 'Zeb', 'Nia', 'Rafi', 'Suki', 'Tavi']
def _holdings(tsn, add):
    s = _sp(tsn)
    for (site_id, site, sec_id, sec, encs) in add:
        for (nm, n) in encs:
            s['enclosures'].append({'id': _eid[0], 'name': nm, 'sectionId': sec_id, 'section': sec, 'siteId': site_id, 'site': site, 'animals': n}); _eid[0] += 1
    have = {}
    for a in s['animalList']: have.setdefault(a['enclosure'], []).append(a)
    al = []
    for e in s['enclosures']:
        keep = have.get(e['id'], [])[:e['animals']]
        al.extend(keep)
        for k in range(e['animals'] - len(keep)):
            a = {'id': _aid[0], 'sex': _r.choice(['m', 'f', 'f', 'm', 'u']), 'enclosure': e['id']}
            if _aid[0] % 4 == 0: a['label'] = _NAMES2[(_aid[0] // 4) % len(_NAMES2)]
            al.append(a); _aid[0] += 1
    s['animalList'] = al; s['animals'] = len(al)
_holdings(150254, [   # Southern Cassowary: 2 sites, 5 sections, 28 animals
    (47, 'LSET', 901, 'Cassowary Paddock', [('Paddock A', 4), ('Paddock B', 3), ('Paddock C', 3)]),
    (29, 'LSET FARM', 163, 'Congo', [('CONGO 2', 3)]),
    (29, 'LSET FARM', 902, 'Ratite Run', [('Ratite Run 1', 4), ('Ratite Run 2', 3)]),
    (29, 'LSET FARM', 903, 'Quarantine Yard', [('Q Pen 1', 2), ('Q Pen 2', 2)]),
])
_holdings(161818, [   # Geoffroy's Marmoset: 2 sites, 4 sections
    (47, 'LSET', 904, 'Primate House', [('PH 1', 3), ('PH 2', 2), ('PH 3', 2)]),
    (47, 'LSET', 905, 'Night Enclosures', [('NE 1', 2), ('NE 2', 1)]),
    (29, 'LSET FARM', 906, 'Canopy Walk', [('CW 1', 2), ('CW 2', 2)]),
])
_holdings(161822, [   # Golden-Headed Lion Tamarin: 2 sites, 4 sections
    (29, 'LSET FARM', 906, 'Canopy Walk', [('CW 3', 3), ('CW 4', 2)]),
    (47, 'LSET', 904, 'Primate House', [('PH 4', 3), ('PH 5', 3)]),
    (47, 'LSET', 907, 'Tamarin Island', [('Island 1', 4), ('Island 2', 3)]),
])

# named marmoset for the animal-specific sample request (SAMPLE DATA)
_mar = [a for a in _sp(161818)['animalList'] if a.get('label')][0]
_MAR_ID, _MAR_LABEL = _mar['id'], _mar['label']
_MAR_NAME = _MAR_LABEL + ' · ' + [e['name'] for e in _sp(161818)['enclosures'] if e['id'] == _mar['enclosure']][0]
# ---- Fresh pending requests for the Head Dietician to configure (SAMPLE DATA) ----
_HA = {'id': 'u-dt', 'name': 'Hydar Ali', 'role': 'Dietician'}
SAMPLE_REQS = [
    {'id': 'DR-00430', 'status': 'requested', 'sp': 'Coypu', 'sci': 'Myocastor coypus', 'tsn': 135332, 'where': 'Enclosure · Coypu 9', 'scope': 'enclosure', 'scopeRef': 15232, 'scopeText': 'Coypu 9',
     'prio': 'high', 'type': 'temporary', 'title': 'Soft feed after dental check', 'text': 'Two coypu in Coypu 9 had teeth trimmed. Give soft, chopped roots and no whole maize for three weeks.',
     'notes': 'Vet will recheck on 31 Oct.', 'start': '2026-10-10', 'end': '2026-10-31', 'date': '1 Oct 2026', 'iso': '2026-10-01', 'currentLabel': 'D-152 Year-round', 'planId': 152, 'by': _HA,
     'events': [{'kind': 'submitted', 'at': '2026-10-01T09:20', 'by': 'Hydar Ali', 'role': 'Dietician', 'text': 'Request submitted'},
                {'kind': 'comment', 'at': '2026-10-01T09:24', 'by': 'Hydar Ali', 'role': 'Dietician', 'text': 'Dental notes from the vet attached.', 'files': ['Coypu-9-dental-notes.pdf']}]},
    {'id': 'DR-00431', 'status': 'requested', 'sp': 'Southern Cassowary', 'sci': 'Casuarius casuarius', 'tsn': 150254, 'where': 'Species · Species-wide', 'scope': 'species', 'scopeRef': None, 'scopeText': 'Whole species',
     'prio': 'medium', 'type': 'base', 'title': 'Base diet for the cassowaries', 'text': 'Southern Cassowary has no diet set. Please create a base fruit and pellet diet for all 28 birds.',
     'notes': 'Keepers currently feed papaya and ratite pellets twice a day.', 'start': '2026-10-15', 'end': '', 'date': '30 Sep 2026', 'iso': '2026-09-30', 'currentLabel': 'No active diet', 'planId': None, 'by': _HA,
     'events': [{'kind': 'submitted', 'at': '2026-09-30T16:05', 'by': 'Hydar Ali', 'role': 'Dietician', 'text': 'Request submitted'}]},
    {'id': 'DR-00432', 'status': 'requested', 'sp': 'Common Buttonquail', 'sci': 'Turnix sylvaticus', 'tsn': 229408, 'where': 'Section · Quail Yard', 'scope': 'section', 'scopeRef': 198, 'scopeText': 'Quail Yard',
     'prio': 'low', 'type': 'site', 'season': {'from': '11-01', 'to': '02-28'}, 'title': 'Winter ration for Quail Yard', 'text': 'Every winter the Quail Yard birds need more seed and mealworm. Please add a ration that repeats from November to February.',
     'notes': '', 'start': '2026-11-01', 'end': '2027-02-28', 'date': '29 Sep 2026', 'iso': '2026-09-29', 'currentLabel': 'D-210 Year-round', 'planId': 210, 'by': _HA,
     'events': [{'kind': 'submitted', 'at': '2026-09-29T11:40', 'by': 'Hydar Ali', 'role': 'Dietician', 'text': 'Request submitted'}]},
    {'id': 'DR-00433', 'status': 'configuring', 'sp': 'Coypu', 'sci': 'Myocastor coypus', 'tsn': 135332, 'where': 'Species · Species-wide', 'scope': 'species', 'scopeRef': None, 'scopeText': 'Whole species',
     'prio': 'medium', 'type': 'base', 'title': 'Less maize in the Coypu base diet', 'text': 'Keepers see weight gain across the colony. Cut maize in the base diet and add more greens for all coypu.',
     'notes': 'Weigh-in results shared in the chat.', 'start': '2026-10-05', 'end': '', 'date': '28 Sep 2026', 'iso': '2026-09-28', 'currentLabel': 'D-273 Year-round', 'planId': 220, 'by': _HA, 'acceptedBy': 'Dr. Meera Iyer',
     'events': [{'kind': 'submitted', 'at': '2026-09-28T10:15', 'by': 'Hydar Ali', 'role': 'Dietician', 'text': 'Request submitted'},
                {'kind': 'review', 'at': '2026-09-29T09:00', 'by': 'Dr. Meera Iyer', 'role': 'Head Dietician', 'text': 'Opened for review'},
                {'kind': 'accepted', 'at': '2026-09-29T09:05', 'by': 'Dr. Meera Iyer', 'role': 'Head Dietician', 'text': 'Request accepted. Editing is locked for the requester.'}]},
    {'id': 'DR-00434', 'status': 'requested', 'sp': "Geoffroy's Marmoset", 'sci': 'Callithrix geoffroyi', 'tsn': 161818, 'where': 'Animal · ' + _MAR_NAME, 'scope': 'animal', 'scopeRef': _MAR_ID, 'scopeText': _MAR_NAME,
     'prio': 'high', 'type': 'animal', 'title': 'Soft diet for ' + _MAR_LABEL + ' after a tooth extraction', 'text': _MAR_LABEL + ' had a tooth taken out. Give mashed fruit and soaked food only for ten days.',
     'notes': 'Vet review on day ten.', 'start': '2026-10-03', 'end': '2026-10-13', 'date': '1 Oct 2026', 'iso': '2026-10-01', 'currentLabel': 'No active diet', 'planId': None, 'by': _HA,
     'events': [{'kind': 'submitted', 'at': '2026-10-01T08:10', 'by': 'Hydar Ali', 'role': 'Dietician', 'text': 'Request submitted'}]},
    {'id': 'DR-00435', 'status': 'requested', 'sp': 'Golden-Headed Lion Tamarin', 'sci': 'Leontopithecus chrysomelas', 'tsn': 161822, 'where': 'Section · Tamarin Island', 'scope': 'section', 'scopeRef': 907, 'scopeText': 'Tamarin Island',
     'prio': 'low', 'type': 'site', 'title': 'Daily diet for Tamarin Island', 'text': 'The tamarins on Tamarin Island have no diet set. Please add a fruit, insect and gum diet for the section.',
     'notes': '', 'start': '2026-10-10', 'end': '', 'date': '27 Sep 2026', 'iso': '2026-09-27', 'currentLabel': 'No active diet', 'planId': None, 'by': _HA,
     'events': [{'kind': 'submitted', 'at': '2026-09-27T14:30', 'by': 'Hydar Ali', 'role': 'Dietician', 'text': 'Request submitted'}]},
]

# ---- Requests already at the kitchen stage, so the Kitchen Head has work on first open (SAMPLE DATA) ----
# Each has a proposed (inactive) plan configured by the Head Dietician, in the same shape the wizard saves.
_DM = {'id': 'u-dm', 'name': 'Dr. Meera Iyer'}
def _kev(sub, acc, cfg, sent, extra=None):
    ev = [{'kind': 'submitted', 'at': sub, 'by': 'Hydar Ali', 'role': 'Dietician', 'text': 'Request submitted'},
          {'kind': 'review', 'at': acc, 'by': 'Dr. Meera Iyer', 'role': 'Head Dietician', 'text': 'Opened for review'},
          {'kind': 'accepted', 'at': acc, 'by': 'Dr. Meera Iyer', 'role': 'Head Dietician', 'text': 'Request accepted. Editing is locked for the requester.'},
          {'kind': 'draft', 'at': cfg[0], 'by': 'Dr. Meera Iyer', 'role': 'Head Dietician', 'text': cfg[1]},
          {'kind': 'sent-kitchen', 'at': sent, 'by': 'Dr. Meera Iyer', 'role': 'Head Dietician', 'text': 'Sent to Kitchen'}]
    return ev + (extra or [])
def _prop(pid, tsn, scope, ref, name, items, kind, req, extra=None):
    _plan(pid, tsn, scope, ref, name, items, 'Other', '')
    p = BS['plans'][str(pid)]
    p.update({'active': False, 'proposed': True, 'fromReq': req, 'kind': kind, 'sharers': [], 'created': '2026-09-29', 'by': 'Dr. Meera Iyer'})
    if extra: p.update(extra)
    _sp(tsn)['plans'] = [pid] + _sp(tsn)['plans']
_prop(401, 135332, 'animal', 215936, '#215936', [{'name': 'Sweet Potato', 'amount': '1.5 kg', 'prep': 'Steamed'}, {'name': 'Carrot', 'amount': '1 kg', 'prep': 'Chopped'}], 'time-bound', 'DR-00425', {'from': '2026-10-05', 'to': '2026-10-25'})
_prop(402, 229408, 'enclosure', 15302, 'Quail Pen 3', [{'name': 'Mealworm', 'amount': '90 g'}, {'name': 'Ragi', 'amount': '120 g', 'prep': 'Cooked'}], 'base', 'DR-00426', {'editOf': 153, 'editOfLabel': 'D-153'})
_prop(403, 135332, 'section', 196, 'Coypu Marsh', [{'name': 'Spinach', 'amount': '3 kg', 'prep': 'Chopped'}, {'name': 'Carrot', 'amount': '4 kg', 'prep': 'Chopped'}], 'seasonal', 'DR-00427', {'from': '2026-10-01', 'to': '2026-11-30', 'recurring': True})
_prop(404, 135332, 'enclosure', 15235, 'Coypu 12', [{'name': 'Maize', 'amount': '2 kg'}, {'name': 'Sweet Potato', 'amount': '3 kg', 'prep': 'Steamed'}], 'base', 'DR-00428')
_KS = lambda rid, sp, sci, tsn, where, scope, ref, txt, prio, typ, title, text, start, end, date, iso, cur, plan, status, pid, label, ev, more=None: dict(
    {'id': rid, 'status': status, 'sp': sp, 'sci': sci, 'tsn': tsn, 'where': where, 'scope': scope, 'scopeRef': ref, 'scopeText': txt, 'prio': prio, 'type': typ, 'title': title, 'text': text,
     'notes': '', 'start': start, 'end': end, 'date': date, 'iso': iso, 'currentLabel': cur, 'planId': plan, 'by': _HA, 'acceptedBy': 'Dr. Meera Iyer',
     'proposedId': pid, 'cfgLabel': label, 'configuredBy': _DM, 'events': ev}, **(more or {}))
SAMPLE_REQS += [
    _KS('DR-00425', 'Coypu', 'Myocastor coypus', 135332, 'Animal · #215936 · Coypu 3', 'animal', 215936, '#215936', 'high', 'temporary', 'Steamed roots for the senior female',
        'The older female in Coypu 3 is losing weight. Give steamed, chopped roots only for three weeks.', '2026-10-05', '2026-10-25', '28 Sep 2026', '2026-09-28', 'D-150 Year-round', 150, 'kitchen_review', 401, 'Time-bound diet',
        _kev('2026-09-28T08:40', '2026-09-28T10:05', ('2026-09-29T09:10', 'Configured as Time-bound diet D-401 (Proposed)'), '2026-09-29T09:30')),
    _KS('DR-00426', 'Common Buttonquail', 'Turnix sylvaticus', 229408, 'Enclosure · Quail Pen 3', 'enclosure', 15302, 'Quail Pen 3', 'medium', 'site', 'More mealworm for laying hens',
        'Quail Pen 3 has four laying hens. Raise mealworm and add cooked ragi while they lay.', '2026-10-03', '', '27 Sep 2026', '2026-09-27', 'D-153 Year-round', 153, 'kitchen_review', 402, 'Year-round diet',
        _kev('2026-09-27T11:15', '2026-09-27T15:00', ('2026-09-28T09:40', 'Configured as Year-round diet D-402 (Proposed change to D-153)'), '2026-09-28T10:00'), {'editOf': 153, 'editOfLabel': 'D-153'}),
    _KS('DR-00427', 'Coypu', 'Myocastor coypus', 135332, 'Section · Coypu Marsh', 'section', 196, 'Coypu Marsh', 'low', 'site', 'Monsoon greens for Coypu Marsh',
        'The marsh enclosures flood in the monsoon. Add chopped greens and carrot from October to November.', '2026-10-01', '2026-11-30', '25 Sep 2026', '2026-09-25', 'D-273 Year-round', None, 'delayed', 403, 'Seasonal diet',
        _kev('2026-09-25T09:00', '2026-09-25T12:20', ('2026-09-26T10:10', 'Configured as Seasonal diet D-403 (Proposed)'), '2026-09-26T10:30',
             [{'kind': 'delayed', 'at': '2026-09-29T08:15', 'by': 'Suresh Gowda', 'role': 'Kitchen Head', 'text': 'Delayed to 6 Oct 2026: Spinach arrives with the Monday delivery'}]),
        {'delayUntil': '2026-10-06', 'delayReason': 'Spinach arrives with the Monday delivery', 'season': {'from': '10-01', 'to': '11-30'}}),
    _KS('DR-00428', 'Coypu', 'Myocastor coypus', 135332, 'Enclosure · Coypu 12', 'enclosure', 15235, 'Coypu 12', 'medium', 'base', 'Less maize for Coypu 12',
        'The pair in Coypu 12 are overweight. Cut maize and add steamed sweet potato.', '2026-10-04', '', '24 Sep 2026', '2026-09-24', 'D-273 Year-round', None, 'adjustment', 404, 'Year-round diet',
        _kev('2026-09-24T10:30', '2026-09-24T14:00', ('2026-09-25T09:00', 'Configured as Year-round diet D-404 (Proposed)'), '2026-09-25T09:20',
             [{'kind': 'adjustment', 'at': '2026-09-26T07:50', 'by': 'Suresh Gowda', 'role': 'Kitchen Head', 'text': 'Adjustment requested: Sweet potato is short this week. Please use carrot instead.'}]),
        {'adjustReason': 'Sweet potato is short this week. Please use carrot instead.'}),
]

# ---- More kitchen-stage requests so the Kitchen Dashboard looks populated (SAMPLE DATA) ----
_prop(405, 134496, 'enclosure', 15304, 'AG 3', [{'name': 'Papaya', 'amount': '1.2 kg'}, {'name': 'Pomegranate', 'amount': '0.6 kg', 'prep': 'Chopped'}], 'time-bound', 'DR-00418', {'from': '2026-10-06', 'to': '2026-10-27'})
_prop(406, 134467, 'species', None, None, [{'name': 'Ragi', 'amount': '0.4 kg', 'prep': 'Cooked'}, {'name': 'Spinach', 'amount': '0.2 kg', 'prep': 'Chopped'}], 'base', 'DR-00419', {'editOf': 283, 'editOfLabel': 'D-283'})
_prop(407, 302971, 'enclosure', 14907, 'CL 1', [{'name': 'Spinach', 'amount': '4 kg', 'prep': 'Washed'}, {'name': 'Sweet Potato', 'amount': '3 kg', 'prep': 'Steamed'}], 'seasonal', 'DR-00420', {'from': '2026-10-01', 'to': '2026-11-30', 'recurring': True})
_prop(408, 161819, 'enclosure', 15159, 'SAN 3', [{'name': 'Mealworm', 'amount': '40 g'}, {'name': 'Bannana', 'amount': '0.3 kg', 'prep': 'Chopped'}], 'base', 'DR-00421')
_prop(409, 172338, 'species', None, None, [{'name': 'Carrot', 'amount': '0.3 kg', 'prep': 'Chopped'}, {'name': 'Spinach', 'amount': '0.2 kg', 'prep': 'Washed'}], 'base', 'DR-00422', {'editOf': 234, 'editOfLabel': 'D-243'})
_prop(410, 134495, 'enclosure', 15306, 'AG 5', [{'name': 'Sunflower Seeds', 'amount': '0.2 kg'}, {'name': 'Apple', 'amount': '0.5 kg'}], 'time-bound', 'DR-00423', {'from': '2026-10-02', 'to': '2026-10-30'})
_prop(411, 360599, 'enclosure', 19981, 'Ril enclosure', [{'name': 'Spinach', 'amount': '2 kg', 'prep': 'Washed'}, {'name': 'Watermelon', 'amount': '3 kg', 'prep': 'Chopped'}], 'time-bound', 'DR-00424', {'from': '2026-10-01', 'to': '2026-10-20'})
def _ready(at):
    return [{'kind': 'sent-prep', 'at': at, 'by': 'Suresh Gowda', 'role': 'Kitchen Head', 'text': 'Sent to prep.'}]
SAMPLE_REQS += [
    _KS('DR-00418', 'Scarlet Macaw', 'Ara macao', 134496, 'Enclosure · AG 3', 'enclosure', 15304, 'AG 3', 'high', 'temporary', 'Extra fruit for the moulting pair',
        'The pair in AG 3 are in a heavy moult. Add papaya and chopped pomegranate for three weeks.', '2026-10-06', '2026-10-27', '29 Sep 2026', '2026-09-29', 'D-226 Year-round', 226, 'kitchen_review', 405, 'Time-bound diet',
        _kev('2026-09-29T08:05', '2026-09-29T11:30', ('2026-09-30T09:00', 'Configured as Time-bound diet D-405 (Proposed)'), '2026-09-30T09:20')),
    _KS('DR-00419', "Fischer's Lovebird", 'Agapornis fischeri', 134467, 'Species · Species-wide', 'species', None, 'Whole species', 'low', 'base', 'Add sprouted millet to the base diet',
        'Keepers want more variety for the lovebirds. Add cooked ragi and chopped greens to the base diet.', '2026-10-08', '', '29 Sep 2026', '2026-09-29', 'D-283 Year-round', 283, 'kitchen_review', 406, 'Base diet',
        _kev('2026-09-29T13:10', '2026-09-29T16:00', ('2026-09-30T10:20', 'Configured as Base diet D-406 (Proposed change to D-283)'), '2026-09-30T10:45'), {'editOf': 283, 'editOfLabel': 'D-283'}),
    _KS('DR-00420', 'Capybara', 'Hydrochoerus hydrochaeris', 302971, 'Enclosure · CL 1', 'enclosure', 14907, 'CL 1', 'medium', 'site', 'Monsoon greens for CL 1',
        'The paddock floods in the monsoon and grazing drops. Add washed greens and steamed sweet potato in October and November.', '2026-10-01', '2026-11-30', '23 Sep 2026', '2026-09-23', 'D-273 Year-round', 201, 'delayed', 407, 'Seasonal diet',
        _kev('2026-09-23T09:30', '2026-09-23T12:00', ('2026-09-24T09:15', 'Configured as Seasonal diet D-407 (Proposed)'), '2026-09-24T09:40',
             [{'kind': 'delayed', 'at': '2026-09-27T08:30', 'by': 'Suresh Gowda', 'role': 'Kitchen Head', 'text': 'Delayed to 8 Oct 2026: Spinach supply resumes next week'}]),
        {'delayUntil': '2026-10-08', 'delayReason': 'Spinach supply resumes next week', 'season': {'from': '10-01', 'to': '11-30'}}),
    _KS('DR-00421', 'Common Marmoset', 'Callithrix jacchus', 161819, 'Enclosure · SAN 3', 'enclosure', 15159, 'SAN 3', 'high', 'base', 'More protein for the breeding pair',
        'The female in SAN 3 is nursing. Add mealworm and banana to the daily diet.', '2026-10-02', '', '22 Sep 2026', '2026-09-22', 'D-273 Year-round', 211, 'adjustment', 408, 'Year-round diet',
        _kev('2026-09-22T10:00', '2026-09-22T13:20', ('2026-09-23T09:00', 'Configured as Year-round diet D-408 (Proposed)'), '2026-09-23T09:30',
             [{'kind': 'adjustment', 'at': '2026-09-24T08:10', 'by': 'Anil Kumar', 'role': 'Kitchen Operator', 'text': 'Adjustment requested: Mealworm stock is low until the next live feed delivery. Please halve it for now.'}]),
        {'adjustReason': 'Mealworm stock is low until the next live feed delivery. Please halve it for now.'}),
    _KS('DR-00422', 'Degu', 'Octodon degus', 172338, 'Species · Species-wide', 'species', None, 'Whole species', 'low', 'base', 'Less fruit, more greens for degus',
        'Degus should not get sugary fruit. Replace fruit with chopped carrot and washed greens.', '2026-09-30', '', '18 Sep 2026', '2026-09-18', 'D-243 Year-round', 234, 'ready', 409, 'Base diet',
        _kev('2026-09-18T09:00', '2026-09-18T11:00', ('2026-09-19T09:30', 'Configured as Base diet D-409 (Proposed change to D-243)'), '2026-09-19T10:00', _ready('2026-09-21T08:40')),
        {'editOf': 234, 'editOfLabel': 'D-243', 'readyAt': '2026-09-21T08:40'}),
    _KS('DR-00423', 'Blue-And-Yellow Macaw', 'Ara ararauna', 134495, 'Enclosure · AG 5', 'enclosure', 15306, 'AG 5', 'medium', 'temporary', 'Seeds for foraging enrichment',
        'Add sunflower seeds scattered for foraging in AG 5 through October.', '2026-10-02', '2026-10-30', '20 Sep 2026', '2026-09-20', 'D-273 Year-round', 182, 'ready', 410, 'Time-bound diet',
        _kev('2026-09-20T10:30', '2026-09-20T14:00', ('2026-09-21T09:20', 'Configured as Time-bound diet D-410 (Proposed)'), '2026-09-21T09:45', _ready('2026-09-23T07:55')),
        {'readyAt': '2026-09-23T07:55'}),
    _KS('DR-00424', 'Aldabra Giant Tortoise', 'Aldabrachelys gigantea', 360599, 'Enclosure · Ril enclosure', 'enclosure', 19981, 'Ril enclosure', 'high', 'temporary', 'Soft greens after shell check',
        'The vet treated a shell crack. Give washed greens and chopped watermelon only for three weeks.', '2026-10-01', '2026-10-20', '24 Sep 2026', '2026-09-24', 'D-263 Year-round', 263, 'ready', 411, 'Time-bound diet',
        _kev('2026-09-24T08:15', '2026-09-24T09:30', ('2026-09-24T12:00', 'Configured as Time-bound diet D-411 (Proposed)'), '2026-09-24T12:20', _ready('2026-09-25T07:30')),
        {'readyAt': '2026-09-25T07:30'}),
]

# ---- Kitchen auto-resolution demo: Head Dietician alternatives on proposed diet lines (SAMPLE DATA) ----
# Each line lists the main item, then the HD's alternatives in order ("or ..."). The kitchen preps the first
# candidate whose stock fully covers the line. Orange / Lime / Lemon / Grapefruit are SAMPLE Diet Master items.
SAMPLE_ITEMS = [
    {'id': 3901, 'name': 'Orange', 'unit': 'kg', 'preps': ['Whole', 'Chopped'], 'cuts': [], 'isActive': True, 'units': ['kg', 'g']},
    {'id': 3902, 'name': 'Lime', 'unit': 'kg', 'preps': ['Whole', 'Chopped'], 'cuts': [], 'isActive': True, 'units': ['kg', 'g']},
    {'id': 3903, 'name': 'Lemon', 'unit': 'kg', 'preps': ['Whole', 'Chopped'], 'cuts': [], 'isActive': True, 'units': ['kg', 'g']},
    {'id': 3904, 'name': 'Grapefruit', 'unit': 'kg', 'preps': ['Whole', 'Chopped'], 'cuts': [], 'isActive': True, 'units': ['kg', 'g']},
]
def _sched(items): return [{'time': 'any time', 'days': [{'day': 'Daily', 'items': items}]}]
def _citrus(q): return {'name': 'Orange', 'amount': q + ' kg', 'prep': 'Chopped', 'alts': [{'name': 'Lime', 'amount': q + ' kg'}, {'name': 'Lemon', 'amount': q + ' kg'}]}
BS['plans']['401']['schedule'] = _sched([{'name': 'Sweet Potato', 'amount': '1.5 kg', 'prep': 'Steamed', 'alts': [{'name': 'Carrot', 'amount': '1.5 kg', 'prep': 'Chopped'}]}, {'name': 'Carrot', 'amount': '1 kg', 'prep': 'Chopped'}])   # alternative wins
BS['plans']['402']['schedule'] = _sched([{'name': 'Mealworm', 'amount': '90 g', 'alts': [{'name': 'Egg', 'amount': '5 nos'}]}, {'name': 'Ragi', 'amount': '120 g', 'prep': 'Cooked'}])   # unresolved
BS['plans']['405']['schedule'] = _sched([_citrus('1.5'), {'name': 'Papaya', 'amount': '1.2 kg'}])   # Orange covers it: main item
BS['plans']['407']['schedule'] = _sched([_citrus('2.5'), {'name': 'Sweet Potato', 'amount': '3 kg', 'prep': 'Steamed', 'alts': [{'name': 'Carrot', 'amount': '3 kg'}]}])   # Lime (alternative 1)
BS['plans']['403']['schedule'] = _sched([_citrus('5'), {'name': 'Carrot', 'amount': '4 kg', 'prep': 'Chopped'}])   # Lemon (alternative 2)
BS['plans']['411']['schedule'] = _sched([{'name': 'Spinach', 'amount': '1 kg', 'prep': 'Washed'}, {'name': 'Watermelon', 'amount': '3 kg', 'prep': 'Chopped'}])


# ---- 10-species sample, clean slate (SAMPLE DATA) ----
# Only 10 species: 5 with one year-round base diet at species level and 5 with no diet at all. Every site,
# section, enclosure and animal of a base-diet species inherits that base diet: no overrides, no seasonal,
# time-bound or sex-based plans, and no proposed plans. No requests are seeded either; the user raises them.
SP_WITH = [135332, 134467, 360599, 195064, 127302]      # Coypu, Fischer's Lovebird, Aldabra Giant Tortoise, European Polecat, Elephantnose Fish
SP_WITHOUT = [150254, 161818, 195022, 132735, 235859]   # Southern Cassowary, Geoffroy's Marmoset, Meerkat, Green Iguana, Koi Fish
for _t in SP_WITH + SP_WITHOUT:
    if _t != 135332: _holdings(_t, [])   # one animal row per animal held, so the Animal-wide list matches the count
    _s = _sp(_t)
    _b = next((BS['plans'][str(i)] for i in _s['plans'] if BS['plans'][str(i)]['scope'] == 'species' and BS['plans'][str(i)]['kind'] == 'base' and BS['plans'][str(i)]['active']), None) if _t in SP_WITH else None
    _s['plans'] = [_b['id']] if _b else []
    if _b: _b['update'] = 'none'   # nothing pending: no requests are seeded
    _s['diet'] = bool(_b)
BS['species'] = [_sp(t) for t in SP_WITH + SP_WITHOUT]
_keep_t = set(SP_WITH + SP_WITHOUT)
_keep_p = {i for x in BS['species'] for i in x['plans']}
BS['plans'] = {k: v for k, v in BS['plans'].items() if v['id'] in _keep_p}
for _p in BS['plans'].values(): _p['sharers'] = [x for x in _p.get('sharers', []) if x[0] in _keep_t and x[1] in _keep_p]
SAMPLE_REQS = []
