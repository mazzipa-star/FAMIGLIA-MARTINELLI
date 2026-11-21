"""Generate a one-time PostgreSQL import of the existing public genealogy."""
from pathlib import Path
import json
r=Path(__file__).resolve().parents[1]
q=lambda s:"'"+str(s).replace("'","''")+"'"
j=lambda d:q(json.dumps(d,ensure_ascii=False))+"::jsonb"
trees=json.loads((r/'content/genealogia.json').read_text());records=json.loads((r/'content/ritratti-famiglia.json').read_text())
s=['begin;',"do $$begin if exists(select 1 from family_private.people) then raise exception 'Importazione già eseguita: i dati correnti non saranno sovrascritti';end if;end $$;"]
parents=set();partners=set()
for tree in trees:
 s.append('insert into family_private.trees values('+q(tree['id'])+','+j({k:v for k,v in tree.items() if k not in ['people','families']})+');')
 for p in tree['people']:
  s.append('insert into family_private.people(id,tree_id,data) values('+q(p['id'])+','+q(tree['id'])+','+j({k:v for k,v in p.items() if k not in ['parents','partners']})+');')
  parents.update((pid,p['id']) for pid in p['parents']);partners.update(tuple(sorted([p['id'],pid])) for pid in p['partners'])
for a,b in sorted(parents):s.append('insert into family_private.parents values('+q(a)+','+q(b)+');')
for a,b in sorted(partners):s.append('insert into family_private.partners values('+q(a)+','+q(b)+');')
for p in records:s.append('insert into family_private.records values('+q(p['id'])+','+j(p)+');')
for id,name in [('2','Graziella'),('4','Vera'),('6','Sante'),('8','Anna Maria')]:s.append('insert into family_private.branches(root_id,label) values('+q('discendenti-'+id)+','+q('Famiglia '+name)+');')
s.append('commit;')
(r/'backend/supabase/seed.sql').write_text('\n'.join(s)+'\n')
print('Importazione preparata:',sum(len(t['people']) for t in trees),'persone e',len(records),'schede.')
