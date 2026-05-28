class QuranMediaPlayerCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._hass = null;
    this._lang = "ar";
    this._showSurah = false;
    this._showReciter = false;
    this._showPlayer = false;
    this._listScrollSurah = 0;
    this._listScrollReciter = 0;
  }

  setConfig(config) {
    this._config = config || {};
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  getCardSize() { return 3; }

  _t(ar, en) { return this._lang === "ar" ? ar : en; }

  _entity() { return this._hass?.states["media_player.player"]; }
  _attr(k) { return this._entity()?.attributes?.[k]; }
  _call(domain, service, data = {}) { this._hass.callService(domain, service, data); }

  _saveScroll() {
    const sl = this.shadowRoot.querySelector(".list-surah");
    const rl = this.shadowRoot.querySelector(".list-reciter");
    const pl = this.shadowRoot.querySelector(".list-player");
    if (sl) this._listScrollSurah = sl.scrollTop;
    if (rl) this._listScrollReciter = rl.scrollTop;
  }

  _restoreScroll() {
    const sl = this.shadowRoot.querySelector(".list-surah");
    const rl = this.shadowRoot.querySelector(".list-reciter");
    if (sl) sl.scrollTop = this._listScrollSurah;
    if (rl) rl.scrollTop = this._listScrollReciter;
  }

  _render() {
    if (!this._hass) return;
    this._saveScroll();

    const state    = this._entity()?.state ?? "idle";
    const isPlay   = state === "playing";
    const isLive   = this._attr("is_live") ?? false;
    const surah    = this._attr("sound_mode") ?? "—";
    const reciter  = this._attr("source") ?? "—";
    const player   = this._attr("selected_player") ?? "—";
    const surahs   = this._attr("sound_mode_list") ?? [];
    const reciters = this._attr("source_list") ?? [];
    const players  = this._attr("available_players") ?? [];
    const playerShort = player.replace("media_player.", "");

    const surahAr  = surah.split("|")[0]?.trim() ?? surah;
    const surahEn  = surah.split("|")[1]?.trim() ?? surah;
    const reciterAr = reciter.split("|")[0]?.trim() ?? reciter;
    const reciterEn = reciter.split("|")[1]?.trim() ?? reciter;

    

    this.shadowRoot.innerHTML = `
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  :host { display: block; font-family: 'Segoe UI', system-ui, sans-serif; }

  .card {
    border-radius: 20px;
    overflow: visible;
    position: relative;
    color: #fff;
    min-height: 180px;
  }

  .bg {
    position: absolute; inset: 0;
    background: linear-gradient(145deg, #0a3d1f 0%, #052010 40%, #031a0d 100%);
    z-index: 0;
  }

  .overlay {
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 70% 20%, rgba(0,120,50,0.15) 0%, transparent 60%),
                radial-gradient(ellipse at 20% 80%, rgba(0,80,30,0.1) 0%, transparent 50%);
    z-index: 1;
  }

  .content {
    position: relative;
    z-index: 2;
  }

  .top {
    padding: 18px 18px 14px;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .info { flex: 1; min-width: 0; direction: ${this._lang==="ar"?"rtl":"ltr"}; }

  .title {
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 0.3px;
    white-space: nowrap;
    overflow: visible;
    text-overflow: ellipsis;
    color: #fff;
    text-shadow: 0 1px 4px rgba(0,0,0,0.5);
  }

  .sub {
    font-size: 12px;
    color: rgba(255,255,255,0.7);
    margin-top: 3px;
    white-space: nowrap;
    overflow: visible;
    text-overflow: ellipsis;
  }

  .live-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #ff5252;
    margin-left: 5px;
    animation: blink 1.4s infinite;
    vertical-align: middle;
  }

  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

  .status {
    font-size: 11px;
    font-weight: 600;
    color: ${isPlay ? "#69f0ae" : "rgba(255,255,255,0.5)"};
    white-space: nowrap;
    flex-shrink: 0;
  }

  .controls {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
  }

  .btn-play {
    width: 42px; height: 42px;
    border-radius: 50%;
    background: rgba(255,255,255,0.95);
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: #1a3d2b;
    flex-shrink: 0;
    transition: .15s;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
  }
  .btn-play:hover { background: #fff; transform: scale(1.05); }

  .btn-icon {
    width: 34px; height: 34px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.3);
    background: rgba(255,255,255,0.1);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255,255,255,0.85);
    font-size: 14px;
    transition: .15s;
    backdrop-filter: blur(4px);
  }
  .btn-icon:hover { background: rgba(255,255,255,0.2); border-color: rgba(255,255,255,0.6); }

  .btn-lang {
    font-size: 10px;
    font-weight: 700;
    padding: 4px 8px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.3);
    background: rgba(255,255,255,0.1);
    cursor: pointer;
    color: rgba(255,255,255,0.85);
    transition: .15s;
    flex-shrink: 0;
    backdrop-filter: blur(4px);
  }
  .btn-lang:hover { background: rgba(255,255,255,0.2); }

  .divider {
    height: 1px;
    background: rgba(255,255,255,0.12);
    margin: 0 18px;
  }

  .bottom {
    padding: 10px 18px;
    display: flex;
    align-items: center;
    gap: 8px;
    position: relative;
  }

  .sel-btn {
    flex: 1;
    padding: 7px 10px;
    border-radius: 10px;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    font-size: 12px;
    color: #fff;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 5px;
    min-width: 0;
    direction: ${this._lang==="ar"?"rtl":"ltr"};
    transition: .15s;
    backdrop-filter: blur(4px);
  }
  .sel-btn:hover, .sel-btn.open {
    background: rgba(255,255,255,0.18);
    border-color: rgba(255,255,255,0.5);
  }
  .sel-btn span {
    flex: 1;
    white-space: nowrap;
    overflow: visible;
    text-overflow: ellipsis;
    text-align: ${this._lang==="ar"?"right":"left"};
  }

  .btn-live {
    padding: 7px 11px;
    border-radius: 10px;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    font-size: 12px;
    color: rgba(255,255,255,0.85);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 5px;
    flex-shrink: 0;
    transition: .15s;
    white-space: nowrap;
    backdrop-filter: blur(4px);
  }
  .btn-live:hover { background: rgba(255,82,82,0.2); border-color: #ff5252; color: #ff5252; }
  .btn-live.active { background: rgba(255,82,82,0.15); border-color: #ff5252; color: #ff5252; }

  .dropdown {
    position: absolute;
    ${this._lang==="ar"?"right":"left"}: 18px;
    bottom: calc(100% + 8px);
    width: calc(50% - 22px);
    background: rgba(10,30,20,0.97);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 14px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    z-index: 999;
    overflow: visible;
    backdrop-filter: blur(16px);
  }
  .dropdown.reciter {
    ${this._lang==="ar"?"left":"right"}: 18px;
    ${this._lang==="ar"?"right":"left"}: unset;
  }

  .list-surah, .list-reciter {
    max-height: 220px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.2) transparent;
  }

  .item {
    padding: 10px 14px;
    font-size: 13px;
    cursor: pointer;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    color: rgba(255,255,255,0.85);
    direction: ${this._lang==="ar"?"rtl":"ltr"};
    transition: .1s;
  }
  .item:last-child { border-bottom: none; }
  .item:hover { background: rgba(255,255,255,0.08); color: #fff; }
  .item.sel { color: #69f0ae; font-weight: 600; }

  .player-row {
    padding: 0 18px 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    position: relative;
  }

  .player-btn {
    padding: 5px 10px;
    border-radius: 20px;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    font-size: 11px;
    color: rgba(255,255,255,0.7);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 5px;
    transition: .15s;
    backdrop-filter: blur(4px);
  }
  .player-btn:hover, .player-btn.open {
    background: rgba(255,255,255,0.18);
    border-color: rgba(255,255,255,0.5);
    color: #fff;
  }
  .player-btn span {
    white-space: nowrap;
    overflow: visible;
    text-overflow: ellipsis;
    max-width: 130px;
  }

  .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: ${isPlay ? "#69f0ae" : "rgba(255,255,255,0.3)"};
    flex-shrink: 0;
  }

  .pdrop {
    position: absolute;
    left: 18px; right: 18px;
    bottom: calc(100% + 8px);
    background: rgba(10,30,20,0.97);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 14px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    z-index: 999;
    overflow: visible;
    max-height: 200px;
    overflow-y: auto;
    backdrop-filter: blur(16px);
  }

  svg { flex-shrink: 0; color: rgba(255,255,255,0.6); }
</style>

<ha-card class="card">
  <div class="bg"></div>
  <div class="overlay"></div>
  <div class="content">

    <div class="top">
      <div class="info">
        <div class="title">
          ${isLive
            ? (this._lang==="ar" ? "إذاعة القرآن الكريم" : "Saudi Quran Radio")
            : (this._lang==="ar" ? surahAr : surahEn)}
          ${isLive ? '<span class="live-dot"></span>' : ""}
        </div>
        <div class="sub">
          ${isLive
            ? (this._lang==="ar" ? "بث مباشر · السعودية" : "Live · Saudi Arabia")
            : (this._lang==="ar" ? reciterAr : reciterEn)}
        </div>
      </div>
      <span class="status">${isPlay ? this._t("يشتغل","Playing") : this._t("وقف","Stopped")}</span>
      <div class="controls">
        <button class="btn-play" id="btn-play">${isPlay ? "⏸" : "▶"}</button>
        <button class="btn-icon" id="btn-next" title="${this._t("التالية","Next")}">⏭</button>
        <button class="btn-lang" id="btn-lang">${this._lang==="ar"?"EN":"عر"}</button>
      </div>
    </div>

    <div class="divider"></div>

    <div class="bottom">
      <button class="sel-btn ${this._showSurah?"open":""}" id="surah-btn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
          <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
        </svg>
        <span>${this._t("السورة","Surah")}: ${this._lang==="ar"?surahAr:surahEn}</span>
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="6 9 12 15 18 9"/>
        </svg>
      </button>

      <button class="sel-btn ${this._showReciter?"open":""}" id="reciter-btn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
          <line x1="12" y1="19" x2="12" y2="23"/>
          <line x1="8" y1="23" x2="16" y2="23"/>
        </svg>
        <span>${this._t("القارئ","Reciter")}: ${this._lang==="ar"?reciterAr:reciterEn}</span>
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="6 9 12 15 18 9"/>
        </svg>
      </button>

      <button class="btn-live ${isLive?"active":""}" id="btn-live">
        📻 ${this._t("إذاعة","Live")}
      </button>

      ${this._showSurah ? `
      <div class="dropdown">
        <div class="list-surah">
          ${surahs.map(s => `
            <div class="item ${s===surah?"sel":""}" data-surah="${s}">
              ${s.split("|")[this._lang==="ar"?0:1]?.trim()??s}
            </div>`).join("")}
        </div>
      </div>` : ""}

      ${this._showReciter ? `
      <div class="dropdown reciter">
        <div class="list-reciter">
          ${reciters.map(r => `
            <div class="item ${r===reciter?"sel":""}" data-reciter="${r}">
              ${r.split("|")[this._lang==="ar"?0:1]?.trim()??r}
            </div>`).join("")}
        </div>
      </div>` : ""}
    </div>

    <div class="divider"></div>

    <div class="player-row">
      <button class="player-btn ${this._showPlayer?"open":""}" id="player-btn">
        <span class="dot"></span>
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
          <path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>
        </svg>
        <span>${playerShort}</span>
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="6 9 12 15 18 9"/>
        </svg>
      </button>

      ${this._showPlayer ? `
      <div class="pdrop">
        <div class="list-player">
          ${players.map(p => `
            <div class="item ${p===player?"sel":""}" data-player="${p}">
              🔊 ${p.replace("media_player.","")}
            </div>`).join("")}
        </div>
      </div>` : ""}
    </div>

  </div>
</ha-card>`;

    this._restoreScroll();
    this._attachEvents(isPlay, isLive, surahs, surah, player);
  }

  _attachEvents(isPlay, isLive, surahs, surah, player) {

    this.shadowRoot.getElementById("btn-play")?.addEventListener("click", () => {
      if (isPlay) {
        this._call("media_player","media_stop",{entity_id:"media_player.player"});
      } else {
        this._call("media_player","media_play",{entity_id:"media_player.player"});
      }
    });

    this.shadowRoot.getElementById("btn-next")?.addEventListener("click", () => {
      const currentNum = this._attr("current_surah_number") ?? 1;
      const nextNum = currentNum >= 114 ? 1 : currentNum + 1;
      const allSurahs = this._attr("sound_mode_list") ?? [];
      const nextSurahName = allSurahs[nextNum - 1];
      if (nextSurahName) {
        this._call("media_player","select_sound_mode",{
          entity_id:"media_player.player",
          sound_mode: nextSurahName
        });
        setTimeout(() => {
          this._call("media_player","media_play",{entity_id:"media_player.player"});
        }, 400);
      }
    });

    this.shadowRoot.getElementById("btn-live")?.addEventListener("click", () => {
      if (isLive && isPlay) {
        this._call("media_player","media_stop",{entity_id:"media_player.player"});
      } else {
        this._call("quran_media","play_live",{
          stream:"📻 إذاعة القرآن الكريم - السعودية | Saudi Quran Radio"
        });
      }
    });

    this.shadowRoot.getElementById("btn-lang")?.addEventListener("click", () => {
      this._lang = this._lang==="ar" ? "en" : "ar";
      this._render();
    });

    this.shadowRoot.getElementById("surah-btn")?.addEventListener("click", () => {
      this._showSurah = !this._showSurah;
      this._showReciter = false;
      this._showPlayer = false;
      this._listScrollSurah = 0;
      this._render();
      setTimeout(() => {
        const sel = this.shadowRoot.querySelector(".list-surah .item.sel");
        if (sel) sel.scrollIntoView({block:"center"});
      }, 50);
    });

    this.shadowRoot.getElementById("reciter-btn")?.addEventListener("click", () => {
      this._showReciter = !this._showReciter;
      this._showSurah = false;
      this._showPlayer = false;
      this._listScrollReciter = 0;
      this._render();
      setTimeout(() => {
        const sel = this.shadowRoot.querySelector(".list-reciter .item.sel");
        if (sel) sel.scrollIntoView({block:"center"});
      }, 50);
    });

    this.shadowRoot.getElementById("player-btn")?.addEventListener("click", () => {
      this._showPlayer = !this._showPlayer;
      this._showSurah = false;
      this._showReciter = false;
      this._render();
    });

    this.shadowRoot.querySelectorAll("[data-surah]").forEach(el => {
      el.addEventListener("click", () => {
        this._call("media_player","select_sound_mode",{
          entity_id:"media_player.player",
          sound_mode: el.dataset.surah
        });
        setTimeout(() => {
          this._call("media_player","media_play",{entity_id:"media_player.player"});
        }, 400);
        this._showSurah = false;
        this._render();
      });
    });

    this.shadowRoot.querySelectorAll("[data-reciter]").forEach(el => {
      el.addEventListener("click", () => {
        this._call("media_player","select_source",{
          entity_id:"media_player.player",
          source: el.dataset.reciter
        });
        setTimeout(() => {
          this._call("media_player","media_play",{entity_id:"media_player.player"});
        }, 400);
        this._showReciter = false;
        this._render();
      });
    });

    this.shadowRoot.querySelectorAll("[data-player]").forEach(el => {
      el.addEventListener("click", () => {
        // إيقاف البلير القديم أولاً
        if (player && player !== el.dataset.player) {
          this._call("media_player","media_stop",{entity_id: player});
        }
        this._call("quran_media","select_player",{player: el.dataset.player});
        this._showPlayer = false;
        this._render();
      });
    });

    this.shadowRoot.querySelector(".list-surah")?.addEventListener("scroll", e => {
      this._listScrollSurah = e.target.scrollTop;
    });
    this.shadowRoot.querySelector(".list-reciter")?.addEventListener("scroll", e => {
      this._listScrollReciter = e.target.scrollTop;
    });
  }
}

customElements.define("quran-media-player-card", QuranMediaPlayerCard);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "quran-media-player-card",
  name: "Quran Media Player",
  description: "مشغل القرآن الكريم | Holy Quran Media Player",
});
