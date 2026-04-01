<!DOCTYPE html>
<html lang="sl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ROI Kalkulator: Zdravstveno Zavarovanje</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f4f0; min-height: 100vh; padding: 32px 16px; color: #1a1a18; }
    .roi-wrap { max-width: 960px; margin: 0 auto; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 16px rgba(0,0,0,0.10); }
    .header-band { background: #0F6E56; padding: 28px 32px 24px; }
    .header-band h1 { color: #E1F5EE; font-size: 20px; font-weight: 500; margin: 0 0 4px; }
    .header-band p { color: #9FE1CB; font-size: 13px; margin: 0; }
    .body { display: grid; grid-template-columns: 300px 1fr; }
    .sidebar { background: #f0efe9; border-right: 0.5px solid #d3d1c7; padding: 24px 20px; }
    .results { background: #ffffff; padding: 24px 28px 32px; }
    .section-label { font-size: 11px; font-weight: 500; color: #0F6E56; text-transform: uppercase; letter-spacing: 0.06em; margin: 0 0 12px; }
    .field { margin-bottom: 14px; }
    .field label { display: block; font-size: 12px; color: #5f5e5a; margin-bottom: 4px; }
    .field input[type=number] { width: 100%; padding: 7px 10px; border: 0.5px solid #b4b2a9; border-radius: 6px; font-size: 13px; background: #fff; color: #1a1a18; outline: none; }
    .field input[type=number]:focus { border-color: #1D9E75; box-shadow: 0 0 0 2px rgba(29,158,117,0.12); }
    .field input[type=range] { width: 100%; accent-color: #1D9E75; }
    .checkbox-row { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; cursor: pointer; }
    .checkbox-row input { accent-color: #1D9E75; width: 14px; height: 14px; cursor: pointer; }
    .checkbox-row label { font-size: 12px; color: #5f5e5a; cursor: pointer; }
    .sep { height: 0.5px; background: #d3d1c7; margin: 16px 0 14px; }
    .metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px; }
    .metric { background: #f5f4f0; border-radius: 8px; padding: 14px 16px; }
    .metric .mlabel { font-size: 11px; color: #888780; margin-bottom: 6px; }
    .metric .mval { font-size: 21px; font-weight: 500; color: #1a1a18; }
    .metric .mval.pos { color: #0F6E56; }
    .metric .mval.neg { color: #993C1D; }
    .divider { height: 0.5px; background: #e8e7e1; margin: 16px 0; }
    .chart-label { font-size: 12px; color: #888780; margin: 0 0 10px; }
    .bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
    .bar-name { font-size: 12px; color: #5f5e5a; width: 140px; flex-shrink: 0; text-align: right; }
    .bar-track { flex: 1; height: 20px; background: #f0efe9; border-radius: 4px; overflow: hidden; }
    .bar-fill { height: 100%; border-radius: 4px; transition: width 0.35s ease; }
    .bar-amount { font-size: 12px; font-weight: 500; color: #1a1a18; min-width: 90px; }
    .summary-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px; }
    .summary-row span:first-child { font-size: 13px; color: #5f5e5a; }
    .summary-row span:last-child { font-size: 13px; font-weight: 500; color: #1a1a18; }
    .summary-row.total span:first-child { font-size: 14px; color: #1a1a18; font-weight: 500; }
    .summary-row.total span:last-child { font-size: 19px; font-weight: 500; color: #0F6E56; }
    .roi-badge { display: inline-flex; align-items: center; gap: 8px; background: #E1F5EE; border-radius: 8px; padding: 8px 18px; margin-top: 6px; }
    .roi-badge .roi-pct { font-size: 26px; font-weight: 500; color: #085041; }
    .roi-badge .roi-text { font-size: 12px; color: #0F6E56; }
    @media (max-width: 700px) {
      .body { grid-template-columns: 1fr; }
      .sidebar { border-right: none; border-bottom: 0.5px solid #d3d1c7; }
      .metrics { grid-template-columns: repeat(2, 1fr); }
    }
  </style>
</head>
<body>
<div class="roi-wrap">
  <div class="header-band">
    <h1>ROI kalkulator: zdravstveno zavarovanje za zaposlene</h1>
    <p>Ocena finančnega učinka kolektivnega zdravstvenega zavarovanja na podlagi bolniških odsotnosti in fluktuacije</p>
  </div>
  <div class="body">
    <div class="sidebar">
      <div class="section-label">Podatki podjetja</div>
      <div class="field"><label>Število zaposlenih</label><input type="number" id="zaposleni" value="50" min="1"></div>
      <div class="field"><label>Povprečna bruto I plača (€)</label><input type="number" id="bruto1" value="2500" min="0"></div>
      <div class="field">
        <label>Dni bolniške / zaposleni / leto: <span id="bolniska-out">15</span></label>
        <input type="range" id="bolniska" min="0" max="40" value="15" step="1">
      </div>
      <div class="field">
        <label>Faktor izgube produktivnosti: <span id="faktor-out">1.5</span></label>
        <input type="range" id="faktor" min="1.0" max="3.0" value="1.5" step="0.1">
      </div>
      <div class="sep"></div>
      <div class="section-label">Parametri zavarovanja</div>
      <div class="field"><label>Mesečna premija / zaposlenega (€)</label><input type="number" id="premija" value="35" min="0"></div>
      <div class="field">
        <label>Zmanjšanje odsotnosti: <span id="ucinek-out">15</span>%</label>
        <input type="range" id="ucinek" min="0" max="50" value="15" step="1">
      </div>
      <div class="sep"></div>
      <div class="section-label">Strateški vpliv</div>
      <div class="checkbox-row"><input type="checkbox" id="fluktuacija" checked><label for="fluktuacija">Vključi prihranek pri fluktuaciji</label></div>
      <div class="field" id="odhod-wrap"><label>Preprečeni odhodi / leto</label><input type="number" id="odhodi" value="1" min="0"></div>
    </div>

    <div class="results">
      <div class="section-label">Letni pregled stroškov in prihrankov</div>
      <div class="metrics">
        <div class="metric"><div class="mlabel">Strošek zavarovanja</div><div class="mval neg" id="m-zavarovanje">—</div></div>
        <div class="metric"><div class="mlabel">Prihranek pri bolniški</div><div class="mval pos" id="m-bolniska">—</div></div>
        <div class="metric"><div class="mlabel">Neto korist</div><div class="mval" id="m-neto">—</div></div>
      </div>

      <div class="divider"></div>
      <div class="chart-label">Primerjava stroškov (letno)</div>
      <div class="bar-row">
        <div class="bar-name">Brez zavarovanja</div>
        <div class="bar-track"><div class="bar-fill" id="bar-brez" style="background:#D85A30;"></div></div>
        <div class="bar-amount" id="lbl-brez">—</div>
      </div>
      <div class="bar-row">
        <div class="bar-name">Z zavarovanjem</div>
        <div class="bar-track"><div class="bar-fill" id="bar-z" style="background:#1D9E75;"></div></div>
        <div class="bar-amount" id="lbl-z">—</div>
      </div>
      <div class="bar-row" id="fluk-row">
        <div class="bar-name">Prihranek fluktuacija</div>
        <div class="bar-track"><div class="bar-fill" id="bar-fluk" style="background:#378ADD;"></div></div>
        <div class="bar-amount" id="lbl-fluk">—</div>
      </div>

      <div class="divider"></div>
      <div class="summary-row"><span>Strošek bolniške brez zavarovanja</span><span id="s1">—</span></div>
      <div class="summary-row"><span>Strošek bolniške z zavarovanjem</span><span id="s2">—</span></div>
      <div class="summary-row"><span>Strošek premij (letno)</span><span id="s3">—</span></div>
      <div class="summary-row" id="s4-row"><span>Prihranek pri fluktuaciji</span><span id="s4">—</span></div>
      <div class="divider"></div>
      <div class="summary-row total"><span>Letni neto prihranek</span><span id="s-total">—</span></div>
      <div style="margin-top:14px;">
        <div class="roi-badge">
          <span class="roi-pct" id="roi-pct">—</span>
          <span class="roi-text">ROI (donos na investicijo)</span>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
  const fmt = v => (v < 0 ? '-' : '') + Math.abs(Math.round(v)).toLocaleString('sl-SI') + ' €';
  const fmtPct = v => (v >= 0 ? '+' : '') + Math.round(v) + ' %';

  function calc() {
    const n       = +document.getElementById('zaposleni').value || 0;
    const b1      = +document.getElementById('bruto1').value || 0;
    const dni     = +document.getElementById('bolniska').value;
    const fak     = +document.getElementById('faktor').value;
    const premija = +document.getElementById('premija').value || 0;
    const ucinek  = +document.getElementById('ucinek').value / 100;
    const flukVklop = document.getElementById('fluktuacija').checked;
    const odhodi  = flukVklop ? (+document.getElementById('odhodi').value || 0) : 0;

    const bruto2          = b1 * 1.161;
    const dnevni          = bruto2 / 21;
    const strosakBrezZav  = n * dni * dnevni * fak;
    const strosakZZav     = strosakBrezZav * (1 - ucinek);
    const prispalek       = strosakBrezZav - strosakZZav;
    const strZav          = n * premija * 12;
    const strFluk         = flukVklop ? odhodi * b1 * 1.3 : 0;
    const neto            = prispalek - strZav + strFluk;
    const roi             = strZav > 0 ? ((prispalek + strFluk - strZav) / strZav) * 100 : 0;

    document.getElementById('m-zavarovanje').textContent = fmt(-strZav);
    document.getElementById('m-bolniska').textContent    = fmt(prispalek);
    const netoEl = document.getElementById('m-neto');
    netoEl.textContent = fmt(neto);
    netoEl.className   = 'mval ' + (neto >= 0 ? 'pos' : 'neg');

    const maxBar = Math.max(strosakBrezZav, strosakZZav + strZav, strFluk, 1);
    document.getElementById('bar-brez').style.width = Math.round((strosakBrezZav / maxBar) * 100) + '%';
    document.getElementById('bar-z').style.width    = Math.round(((strosakZZav + strZav) / maxBar) * 100) + '%';
    document.getElementById('bar-fluk').style.width = Math.round((strFluk / maxBar) * 100) + '%';
    document.getElementById('lbl-brez').textContent = fmt(strosakBrezZav);
    document.getElementById('lbl-z').textContent    = fmt(strosakZZav + strZav);
    document.getElementById('lbl-fluk').textContent = fmt(strFluk);

    document.getElementById('s1').textContent     = fmt(strosakBrezZav);
    document.getElementById('s2').textContent     = fmt(strosakZZav);
    document.getElementById('s3').textContent     = fmt(-strZav);
    document.getElementById('s4').textContent     = '+' + Math.abs(Math.round(strFluk)).toLocaleString('sl-SI') + ' €';
    document.getElementById('s-total').textContent = fmt(neto);
    document.getElementById('roi-pct').textContent = fmtPct(roi);

    document.getElementById('s4-row').style.display   = flukVklop ? 'flex' : 'none';
    document.getElementById('fluk-row').style.display = flukVklop ? 'flex' : 'none';
  }

  ['zaposleni','bruto1','premija','odhodi'].forEach(id =>
    document.getElementById(id).addEventListener('input', calc)
  );

  [['bolniska','bolniska-out'], ['ucinek','ucinek-out']].forEach(([id, out]) => {
    document.getElementById(id).addEventListener('input', () => {
      document.getElementById(out).textContent = document.getElementById(id).value;
      calc();
    });
  });

  document.getElementById('faktor').addEventListener('input', () => {
    document.getElementById('faktor-out').textContent = (+document.getElementById('faktor').value).toFixed(1);
    calc();
  });

  document.getElementById('fluktuacija').addEventListener('change', e => {
    document.getElementById('odhod-wrap').style.display = e.target.checked ? '' : 'none';
    calc();
  });

  calc();
</script>
</body>
</html>
