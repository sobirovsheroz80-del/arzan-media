# arzan-media tools

- `reel.py` — renders a 1080x1920 text-card reel from a JSON spec (PIL + ffmpeg, Inter fonts).
  `python3 reel.py spec.json out.mp4 --cover cover.jpg`
- `week1.py` — example of a weekly pack: 7 topics x (RU, KZ), writes `out/week1/*.mp4`, covers and `manifest.json`.
  Copy it to `weekN.py`, change topics/hooks, run from this folder.

Publishing: files are served via jsDelivr, e.g.
`https://cdn.jsdelivr.net/gh/sobirovsheroz80-del/arzan-media@main/reels/week1/skolko_ru.mp4`
and scheduled through the Supermetrics `manage_social_media` tool (account 17841414526826583, ds_id IGI).

Prices used in week 1 (from the account's own posts, 26.10.2026): Beeline 4 190, Tele2 3 990, Activ 2 990, Altel 2 990, Activ Unlim 1 690 ₸/month. Confirm with the owner before reusing.
Rules: no voice-over (owner rejected synthetic voices); no third-party music; keyword CTA "ТАРИФ" -> WhatsApp; never mention Turkestan; tariff without calls is called "Unlim".
