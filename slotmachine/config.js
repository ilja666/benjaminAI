// ============================================================
// SLOT MACHINE CONFIGURATIE
// Pas hier symbolen, gewichten en uitbetalingen aan.
// ============================================================

const CONFIG = {

  // Startkapitaal en inzet-limieten
  startCredits: 100,
  minBet: 1,
  maxBet: 10,
  defaultBet: 1,

  // Aantal reels en zichtbare rijen (altijd 1 payline = middelste rij)
  reelCount: 3,

  // Symbolen: name = bestandsnaam in img/, weight = hoe vaak op reel (hogere waarde = vaker)
  // payout = vermenigvuldiger op inzet bij 3x match
  // payout2 = vermenigvuldiger bij 2x match (0 = geen win)
  symbols: [
    { name: 'cherry', label: 'Cherry',  weight: 8,  payout: 5,   payout2: 1 },
    { name: 'lemon',  label: 'Lemon',   weight: 7,  payout: 8,   payout2: 0 },
    { name: 'orange', label: 'Orange',  weight: 6,  payout: 10,  payout2: 0 },
    { name: 'bell',   label: 'Bell',    weight: 5,  payout: 15,  payout2: 0 },
    { name: 'bar',    label: 'BAR',     weight: 4,  payout: 20,  payout2: 0 },
    { name: 'seven',  label: 'Seven',   weight: 2,  payout: 50,  payout2: 0 },
    { name: 'wild',   label: 'WILD',    weight: 1,  payout: 100, payout2: 0 },
  ],

  // Spin animatie instellingen
  spinDuration: 800,   // ms totale spinduur per reel
  spinDelay: 200,      // ms vertraging tussen reels
  symbolHeight: 110,   // px hoogte per symbool in reel
  spinSymbolCount: 20, // aantal symbolen dat langskomt tijdens spin
};
