// ============================================================
// SLOT MACHINE - GAME LOGICA
// ============================================================

(function () {
  'use strict';

  // --- State ---
  let credits = CONFIG.startCredits;
  let bet = CONFIG.defaultBet;
  let spinning = false;
  let lastResult = [];

  // --- DOM refs ---
  const elCredits   = document.getElementById('credits');
  const elBet       = document.getElementById('bet-display');
  const elWin       = document.getElementById('win-display');
  const elMessage   = document.getElementById('message');
  const elSpin      = document.getElementById('btn-spin');
  const elBetUp     = document.getElementById('btn-bet-up');
  const elBetDown   = document.getElementById('btn-bet-down');
  const elBetMin    = document.getElementById('btn-bet-min');
  const elBetMax    = document.getElementById('btn-bet-max');
  const elPaytable  = document.getElementById('paytable');
  const elPayBtn    = document.getElementById('btn-paytable');
  const elPayTable  = document.getElementById('pay-table-content');
  const elRTPValue  = document.getElementById('rtp-value');

  // --- Weighted random symbol picker ---
  function buildWeightedPool() {
    const pool = [];
    CONFIG.symbols.forEach(sym => {
      for (let i = 0; i < sym.weight; i++) pool.push(sym);
    });
    return pool;
  }

  const weightedPool = buildWeightedPool();

  function randomSymbol() {
    return weightedPool[Math.floor(Math.random() * weightedPool.length)];
  }

  // --- Build reel strip (visible + scroll buffer) ---
  function buildReelStrip(innerEl) {
    innerEl.innerHTML = '';
    // Pre-fill with random symbols for scroll effect
    for (let i = 0; i < CONFIG.spinSymbolCount + 3; i++) {
      appendSymbol(innerEl, randomSymbol());
    }
  }

  function appendSymbol(innerEl, sym) {
    const img = document.createElement('img');
    img.src = `img/${sym.name}.png`;
    img.alt = sym.label;
    img.className = 'symbol';
    img.title = sym.label;
    innerEl.appendChild(img);
    return img;
  }

  function setReelSymbol(innerEl, sym) {
    // Replace all children with a single centered symbol
    innerEl.innerHTML = '';
    innerEl.style.transform = 'translateY(0)';
    appendSymbol(innerEl, sym);
  }

  // --- Init reels ---
  const inners = [];
  for (let i = 0; i < CONFIG.reelCount; i++) {
    const inner = document.getElementById(`inner${i}`);
    inners.push(inner);
    setReelSymbol(inner, randomSymbol());
  }

  // --- Spin animation for one reel ---
  function spinReel(innerEl, finalSymbol) {
    return new Promise(resolve => {
      // Build scroll strip: random symbols + final at bottom
      innerEl.innerHTML = '';
      innerEl.style.transition = 'none';
      innerEl.style.transform = 'translateY(0)';

      const totalSymbols = CONFIG.spinSymbolCount;
      for (let i = 0; i < totalSymbols; i++) {
        appendSymbol(innerEl, randomSymbol());
      }
      // Final symbol at end
      appendSymbol(innerEl, finalSymbol);

      const totalHeight = totalSymbols * CONFIG.symbolHeight;

      // Force reflow
      innerEl.getBoundingClientRect();

      // Animate scroll
      innerEl.style.transition = `transform ${CONFIG.spinDuration}ms cubic-bezier(0.25, 0.1, 0.25, 1)`;
      innerEl.style.transform = `translateY(-${totalHeight}px)`;

      setTimeout(() => {
        // Snap to final symbol
        innerEl.style.transition = 'none';
        innerEl.style.transform = 'translateY(0)';
        innerEl.innerHTML = '';
        appendSymbol(innerEl, finalSymbol);
        resolve();
      }, CONFIG.spinDuration + 50);
    });
  }

  // --- Win evaluation ---
  function evaluate(results) {
    const [s0, s1, s2] = results;

    // WILD substitutes any symbol
    const isWild = s => s.name === 'wild';

    // 3 of a kind (including wild)
    let matchSym = null;
    if (s0.name === s1.name && s1.name === s2.name) {
      matchSym = s0;
    } else if (isWild(s0) && isWild(s1)) {
      matchSym = s2;
    } else if (isWild(s0) && isWild(s2)) {
      matchSym = s1;
    } else if (isWild(s1) && isWild(s2)) {
      matchSym = s0;
    } else if (isWild(s0) && s1.name === s2.name) {
      matchSym = s1;
    } else if (isWild(s1) && s0.name === s2.name) {
      matchSym = s0;
    } else if (isWild(s2) && s0.name === s1.name) {
      matchSym = s0;
    }

    if (matchSym && !isWild(matchSym)) {
      return { type: '3x', symbol: matchSym, multiplier: matchSym.payout };
    }
    if (isWild(s0) && isWild(s1) && isWild(s2)) {
      return { type: '3x', symbol: CONFIG.symbols.find(s => s.name === 'wild'), multiplier: CONFIG.symbols.find(s => s.name === 'wild').payout };
    }

    // 2 of a kind (payout2 > 0 only)
    const pairs = [[s0,s1],[s1,s2],[s0,s2]];
    for (const [a,b] of pairs) {
      if (a.name === b.name && a.payout2 > 0) {
        return { type: '2x', symbol: a, multiplier: a.payout2 };
      }
    }

    return null;
  }

  // --- UI updates ---
  function updateUI() {
    elCredits.textContent = credits;
    elBet.textContent = bet;
  }

  function showMessage(text, type) {
    elMessage.textContent = text;
    elMessage.className = type || '';
    elMessage.classList.remove('hidden');
  }

  function hideMessage() {
    elMessage.classList.add('hidden');
  }

  function setButtons(disabled) {
    spinning = disabled;
    elSpin.disabled = disabled;
    elBetUp.disabled = disabled;
    elBetDown.disabled = disabled;
    elBetMin.disabled = disabled;
    elBetMax.disabled = disabled;
  }

  // --- Spin handler ---
  async function doSpin() {
    if (spinning) return;
    if (credits < bet) {
      showMessage('NIET GENOEG CREDITS', '');
      return;
    }

    credits -= bet;
    elWin.textContent = 0;
    hideMessage();
    updateUI();
    setButtons(true);

    // Pick final symbols
    const finals = Array.from({ length: CONFIG.reelCount }, () => randomSymbol());

    // Spin reels with staggered delay
    const spinPromises = inners.map((inner, i) =>
      new Promise(resolve => setTimeout(() => spinReel(inner, finals[i]).then(resolve), i * CONFIG.spinDelay))
    );

    await Promise.all(spinPromises);

    lastResult = finals;
    const result = evaluate(finals);

    if (result) {
      const winAmount = bet * result.multiplier;
      credits += winAmount;
      elWin.textContent = winAmount;
      showMessage(`${result.type === '3x' ? '3x' : '2x'} ${result.symbol.label.toUpperCase()} +${winAmount}`, 'win');

      // Flash reels
      document.querySelectorAll('.reel-wrapper').forEach(rw => {
        rw.classList.add('win-flash');
        setTimeout(() => rw.classList.remove('win-flash'), 1500);
      });
    } else {
      showMessage('GEEN WIN', '');
    }

    updateUI();
    setButtons(false);

    if (credits <= 0) {
      showMessage('GAME OVER - Herlaad de pagina', '');
      elSpin.disabled = true;
    }
  }

  // --- Bet controls ---
  elBetUp.addEventListener('click', () => {
    if (bet < CONFIG.maxBet) { bet++; updateUI(); }
  });
  elBetDown.addEventListener('click', () => {
    if (bet > CONFIG.minBet) { bet--; updateUI(); }
  });
  elBetMin.addEventListener('click', () => { bet = CONFIG.minBet; updateUI(); });
  elBetMax.addEventListener('click', () => { bet = CONFIG.maxBet; updateUI(); });
  elSpin.addEventListener('click', doSpin);

  // Spacebar spin
  document.addEventListener('keydown', e => {
    if (e.code === 'Space' && !spinning) { e.preventDefault(); doSpin(); }
  });

  // --- Paytable ---
  function buildPaytable() {
    let totalRTP = 0;
    const totalWeight = weightedPool.length;
    const p3 = sym => Math.pow(sym.weight / totalWeight, 3);
    const p2 = sym => 3 * Math.pow(sym.weight / totalWeight, 2) * (1 - sym.weight / totalWeight);

    CONFIG.symbols.forEach(sym => {
      totalRTP += p3(sym) * sym.payout;
      if (sym.payout2 > 0) totalRTP += p2(sym) * sym.payout2;
    });

    elRTPValue.textContent = (totalRTP * 100).toFixed(1);

    elPayTable.innerHTML = CONFIG.symbols.map(sym =>
      `<tr>
        <td><img src="img/${sym.name}.png" style="width:24px;height:24px;vertical-align:middle"> ${sym.label}</td>
        <td>3x = ${sym.payout}x bet${sym.payout2 > 0 ? ` | 2x = ${sym.payout2}x bet` : ''}</td>
      </tr>`
    ).join('');
  }

  elPayBtn.addEventListener('click', () => {
    elPaytable.classList.toggle('hidden');
  });

  // --- Init ---
  buildPaytable();
  updateUI();

})();
