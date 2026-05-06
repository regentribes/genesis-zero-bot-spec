// Project document export view (printable)
function ProjectDocumentView({ values, onClose, onPrint }) {
  const D = window.FW_DATA;
  const pillarScores = computePillarScores(values);
  const overall = Object.values(pillarScores).reduce((a,b) => a+b, 0) / 5;
  const today = new Date().toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
  const projectName = values.project_name || 'Untitled Regenerative Neighborhood';

  return (
    <div className="modal-bg no-print" onClick={onClose}>
      <div className="modal" style={{position:'relative'}} onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>

        <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: 24, paddingBottom: 16, borderBottom: '1px solid var(--rule)'}}>
          <div>
            <div className="eyebrow">Preview & Print</div>
            <div style={{fontFamily:'var(--serif)', fontSize:24}}>Project Document</div>
          </div>
          <div className="row gap-8">
            <button className="btn" onClick={() => downloadAsHTML(values)}>⬇ Download HTML</button>
            <button className="btn btn-primary" onClick={onPrint}>🖨 Print / Save PDF</button>
          </div>
        </div>

        <div id="printable-doc">
          <DocBody values={values} D={D} pillarScores={pillarScores} overall={overall} today={today} projectName={projectName}/>
        </div>
      </div>
    </div>
  );
}

function DocBody({ values, D, pillarScores, overall, today, projectName }) {
  return (
    <div style={{padding: '0 0 40px', fontFamily:'var(--sans)', color:'var(--ink)'}}>
      {/* Cover */}
      <div style={{textAlign:'left', padding:'40px 0 32px', borderBottom:'2px solid var(--ink)'}}>
        <div className="eyebrow" style={{marginBottom: 20}}>Regenerative Neighborhood · Project Document</div>
        <div style={{fontFamily:'var(--serif)', fontSize: 48, lineHeight: 1.05, letterSpacing:'-0.02em', marginBottom: 18}}>
          {projectName}
        </div>
        <div style={{fontFamily:'var(--serif)', fontSize: 18, fontStyle:'italic', color:'var(--ink-2)', marginBottom: 24, maxWidth: 540}}>
          {values.vision_statement || 'A regenerative neighborhood in formation.'}
        </div>
        <div style={{display:'grid', gridTemplateColumns:'repeat(4, 1fr)', gap: 16, marginTop: 24, fontSize: 12}}>
          <div><div className="eyebrow">Date</div><div>{today}</div></div>
          <div><div className="eyebrow">Overall</div><div>{overall.toFixed(1)} / 10</div></div>
          <div><div className="eyebrow">Frameworks</div><div>RNF · Alchemy · RCOS · CLIPS</div></div>
          <div><div className="eyebrow">Version</div><div>v2.0</div></div>
        </div>
      </div>

      {/* Pillar scorecard */}
      <DocSection title="Diagnostic — RNF Pillars">
        <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap: 24, alignItems:'center'}}>
          <PillarRadar scores={pillarScores} size={260}/>
          <div>
            {D.pillars.map(p => (
              <div key={p.id} style={{marginBottom:14}}>
                <div style={{display:'flex', justifyContent:'space-between', marginBottom: 4}}>
                  <span style={{fontWeight:600}}>{p.name}</span>
                  <span className="mono" style={{fontSize: 12}}>{(pillarScores[p.id]||0).toFixed(1)}/10</span>
                </div>
                <div style={{height:4, background:'#e2d9bf', borderRadius:2}}>
                  <div style={{height:'100%', width:`${(pillarScores[p.id]||0)*10}%`, background: p.color, borderRadius:2}}></div>
                </div>
                <div style={{fontSize:11, color:'var(--ink-3)', marginTop:3}}>{p.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </DocSection>

      {/* Phases */}
      {D.phases.map(phase => (
        <DocSection key={phase.id} title={`Phase ${phase.num} — ${phase.name}: ${phase.subtitle}`} meta={phase.time}>
          <div style={{fontFamily:'var(--serif)', fontStyle:'italic', fontSize:16, color:'var(--ink-2)', marginBottom: 20}}>
            {phase.lede}
          </div>
          {phase.steps.filter(s => s.kind !== 'gate').map(step => {
            const hasContent = (step.fields||[]).some(f => values[f.id]) ||
                              (step.sliders||[]).some(s => values[s.id] != null) ||
                              (step.checklist||[]).some(c => values[c.id]);
            return (
              <div key={step.id} style={{marginBottom: 24, paddingBottom: 18, borderBottom:'1px dashed var(--rule-soft)'}}>
                <div style={{display:'flex', justifyContent:'space-between', alignItems:'baseline', marginBottom: 10}}>
                  <div style={{fontFamily:'var(--serif)', fontSize: 20, fontWeight: 500}}>
                    <span className="mono" style={{fontSize: 11, color:'var(--ink-3)', marginRight: 8}}>{step.num}</span>
                    {step.title}
                  </div>
                  <div className="mono" style={{fontSize: 9, color:'var(--ink-3)', letterSpacing:'0.1em'}}>
                    {step.tagLines.join(' · ').toUpperCase()}
                  </div>
                </div>

                {!hasContent && (
                  <div style={{fontSize: 12, color:'var(--ink-3)', fontStyle:'italic'}}>— No entries yet —</div>
                )}

                {(step.fields||[]).filter(f => values[f.id]).map(f => (
                  <div key={f.id} style={{marginBottom: 12}}>
                    <div className="eyebrow" style={{marginBottom: 4}}>{f.label}</div>
                    <div style={{fontSize: 13.5, whiteSpace:'pre-wrap', lineHeight: 1.5}}>{values[f.id]}</div>
                  </div>
                ))}

                {(step.checklist||[]).length > 0 && (
                  <div style={{marginTop: 10, fontSize: 12.5}}>
                    {step.checklist.map(c => (
                      <div key={c.id} style={{padding:'2px 0'}}>
                        <span style={{display:'inline-block', width:14}}>{values[c.id] ? '☑' : '☐'}</span>
                        {c.text}
                      </div>
                    ))}
                  </div>
                )}

                {(step.sliders||[]).filter(s => values[s.id] != null).length > 0 && (
                  <div style={{marginTop: 10, fontSize: 12, display:'grid', gridTemplateColumns:'1fr 1fr', gap: 8}}>
                    {step.sliders.filter(s => values[s.id] != null).map(s => (
                      <div key={s.id} style={{display:'flex', justifyContent:'space-between', padding:'4px 8px', background:'var(--paper-2)', borderRadius:3}}>
                        <span>{s.label}</span>
                        <span className="mono" style={{fontWeight:600}}>{values[s.id]}/10</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}

          {/* Gate result for this phase */}
          {phase.steps.filter(s => s.kind === 'gate').map(g => {
            const met = g.criteria.filter(c => {
              const v = values[c.metric];
              return (typeof v === 'boolean' && v) || (typeof v === 'number' && v >= 6);
            }).length;
            const ratio = met / g.criteria.length;
            const status = ratio >= 0.8 ? 'READY' : ratio >= 0.5 ? 'SOFT-PASS' : 'NOT READY';
            return (
              <div key={g.id} style={{marginTop:16, padding:14, background:'#fbf2e2', border:'1px solid var(--alchemy)', borderRadius:4}}>
                <div style={{display:'flex', justifyContent:'space-between', alignItems:'baseline', marginBottom: 6}}>
                  <div style={{fontFamily:'var(--serif)', fontSize: 17}}>{g.title} — {g.subtitle}</div>
                  <div className="mono" style={{fontSize: 10, letterSpacing:'0.16em'}}>{status} ({met}/{g.criteria.length})</div>
                </div>
                {g.criteria.map(c => {
                  const v = values[c.metric];
                  const m = (typeof v === 'boolean' && v) || (typeof v === 'number' && v >= 6);
                  return <div key={c.id} style={{fontSize:12, padding:'2px 0'}}>{m ? '✓' : '·'} {c.text}</div>;
                })}
              </div>
            );
          })}
        </DocSection>
      ))}

      {/* Action items */}
      <DocSection title="Action Items & Next Horizon">
        <ActionItems values={values} D={D} pillarScores={pillarScores}/>
      </DocSection>

      <div style={{marginTop:32, paddingTop:16, borderTop:'1px solid var(--rule)', fontSize:11, color:'var(--ink-3)', textAlign:'center'}}>
        Generated {today} · Regenerative Neighborhood Framework v2.0 · Open Source
      </div>
    </div>
  );
}

function DocSection({ title, meta, children }) {
  return (
    <div style={{marginTop: 32, pageBreakInside: 'avoid'}}>
      <div style={{display:'flex', justifyContent:'space-between', alignItems:'baseline', marginBottom: 16, paddingBottom: 6, borderBottom: '1px solid var(--ink)'}}>
        <div style={{fontFamily:'var(--serif)', fontSize: 24, fontWeight: 500, letterSpacing:'-0.01em'}}>{title}</div>
        {meta && <div className="mono" style={{fontSize:10, letterSpacing:'0.14em', color:'var(--ink-3)'}}>{meta.toUpperCase()}</div>}
      </div>
      {children}
    </div>
  );
}

function ActionItems({ values, D, pillarScores }) {
  // Build a list of weak spots and recommended actions
  const items = [];
  D.pillars.forEach(p => {
    const score = pillarScores[p.id] || 0;
    if (score < 5) {
      items.push({
        priority: 'High',
        pillar: p.name,
        action: `Strengthen ${p.name} pillar — score ${score.toFixed(1)}/10. Focus on: ${p.desc}.`
      });
    }
  });

  // Empty fields with text
  D.phases.forEach(phase => {
    phase.steps.forEach(step => {
      if (step.kind === 'gate') return;
      (step.fields||[]).forEach(f => {
        if (!values[f.id] || String(values[f.id]).length < 10) {
          items.push({
            priority: 'Medium',
            pillar: `Phase ${phase.num} · ${step.num}`,
            action: `Complete: ${f.label}`
          });
        }
      });
    });
  });

  if (items.length === 0) {
    return <div style={{fontStyle:'italic', color:'var(--ink-3)'}}>All foundations look solid. Next horizon: continuous regeneration.</div>;
  }

  return (
    <div>
      {items.slice(0, 12).map((it, i) => (
        <div key={i} style={{display:'grid', gridTemplateColumns:'80px 140px 1fr', gap: 12, padding:'8px 0', borderBottom:'1px dashed var(--rule-soft)', fontSize: 13}}>
          <div className="mono" style={{fontSize: 10, letterSpacing:'0.1em', color: it.priority === 'High' ? 'var(--alchemy)' : 'var(--ink-3)'}}>{it.priority.toUpperCase()}</div>
          <div className="mono" style={{fontSize: 11, color:'var(--ink-2)'}}>{it.pillar}</div>
          <div>{it.action}</div>
        </div>
      ))}
      {items.length > 12 && <div style={{fontSize: 11, color:'var(--ink-3)', marginTop: 8, fontStyle:'italic'}}>… and {items.length - 12} more</div>}
    </div>
  );
}

function downloadAsHTML(values) {
  // Simple JSON download for now; printing handles HTML/PDF
  const blob = new Blob([JSON.stringify(values, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `regen-neighborhood-${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

Object.assign(window, { ProjectDocumentView });
