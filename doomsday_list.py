"""
DOOMSDAY LIST — Road to Avengers: Doomsday
Run: streamlit run doomsday_list.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import base64
import re

MCU_DATA = [
    # Phase One
    {"title": "Iron Man", "type": "Movie", "phase": "Phase One", "release_date": "2008-05-02"},
    {"title": "The Incredible Hulk", "type": "Movie", "phase": "Phase One", "release_date": "2008-06-13"},
    {"title": "Iron Man 2", "type": "Movie", "phase": "Phase One", "release_date": "2010-05-07"},
    {"title": "Thor", "type": "Movie", "phase": "Phase One", "release_date": "2011-05-06"},
    {"title": "Captain America: The First Avenger", "type": "Movie", "phase": "Phase One", "release_date": "2011-07-22"},
    {"title": "The Avengers", "type": "Movie", "phase": "Phase One", "release_date": "2012-05-04"},

    # Phase Two
    {"title": "Iron Man 3", "type": "Movie", "phase": "Phase Two", "release_date": "2013-05-03"},
    {"title": "Thor: The Dark World", "type": "Movie", "phase": "Phase Two", "release_date": "2013-11-08"},
    {"title": "Daredevil", "type": "Show", "phase": "Phase Two", "release_date": "2015-04-10"},
    {"title": "Captain America: The Winter Soldier", "type": "Movie", "phase": "Phase Two", "release_date": "2014-04-04"},
    {"title": "Guardians of the Galaxy", "type": "Movie", "phase": "Phase Two", "release_date": "2014-08-01"},
    {"title": "Avengers: Age of Ultron", "type": "Movie", "phase": "Phase Two", "release_date": "2015-05-01"},
    {"title": "Ant-Man", "type": "Movie", "phase": "Phase Two", "release_date": "2015-07-17"},

    # Phase Three
    {"title": "Captain America: Civil War", "type": "Movie", "phase": "Phase Three", "release_date": "2016-05-06"},
    {"title": "Doctor Strange", "type": "Movie", "phase": "Phase Three", "release_date": "2016-11-04"},
    {"title": "Guardians of the Galaxy Vol. 2", "type": "Movie", "phase": "Phase Three", "release_date": "2017-05-05"},
    {"title": "Spider-Man: Homecoming", "type": "Movie", "phase": "Phase Three", "release_date": "2017-07-07"},
    {"title": "Thor: Ragnarok", "type": "Movie", "phase": "Phase Three", "release_date": "2017-11-03"},
    {"title": "Black Panther", "type": "Movie", "phase": "Phase Three", "release_date": "2018-02-16"},
    {"title": "Avengers: Infinity War", "type": "Movie", "phase": "Phase Three", "release_date": "2018-04-27"},
    {"title": "Ant-Man and the Wasp", "type": "Movie", "phase": "Phase Three", "release_date": "2018-07-06"},
    {"title": "Captain Marvel", "type": "Movie", "phase": "Phase Three", "release_date": "2019-03-08"},
    {"title": "Avengers: Endgame", "type": "Movie", "phase": "Phase Three", "release_date": "2019-04-26"},
    {"title": "Spider-Man: Far From Home", "type": "Movie", "phase": "Phase Three", "release_date": "2019-07-02"},

    # Phase Four
    {"title": "WandaVision (Not important)", "type": "Show", "phase": "Phase Four", "release_date": "2021-01-15"},
    {"title": "The Falcon and the Winter Soldier", "type": "Show", "phase": "Phase Four", "release_date": "2021-03-19"},
    {"title": "Loki (Season 1)", "type": "Show", "phase": "Phase Four", "release_date": "2021-06-09"},
    {"title": "Black Widow", "type": "Movie", "phase": "Phase Four", "release_date": "2021-07-09"},
    {"title": "What If...? (Season 1) (not important)", "type": "Show", "phase": "Phase Four", "release_date": "2021-08-11"},
    {"title": "Shang-Chi and the Legend of the Ten Rings", "type": "Movie", "phase": "Phase Four", "release_date": "2021-09-03"},
    {"title": "Eternals", "type": "Movie", "phase": "Phase Four", "release_date": "2021-11-05"},
    {"title": "Hawkeye", "type": "Show", "phase": "Phase Four", "release_date": "2021-11-24"},
    {"title": "Spider-Man: No Way Home", "type": "Movie", "phase": "Phase Four", "release_date": "2021-12-17"},
    {"title": "Moon Knight", "type": "Show", "phase": "Phase Four", "release_date": "2022-03-30"},
    {"title": "Doctor Strange in the Multiverse of Madness", "type": "Movie", "phase": "Phase Four", "release_date": "2022-05-06"},
    {"title": "Ms. Marvel", "type": "Show", "phase": "Phase Four", "release_date": "2022-06-08"},
    {"title": "Thor: Love and Thunder", "type": "Movie", "phase": "Phase Four", "release_date": "2022-07-08"},
    {"title": "She-Hulk: Attorney at Law (not important, watch a YouTube summary)", "type": "Show", "phase": "Phase Four", "release_date": "2022-08-18"},
    {"title": "Werewolf by Night (Special)", "type": "Show", "phase": "Phase Four", "release_date": "2022-10-07"},
    {"title": "Black Panther: Wakanda Forever", "type": "Movie", "phase": "Phase Four", "release_date": "2022-11-11"},
    {"title": "Guardians of the Galaxy Holiday Special", "type": "Show", "phase": "Phase Four", "release_date": "2022-11-25"},

    # Phase Five
    {"title": "Ant-Man and the Wasp: Quantumania", "type": "Movie", "phase": "Phase Five", "release_date": "2023-02-17"},
    {"title": "Secret Invasion (watch a summary)", "type": "Show", "phase": "Phase Five", "release_date": "2023-06-21"},
    {"title": "Guardians of the Galaxy Vol. 3", "type": "Movie", "phase": "Phase Five", "release_date": "2023-05-05"},
    {"title": "Loki (Season 2)", "type": "Show", "phase": "Phase Five", "release_date": "2023-10-06"},
    {"title": "The Marvels", "type": "Movie", "phase": "Phase Five", "release_date": "2023-11-10"},
    {"title": "Echo (Not important)", "type": "Show", "phase": "Phase Five", "release_date": "2024-01-09"},
    {"title": "Agatha All Along (skip)", "type": "Show", "phase": "Phase Five", "release_date": "2024-09-18"},
    {"title": "Deadpool & Wolverine", "type": "Movie", "phase": "Phase Five", "release_date": "2024-07-26"},
    {"title": "What If...? (Season 3) (skip)", "type": "Show", "phase": "Phase Five", "release_date": "2024-12-22"},
    {"title": "Captain America: Brave New World", "type": "Movie", "phase": "Phase Five", "release_date": "2025-02-14"},
    {"title": "Daredevil: Born Again", "type": "Show", "phase": "Phase Five", "release_date": "2025-03-04"},
    {"title": "Thunderbolts*", "type": "Movie", "phase": "Phase Five", "release_date": "2025-05-02"},
    {"title": "Ironheart (skip)", "type": "Show", "phase": "Phase Five", "release_date": "2025-06-24"},

    # Phase Six (as announced)
    {"title": "The Fantastic Four: First Steps", "type": "Movie", "phase": "Phase Six", "release_date": "2025-07-25"},
    {"title": "Spider-Man: Brand New Day", "type": "Movie", "phase": "Phase Six", "release_date": "2026-07-31"},
    {"title": "Avengers: Doomsday", "type": "Movie", "phase": "Phase Six", "release_date": "2026-12-18"},
    {"title": "Avengers: Secret Wars", "type": "Movie", "phase": "Phase Six", "release_date": "2027-12-17"},

    # X-Men Legacy (Fox) — background viewing for Avengers: Doomsday.
    # Marvel confirmed the original Fox-era cast (Patrick Stewart as Professor X,
    # Ian McKellen as Magneto, Kelsey Grammer as Beast, Rebecca Romijn as Mystique,
    # James Marsden as Cyclops, Alan Cumming as Nightcrawler) returns in Doomsday,
    # so the core original-timeline trilogy + the multiverse-crossover films are
    # the most relevant prior viewing.
    {"title": "X-Men", "type": "Movie", "phase": "X-Men Legacy (Fox)", "release_date": "2000-07-14"},
    {"title": "X2: X-Men United", "type": "Movie", "phase": "X-Men Legacy (Fox)", "release_date": "2003-05-02"},
    {"title": "X-Men: The Last Stand", "type": "Movie", "phase": "X-Men Legacy (Fox)", "release_date": "2006-05-26"},
    {"title": "X-Men Origins: Wolverine", "type": "Movie", "phase": "X-Men Legacy (Fox)", "release_date": "2009-05-01"},
    {"title": "X-Men: First Class", "type": "Movie", "phase": "X-Men Legacy (Fox)", "release_date": "2011-06-03"},
    {"title": "The Wolverine", "type": "Movie", "phase": "X-Men Legacy (Fox)", "release_date": "2013-07-26"},
    {"title": "X-Men: Days of Future Past", "type": "Movie", "phase": "X-Men Legacy (Fox)", "release_date": "2014-05-23"},
    {"title": "X-Men: Apocalypse", "type": "Movie", "phase": "X-Men Legacy (Fox)", "release_date": "2016-05-27"},
    {"title": "Logan", "type": "Movie", "phase": "X-Men Legacy (Fox)", "release_date": "2017-03-03"},
    {"title": "Deadpool", "type": "Movie", "phase": "X-Men Legacy (Fox)", "release_date": "2016-02-12"},
    {"title": "Deadpool 2", "type": "Movie", "phase": "X-Men Legacy (Fox)", "release_date": "2018-05-18"},
    {"title": "Dark Phoenix", "type": "Movie", "phase": "X-Men Legacy (Fox)", "release_date": "2019-06-07"},
    {"title": "The New Mutants", "type": "Movie", "phase": "X-Men Legacy (Fox)", "release_date": "2020-08-28"},
]

st.set_page_config(
    page_title="DOOMSDAY LIST",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

IMAGE_DIR = Path(__file__).parent / "images"
MCU_PHASES = ["Phase One", "Phase Two", "Phase Three", "Phase Four", "Phase Five", "Phase Six"]
X_MEN_PHASE = "X-Men Legacy (Fox)"

all_df = pd.DataFrame(MCU_DATA).drop_duplicates("title").reset_index(drop=True)
all_df["release_date"] = pd.to_datetime(all_df["release_date"])

# Main journey = MCU Phases 1–6 only.
df = all_df[all_df["phase"].isin(MCU_PHASES)].sort_values("release_date").reset_index(drop=True)
FULL_ORDER = df["title"].tolist()

# X-Men stays in the app, but is kept completely separate from Up Next/progress.
xmen_df = all_df[all_df["phase"] == X_MEN_PHASE].sort_values("release_date").reset_index(drop=True)

def slugify_title(title):
    return re.sub(r"[^a-zA-Z0-9]+", "_", title.lower()).strip("_")

def get_image_path(title):
    if not title:
        return None
    base = slugify_title(title)
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        p = IMAGE_DIR / (base + ext)
        if p.exists():
            return p
    return None

def image_uri(path):
    if not path:
        return None
    mime = {".jpg":"image/jpeg",".jpeg":"image/jpeg",".png":"image/png",".webp":"image/webp"}
    return "data:" + mime.get(path.suffix.lower(),"image/jpeg") + ";base64," + base64.b64encode(path.read_bytes()).decode()

def trailer_url(title):
    from urllib.parse import quote_plus
    return "https://www.youtube.com/results?search_query=" + quote_plus(
        "Marvel Studios " + title + " official trailer"
    )

if "watched" not in st.session_state:
    st.session_state.watched = set()
if "last_checked_title" not in st.session_state:
    st.session_state.last_checked_title = None
if "xmen_watched" not in st.session_state:
    st.session_state.xmen_watched = set()
if "last_checked_xmen_title" not in st.session_state:
    st.session_state.last_checked_xmen_title = None

def get_next_title(after_title):
    if not FULL_ORDER:
        return None
    if not after_title or after_title not in FULL_ORDER:
        return FULL_ORDER[0]
    i = FULL_ORDER.index(after_title)
    return FULL_ORDER[i + 1] if i + 1 < len(FULL_ORDER) else None

def get_next_xmen_title(after_title):
    order = xmen_df["title"].tolist()
    if not order:
        return None
    if not after_title or after_title not in order:
        return order[0]
    i = order.index(after_title)
    return order[i + 1] if i + 1 < len(order) else None

def on_toggle_xmen_title(title):
    checked = st.session_state.get("xchk_" + title, False)
    if checked:
        st.session_state.xmen_watched.add(title)
        st.session_state.last_checked_xmen_title = title
        nxt = get_next_xmen_title(title)
        if nxt:
            st.toast(f"X-Men next: **{nxt}** 🐺", icon="🎬")
        else:
            st.toast("You've finished the X-Men Legacy list! 🏆", icon="🎉")
    else:
        st.session_state.xmen_watched.discard(title)
        ordered = [t for t in xmen_df["title"] if t in st.session_state.xmen_watched]
        st.session_state.last_checked_xmen_title = ordered[-1] if ordered else None

def celebrate(after_title):
    nxt = get_next_title(after_title)
    if nxt:
        st.toast(f"Good girl, now watch **{nxt}** 🍿", icon="✅")
    else:
        st.toast("Good girl, you've finished the whole MCU watchlist! 🏆", icon="🎉")

def on_toggle_title(title):
    checked = st.session_state.get("chk_" + title, False)
    if checked:
        st.session_state.watched.add(title)
        st.session_state.last_checked_title = title
        celebrate(title)
    else:
        st.session_state.watched.discard(title)
        ordered = [t for t in FULL_ORDER if t in st.session_state.watched]
        st.session_state.last_checked_title = ordered[-1] if ordered else None

watched = [t for t in FULL_ORDER if t in st.session_state.watched]
watched_count = len(watched)
total_count = len(FULL_ORDER)
remaining = total_count - watched_count
progress = watched_count / total_count if total_count else 0
next_title = get_next_title(st.session_state.last_checked_title)
next_row = df[df["title"] == next_title].iloc[0] if next_title else None
next_path = get_image_path(next_title)

xmen_next_title = get_next_xmen_title(st.session_state.last_checked_xmen_title)
xmen_next_row = xmen_df[xmen_df["title"] == xmen_next_title].iloc[0] if xmen_next_title else None
xmen_next_path = get_image_path(xmen_next_title)
xmen_next_uri = image_uri(xmen_next_path)
xmen_watched_count = len([t for t in xmen_df["title"] if t in st.session_state.xmen_watched])
xmen_total_count = len(xmen_df)
next_uri = image_uri(next_path)
bg = "url('" + next_uri + "')" if next_uri else "none"

st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --red:#e50914;
    --red2:#ff3945;
    --ink:#050506;
    --panel:#0c0c0f;
    --muted:#85878d;
    --line:rgba(255,255,255,.11);
}

html, body, [class*="css"] { font-family:Inter,sans-serif; }
.stApp {
    background:
      radial-gradient(circle at 78% 18%,rgba(229,9,20,.18),transparent 30%),
      linear-gradient(180deg,#050506 0%,#09090b 48%,#050506 100%);
    color:#f4f4f1;
}
.stApp::before {
    content:"";
    position:fixed;
    inset:-6%;
    z-index:-5;
    background-image:__BG__;
    background-size:cover;
    background-position:center top;
    filter:blur(20px) saturate(1.15) brightness(.45);
    transform:scale(1.08);
    opacity:.30;
}
.stApp::after {
    content:"";
    position:fixed;
    inset:0;
    z-index:-4;
    background:
      linear-gradient(90deg,#050506 0%,rgba(5,5,6,.92) 28%,rgba(5,5,6,.55) 68%,#050506 100%),
      linear-gradient(180deg,rgba(5,5,6,.1),#050506 84%);
    pointer-events:none;
}
.block-container { max-width:1320px!important; padding:0 34px 90px!important; }
header[data-testid="stHeader"] { background:transparent!important; }
section[data-testid="stSidebar"] { background:#08080a; border-right:1px solid var(--line); }

.nav {
    height:78px; display:flex; align-items:center; justify-content:space-between;
    border-bottom:1px solid var(--line);
}
.logo {
    font-family:"Barlow Condensed"; font-size:28px; font-weight:900; letter-spacing:3px;
}
.logo b { color:var(--red); }
.navtag { color:#777980; font-size:10px; letter-spacing:2px; text-transform:uppercase; }

.hero {
    min-height:610px; display:flex; align-items:flex-end; padding:70px 0 62px;
    position:relative;
}
.hero:before {
    content:""; position:absolute; left:-5%; bottom:0; width:58%; height:2px;
    background:linear-gradient(90deg,var(--red),transparent);
}
.kicker { color:#c8c9ca; font-size:12px; font-weight:800; letter-spacing:5px; text-transform:uppercase; }
.hero h1 {
    font-family:"Barlow Condensed"; font-size:clamp(90px,14vw,190px);
    line-height:.76; letter-spacing:-5px; font-weight:900; margin:18px 0 28px;
    text-transform:uppercase;
}
.hero h1 span { color:var(--red); }
.hero p { max-width:650px; color:#9c9ea3; line-height:1.75; font-size:15px; }
.redline { width:110px; height:5px; background:var(--red); margin-top:28px; }

.next {
    min-height:520px; position:relative; overflow:hidden;
    border:1px solid rgba(255,255,255,.13); background:rgba(7,7,9,.82);
    display:grid; grid-template-columns:1.2fr .8fr;
}
.next:before {
    content:""; position:absolute; inset:0; background-image:__BG__;
    background-size:cover; background-position:center; opacity:.24;
}
.next:after {
    content:""; position:absolute; inset:0;
    background:linear-gradient(90deg,#08080a 0%,rgba(8,8,10,.90) 45%,rgba(8,8,10,.32) 100%);
}
.next-copy { position:relative; z-index:2; align-self:center; padding:65px; }
.next-kicker { color:var(--red); font-size:12px; font-weight:900; letter-spacing:4px; text-transform:uppercase; }
.next h2 {
    font-family:"Barlow Condensed"; font-size:clamp(52px,6vw,92px);
    line-height:.84; text-transform:uppercase; font-weight:900; margin:18px 0;
}
.meta { color:#999ba1; font-size:11px; letter-spacing:2px; text-transform:uppercase; }
.next-desc { max-width:540px; color:#aeb0b4; line-height:1.7; margin-top:22px; }
.poster {
    position:relative; z-index:2; display:flex; justify-content:center; align-items:center; padding:45px;
}
.poster img { width:300px; max-height:440px; object-fit:cover; box-shadow:0 35px 80px #000; border:1px solid rgba(255,255,255,.15); }
.placeholder {
    width:280px; height:400px; display:flex; align-items:center; justify-content:center;
    text-align:center; border:1px dashed #444; background:#111; color:#666; padding:25px;
}

.stats {
    display:grid; grid-template-columns:repeat(4,1fr);
    border-top:1px solid var(--line); border-bottom:1px solid var(--line);
    margin:58px 0 70px;
}
.stat { padding:28px 24px; border-right:1px solid var(--line); }
.stat:last-child { border-right:0; }
.num { font-family:"Barlow Condensed"; font-size:56px; font-weight:800; line-height:1; }
.lab { color:#73757a; font-size:10px; font-weight:800; letter-spacing:2px; text-transform:uppercase; margin-top:8px; }

.section-kicker { color:var(--red); font-size:11px; font-weight:900; letter-spacing:4px; text-transform:uppercase; }
.section-title {
    font-family:"Barlow Condensed"; font-size:68px; line-height:.85; font-weight:900;
    text-transform:uppercase; margin:8px 0 34px;
}
.phase { border-top:1px solid var(--line); padding:27px 0 10px; }
.phase-name { font-family:"Barlow Condensed"; font-size:37px; font-weight:800; text-transform:uppercase; }
.phase-count { color:#6e7075; font-size:10px; letter-spacing:2px; text-transform:uppercase; }

div[data-testid="stExpander"] {
    border:1px solid rgba(255,255,255,.09)!important;
    border-radius:0!important; background:rgba(11,11,14,.76)!important;
    margin:7px 0!important;
}
div[data-testid="stExpander"] summary { padding:18px 20px!important; }
div[data-testid="stExpander"] summary:hover { background:rgba(229,9,20,.07)!important; }
div[data-testid="stExpander"] details[open] { border-left:3px solid var(--red)!important; }

div[data-testid="stProgress"] > div { background:#202125!important; border-radius:0!important; }
div[data-testid="stProgress"] > div > div { background:var(--red)!important; border-radius:0!important; }

.stButton > button {
    border-radius:0!important; background:#111114!important; color:white!important;
    border:1px solid rgba(255,255,255,.16)!important;
}
.stButton > button:hover { border-color:var(--red)!important; }

.go-to-btn {
    display:inline-block;
    margin-top:28px;
    padding:13px 22px;
    border:1px solid var(--red);
    background:rgba(229,9,20,.12);
    color:#fff!important;
    text-decoration:none!important;
    font-size:11px;
    font-weight:900;
    letter-spacing:2px;
    text-transform:uppercase;
}
.go-to-btn:hover { background:var(--red); }

.trailer-btn {
    display:inline-block;
    margin:12px 0 18px;
    padding:11px 17px;
    border:1px solid rgba(255,255,255,.2);
    background:#111114;
    color:#fff!important;
    text-decoration:none!important;
    font-size:10px;
    font-weight:800;
    letter-spacing:1.5px;
    text-transform:uppercase;
}
.trailer-btn:hover { border-color:var(--red); background:#1a0b0d; }

.xmen-section {
    margin-top:100px;
    padding:45px 0 20px;
    border-top:1px solid rgba(229,9,20,.5);
}
.xmen-badge {
    display:inline-block;
    padding:6px 10px;
    margin-bottom:12px;
    border:1px solid rgba(229,9,20,.45);
    color:#ff5a63;
    font-size:9px;
    font-weight:900;
    letter-spacing:2px;
    text-transform:uppercase;
}
.xmen-note {
    max-width:760px;
    color:#777980;
    line-height:1.7;
    font-size:13px;
    margin-bottom:30px;
}

@media(max-width:800px) {
    .block-container { padding:0 18px 60px!important; }
    .hero { min-height:500px; }
    .hero h1 { font-size:82px; }
    .next { grid-template-columns:1fr; }
    .stats { grid-template-columns:repeat(2,1fr); }
    .stat:nth-child(2) { border-right:0; }
    .stat:nth-child(n+3) { border-top:1px solid var(--line); }
}
</style>
""".replace("__BG__", bg), unsafe_allow_html=True)

st.markdown("""
<div class="nav">
  <div class="logo">DOOMSDAY<b>LIST</b></div>
  <div class="navtag">MCU PHASES I — VI · THE ROAD TO DOOMSDAY</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div>
    <div class="kicker">The complete Marvel watch journey</div>
    <h1>ROAD TO<br><span>DOOMSDAY</span></h1>
    <div class="redline"></div>
    <p>
      Six phases. One timeline. Every chapter in this list leading toward
      <b>Avengers: Doomsday</b>. Finish a title and your destination moves forward automatically.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

if next_row is not None:
    if next_uri:
        poster = '<img src="' + next_uri + '" alt="poster">'
    else:
        poster = '<div class="placeholder">ADD POSTER TO<br><br>images/' + slugify_title(next_title) + '.jpg</div>'

    st.markdown(
        '<div class="next">'
        '<div class="next-copy">'
        '<div class="next-kicker">▸ Up Next</div>'
        '<h2>' + next_title + '</h2>'
        '<div class="meta">' + str(next_row["phase"]) + ' · ' + str(next_row["type"]) + ' · ' +
        next_row["release_date"].strftime("%B %d, %Y") + '</div>'
        '<div class="next-desc">This is your current destination. Watch it, check it off, and the road automatically advances to the next MCU chapter.</div>'
        '<a class="go-to-btn" href="#entry-' + slugify_title(next_title) + '">GO TO ↓</a>'
        '<a class="go-to-btn" href="#xmen-up-next">X-MEN LEGACY ↓</a>'
        '</div><div class="poster">' + poster + '</div></div>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="stats">'
    '<div class="stat"><div class="num">' + str(watched_count) + '</div><div class="lab">Watched</div></div>'
    '<div class="stat"><div class="num">' + str(remaining) + '</div><div class="lab">Remaining</div></div>'
    '<div class="stat"><div class="num">' + str(total_count) + '</div><div class="lab">MCU Entries</div></div>'
    '<div class="stat"><div class="num">' + str(round(progress*100)) + '%</div><div class="lab">Complete</div></div>'
    '</div>',
    unsafe_allow_html=True,
)
st.progress(progress)

st.sidebar.markdown("## FILTER THE JOURNEY")
search_term = st.sidebar.text_input("Search", placeholder="Movie or show...")
selected_type = st.sidebar.selectbox("Type", ["All", "Movie", "Show"])
selected_phases = st.sidebar.multiselect("Phases", MCU_PHASES, default=MCU_PHASES)
sort_order = st.sidebar.radio("Order", ["Oldest first", "Newest first"])

filtered = df[df["phase"].isin(selected_phases)].copy()
if selected_type != "All":
    filtered = filtered[filtered["type"] == selected_type]
if search_term:
    filtered = filtered[filtered["title"].str.contains(search_term, case=False, na=False)]
filtered = filtered.sort_values("release_date", ascending=(sort_order == "Oldest first"))

st.markdown('<div class="section-kicker">Your timeline</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">THE JOURNEY</div>', unsafe_allow_html=True)

for phase in MCU_PHASES:
    if phase not in selected_phases:
        continue
    phase_df = filtered[filtered["phase"] == phase]
    if phase_df.empty:
        continue

    phase_all = df[df["phase"] == phase].sort_values("release_date")
    phase_watched = sum(t in st.session_state.watched for t in phase_all["title"])

    st.markdown(
        '<div class="phase"><span class="phase-name">' + phase + '</span> '
        '<span class="phase-count">' + str(phase_watched) + '/' + str(len(phase_all)) + ' watched</span></div>',
        unsafe_allow_html=True,
    )

    for _, row in phase_df.iterrows():
        title = row["title"]
        icon = "🎬" if row["type"] == "Movie" else "📺"
        suffix = "  •  NEXT" if title == next_title else ""

        st.markdown(
            '<div id="entry-' + slugify_title(title) + '" style="scroll-margin-top:40px;"></div>',
            unsafe_allow_html=True,
        )
        with st.expander(
            icon + "  " + title + suffix + "  ·  " + row["release_date"].strftime("%b %d, %Y")
        ):
            left, right = st.columns([1, 2.2])
            poster_path = get_image_path(title)

            with left:
                if poster_path:
                    st.image(str(poster_path), use_container_width=True)
                else:
                    st.markdown(
                        '<div class="placeholder" style="width:100%;height:260px;">ADD IMAGE<br><br>' +
                        slugify_title(title) + '.jpg</div>',
                        unsafe_allow_html=True,
                    )

            with right:
                st.markdown("### " + title)
                st.caption(
                    row["type"] + " · " + row["phase"] + " · " +
                    row["release_date"].strftime("%B %d, %Y")
                )
                if title == next_title:
                    st.markdown("**▸ THIS IS YOUR CURRENT NEXT WATCH**")

                st.markdown(
                    '<a class="trailer-btn" href="' + trailer_url(title) +
                    '" target="_blank" rel="noopener noreferrer">WATCH TRAILER ↗</a>',
                    unsafe_allow_html=True,
                )

                st.checkbox(
                    "I've watched this",
                    value=title in st.session_state.watched,
                    key="chk_" + title,
                    on_change=on_toggle_title,
                    args=(title,),
                )

# ============================================================
# X-MEN LEGACY — ISOLATED, WITH ITS OWN TRACKER
# ============================================================
if not xmen_df.empty:
    st.markdown(
        '<div class="xmen-section">'
        '<div class="xmen-badge">Separate / background viewing</div>'
        '<div class="section-kicker">Fox Legacy</div>'
        '<div class="section-title">X-MEN LEGACY</div>'
        '<div class="xmen-note">'
        'This list has its own checklist and its own Up Next. '
        '<strong>It never affects the MCU Phase I–VI journey.</strong>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div id="xmen-up-next" style="scroll-margin-top:40px;"></div>', unsafe_allow_html=True)

    if xmen_next_row is not None:
        xposter = (
            '<img src="' + xmen_next_uri + '" alt="X-Men poster">'
            if xmen_next_uri
            else '<div class="placeholder">ADD POSTER TO<br><br>images/' + slugify_title(xmen_next_title) + '.jpg</div>'
        )
        st.markdown(
            '<div class="next">'
            '<div class="next-copy">'
            '<div class="next-kicker">▸ X-Men Up Next</div>'
            '<h2>' + xmen_next_title + '</h2>'
            '<div class="meta">X-MEN LEGACY (FOX) · ' +
            xmen_next_row["release_date"].strftime("%B %d, %Y") + '</div>'
            '<div class="next-desc">Your next X-Men Legacy chapter. This tracker advances independently from the MCU road.</div>'
            '<a class="go-to-btn" href="#xmen-entry-' + slugify_title(xmen_next_title) + '">GO TO ↓</a>'
            '</div><div class="poster">' + xposter + '</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="next"><div class="next-copy">'
            '<div class="next-kicker">▸ X-Men Up Next</div>'
            '<h2>LEGACY COMPLETE</h2>'
            '<div class="next-desc">You finished every X-Men Legacy title.</div>'
            '</div></div>',
            unsafe_allow_html=True,
        )

    st.progress(xmen_watched_count / xmen_total_count if xmen_total_count else 0)
    st.caption(f"X-Men Legacy progress: {xmen_watched_count}/{xmen_total_count}")

    for _, row in xmen_df.iterrows():
        title = row["title"]
        st.markdown(
            '<div id="xmen-entry-' + slugify_title(title) + '" style="scroll-margin-top:40px;"></div>',
            unsafe_allow_html=True,
        )
        with st.expander("🎬  " + title + "  ·  " + row["release_date"].strftime("%b %d, %Y")):
            left, right = st.columns([1, 2.2])
            poster_path = get_image_path(title)
            with left:
                if poster_path:
                    st.image(str(poster_path), use_container_width=True)
                else:
                    st.markdown(
                        '<div class="placeholder" style="width:100%;height:260px;">ADD IMAGE<br><br>' +
                        slugify_title(title) + '.jpg</div>',
                        unsafe_allow_html=True,
                    )
            with right:
                st.markdown("### " + title)
                st.caption(
                    row["type"] + " · X-Men Legacy (Fox) · " +
                    row["release_date"].strftime("%B %d, %Y")
                )
                if title == xmen_next_title:
                    st.markdown("**▸ THIS IS YOUR CURRENT X-MEN NEXT WATCH**")
                st.markdown(
                    '<a class="trailer-btn" href="' + trailer_url(title) +
                    '" target="_blank" rel="noopener noreferrer">WATCH TRAILER ↗</a>',
                    unsafe_allow_html=True,
                )
                st.checkbox(
                    "I've watched this",
                    value=title in st.session_state.xmen_watched,
                    key="xchk_" + title,
                    on_change=on_toggle_xmen_title,
                    args=(title,),
                )

st.markdown(
    '<div style="margin-top:80px;padding-top:25px;border-top:1px solid rgba(255,255,255,.1);'
    'color:#666;font-size:10px;letter-spacing:2px;text-align:center;">'
    'DOOMSDAY LIST · MCU PHASES I — VI</div>',
    unsafe_allow_html=True,
)
