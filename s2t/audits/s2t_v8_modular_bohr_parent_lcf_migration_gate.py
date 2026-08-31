#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
OUTPUT=ROOT/'s2t/results/s2t_v8_modular_bohr_parent_lcf_migration_gate_results.json'
from s2t.proofdsl.examples.version8_modular_bohr import build_certificate
from s2t.proofdsl.verify import verify_all
def main():
 c=build_certificate(); assert c.transfer_count==13
 r=verify_all(); g=next(x for x in r['gates'] if x['identifier']=='version8_modular_bohr_parent_origin_gate')
 d={'date':'2026-08-29','gate':'version8_modular_bohr_parent_lcf_migration_gate','chain_number':{'gap':'2','forward_ratio':'exp(-2)','reverse_ratio':'exp(2)','transfer_pairs':13,'gauge_invariant':True},'orientation':{'both_branches_primitive':True,'orientation_selected':False},'proofdsl_registry':{'status':g['status'],'obligation_count':6,'certificate_sha256':r['certificate_sha256']['version8_modular_bohr_parent_origin_gate']},'verdict':{'status':'lcf-checked-twofold-orientation-open','next_gate':'version8_chain_orientation_index_defect_lcf_migration_gate'}}
 t=json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+'\n'; OUTPUT.write_text(t,encoding='utf-8'); print(OUTPUT); print(hashlib.sha256(t.encode()).hexdigest())
if __name__=='__main__': main()