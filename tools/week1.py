#!/usr/bin/env python3
"""Week 1 content pack for arzantarifkz: 7 topics x (RU, KZ) = 14 silent reels + covers + captions."""
import json, os, subprocess, sys
OUT = "out/week1"; os.makedirs(OUT, exist_ok=True)

Y = "#F5C400"; G = "#AAAAAA"; K = "#141414"
def H(t, size=112, color=None, gap=6):   # headline line
    d = {"t": t, "size": size, "weight": "black", "gap": gap};
    if color: d["color"] = color
    return d
def S(t, size=52, gap=14, color=G):      # small line
    return {"t": t, "size": size, "weight": "medium", "color": color, "gap": gap}
def PILL(t, size=60, gap=56): return {"t": t, "size": size, "weight": "bold", "color": K, "pill": Y, "pad": 18, "gap": gap}
def ROW(l, r, gap=30): return {"l": l, "r": r, "size": 84, "weight": "bold", "rsize": 92, "gap": gap}

PRICES = [ROW("Beeline", "4 190 ₸"), ROW("Tele2", "3 990 ₸"), ROW("Activ", "2 990 ₸"), ROW("Altel", "2 990 ₸", 52)]
def CTA(lang):
    if lang == "ru":
        return {"min": 4.2, "lines": [H("Напишите", 84), {"t": "ТАРИФ", "size": 150, "weight": "black", "color": K, "pill": Y, "pad": 18, "gap": 24},
                H("в WhatsApp", 84, gap=60), S("подключаем онлайн по всему Казахстану", 46), S("arzantarif.kz", 46, color=Y)]}
    return {"min": 4.2, "lines": [H("WhatsApp-қа", 84), {"t": "ТАРИФ", "size": 150, "weight": "black", "color": K, "pill": Y, "pad": 18, "gap": 24},
            H("деп жазыңыз", 84, gap=60), S("бүкіл Қазақстан бойынша онлайн қосамыз", 44), S("arzantarif.kz", 46, color=Y)]}
def TABLE(title, foot, mins=4.6):
    return {"min": mins, "lines": [PILL(title)] + PRICES + [S(foot, 48)]}
def UNLIM(foot): return {"min": 3.0, "lines": [{"t": "Activ Unlim", "size": 96, "weight": "extrabold", "gap": 20}, H("1 690 ₸", 190, Y, 36), S(foot, 50)]}

T = []  # (slug, lang, scenes, caption)
# 2. Сколько платишь
T.append(("skolko", "ru", [
  {"min": 3.0, "lines": [H("Сколько ты платишь"), H("за связь?", color=Y, gap=48), S("честно, в месяц")]},
  {"min": 3.0, "lines": [H("Больше 3 000 ₸?", 110, gap=40), H("Ты переплачиваешь", 92, Y)]},
  TABLE("Семейный тариф", "в месяц"), CTA("ru")],
  "Сколько вы платите за связь в месяц? Если больше 3 000 ₸, скорее всего, переплачиваете. Семейный тариф: Beeline 4 190 ₸, Tele2 3 990 ₸, Activ и Altel 2 990 ₸.\n\nНапишите ТАРИФ в WhatsApp, подключим онлайн по всему Казахстану. Ссылка в профиле.\n\n#тарифы #тарифыказахстан #связь #beeline #tele2 #activ #altel"))
T.append(("skolko", "kz", [
  {"min": 3.0, "lines": [H("Байланысқа қанша"), H("төлейсіз?", color=Y, gap=48), S("шынын айтқанда, айына")]},
  {"min": 3.0, "lines": [H("3 000 ₸-ден көп пе?", 104, gap=40), H("Артық төлейсіз", 92, Y)]},
  TABLE("Отбасылық тариф", "айына"), CTA("kz")],
  "Байланысқа айына қанша төлейсіз? 3 000 ₸-ден көп болса, артық төлеп жүрген боларсыз. Отбасылық тариф: Beeline 4 190 ₸, Tele2 3 990 ₸, Activ және Altel 2 990 ₸.\n\nWhatsApp-қа ТАРИФ деп жазыңыз, бүкіл Қазақстан бойынша онлайн қосамыз. Сілтеме профильде.\n\n#тариф #тарифтер #байланыс #beeline #tele2 #activ #altel"))
# 3. Только интернет
T.append(("unlim", "ru", [
  {"min": 3.0, "lines": [H("Нужен только"), H("интернет?", color=Y, gap=48), S("без звонков и лишнего")]},
  UNLIM("в месяц"),
  {"min": 2.6, "lines": [H("Подключим", 100, gap=20), H("за один день", 100, Y, 40), S("через WhatsApp", 50)]},
  CTA("ru")],
  "Нужен только интернет? Activ Unlim — 1 690 ₸ в месяц, тариф без звонков. Подключаем через WhatsApp, по всему Казахстану.\n\nНапишите ТАРИФ в WhatsApp. Ссылка в профиле.\n\n#activ #unlim #тарифы #интернет #тарифыказахстан"))
T.append(("unlim", "kz", [
  {"min": 3.0, "lines": [H("Тек интернет"), H("керек пе?", color=Y, gap=48), S("қоңыраусыз, артық ештеңесіз")]},
  UNLIM("айына"),
  {"min": 2.6, "lines": [H("Бір күнде", 100, gap=20), H("қосамыз", 100, Y, 40), S("WhatsApp арқылы", 50)]},
  CTA("kz")],
  "Тек интернет керек пе? Activ Unlim — айына 1 690 ₸, қоңыраусыз тариф. WhatsApp арқылы бүкіл Қазақстан бойынша қосамыз.\n\nWhatsApp-қа ТАРИФ деп жазыңыз. Сілтеме профильде.\n\n#activ #unlim #тариф #интернет #тарифтер"))
# 4. Какой оператор (вовлечение)
T.append(("operator", "ru", [
  {"min": 3.0, "lines": [H("Какой у тебя"), H("оператор?", color=Y, gap=48), S("Beeline, Tele2, Activ или Altel")]},
  {"min": 3.4, "lines": [H("Напиши в комментарии", 90, gap=40), H("подскажем тариф дешевле", 72, Y)]},
  TABLE("Семейный тариф", "в месяц", 4.0), CTA("ru")],
  "Какой у вас оператор? Напишите в комментариях — подскажем тариф дешевле вашего. Beeline 4 190 ₸, Tele2 3 990 ₸, Activ и Altel 2 990 ₸ в месяц.\n\nИли сразу напишите ТАРИФ в WhatsApp, ссылка в профиле.\n\n#тарифы #оператор #beeline #tele2 #activ #altel #казахстан"))
T.append(("operator", "kz", [
  {"min": 3.0, "lines": [H("Операторыңыз"), H("қандай?", color=Y, gap=48), S("Beeline, Tele2, Activ немесе Altel")]},
  {"min": 3.4, "lines": [H("Комментарийге жазыңыз", 84, gap=40), H("арзанырақ тариф ұсынамыз", 70, Y)]},
  TABLE("Отбасылық тариф", "айына", 4.0), CTA("kz")],
  "Операторыңыз қандай? Комментарийге жазыңыз — сіздікінен арзанырақ тариф ұсынамыз. Beeline 4 190 ₸, Tele2 3 990 ₸, Activ және Altel айына 2 990 ₸.\n\nНемесе бірден WhatsApp-қа ТАРИФ деп жазыңыз, сілтеме профильде.\n\n#тариф #оператор #beeline #tele2 #activ #altel #қазақстан"))
# 5. Тот же оператор, цена ниже
T.append(("same", "ru", [
  {"min": 3.2, "lines": [H("Тот же оператор.", 104, gap=20), H("Цена ниже.", 120, Y)]},
  {"min": 3.0, "lines": [S("Beeline · Tele2 · Activ · Altel", 56, gap=40, color="#FFFFFF"), H("Связь та же,", 96, gap=16), H("платишь меньше", 96, Y)]},
  TABLE("Семейный тариф", "в месяц", 4.0), CTA("ru")],
  "Тот же оператор, та же связь, цена ниже. Семейный тариф: Beeline 4 190 ₸, Tele2 3 990 ₸, Activ и Altel 2 990 ₸ в месяц.\n\nНапишите ТАРИФ в WhatsApp, подключим онлайн. Ссылка в профиле.\n\n#тарифы #экономия #beeline #tele2 #activ #altel #тарифыказахстан"))
T.append(("same", "kz", [
  {"min": 3.2, "lines": [H("Сол оператор.", 104, gap=20), H("Бағасы төмен.", 116, Y)]},
  {"min": 3.0, "lines": [S("Beeline · Tele2 · Activ · Altel", 56, gap=40, color="#FFFFFF"), H("Байланыс сол,", 96, gap=16), H("төлем аз", 96, Y)]},
  TABLE("Отбасылық тариф", "айына", 4.0), CTA("kz")],
  "Сол оператор, сол байланыс, бағасы төмен. Отбасылық тариф: Beeline 4 190 ₸, Tele2 3 990 ₸, Activ және Altel айына 2 990 ₸.\n\nWhatsApp-қа ТАРИФ деп жазыңыз, онлайн қосамыз. Сілтеме профильде.\n\n#тариф #үнемдеу #beeline #tele2 #activ #altel #тарифтер"))
# 6. Без салона
T.append(("online", "ru", [
  {"min": 3.4, "lines": [H("Без салона.", 108, gap=14), H("Без очередей.", 108, gap=14), H("Онлайн.", 120, Y)]},
  {"min": 3.2, "lines": [PILL("Как это работает", 56, 50), H("1. Пишете ТАРИФ", 72, gap=22), H("2. Выбираете оператора", 72, gap=22), H("3. Пользуетесь", 72, Y)]},
  UNLIM("в месяц"), CTA("ru")],
  "Подключить тариф можно без салона и очередей: пишете ТАРИФ в WhatsApp, выбираете оператора и пользуетесь. Работаем по всему Казахстану.\n\nСсылка на WhatsApp в профиле.\n\n#тарифы #онлайн #whatsapp #beeline #tele2 #activ #altel"))
T.append(("online", "kz", [
  {"min": 3.4, "lines": [H("Салонсыз.", 108, gap=14), H("Кезексіз.", 108, gap=14), H("Онлайн.", 120, Y)]},
  {"min": 3.2, "lines": [PILL("Қалай жұмыс істейді", 54, 50), H("1. ТАРИФ деп жазасыз", 70, gap=22), H("2. Оператор таңдайсыз", 70, gap=22), H("3. Қолданасыз", 70, Y)]},
  UNLIM("айына"), CTA("kz")],
  "Тарифті салонсыз, кезексіз қосуға болады: WhatsApp-қа ТАРИФ деп жазасыз, оператор таңдайсыз, қолданасыз. Бүкіл Қазақстан бойынша жұмыс істейміз.\n\nWhatsApp сілтемесі профильде.\n\n#тариф #онлайн #whatsapp #beeline #tele2 #activ #altel"))
# 7. Сравнение 4 операторов
T.append(("compare", "ru", [
  {"min": 3.0, "lines": [H("4 оператора."), H("Одна цена ниже.", 96, Y, 48), S("сравниваем семейный тариф")]},
  TABLE("Семейный тариф", "в месяц", 5.0),
  {"min": 2.6, "lines": [H("Самый дешёвый:", 84, gap=24), H("Activ Unlim 1 690 ₸", 92, Y)]},
  CTA("ru")],
  "Сравниваем семейный тариф у четырёх операторов: Beeline 4 190 ₸, Tele2 3 990 ₸, Activ и Altel 2 990 ₸. А если нужен только интернет, Activ Unlim — 1 690 ₸.\n\nНапишите ТАРИФ в WhatsApp, подключим онлайн. Ссылка в профиле.\n\n#тарифы #сравнение #beeline #tele2 #activ #altel #тарифыказахстан"))
T.append(("compare", "kz", [
  {"min": 3.0, "lines": [H("4 оператор."), H("Қайсысы арзан?", 100, Y, 48), S("отбасылық тарифті салыстырамыз")]},
  TABLE("Отбасылық тариф", "айына", 5.0),
  {"min": 2.6, "lines": [H("Ең арзаны:", 84, gap=24), H("Activ Unlim 1 690 ₸", 92, Y)]},
  CTA("kz")],
  "Төрт оператордың отбасылық тарифін салыстырамыз: Beeline 4 190 ₸, Tele2 3 990 ₸, Activ және Altel 2 990 ₸. Тек интернет керек болса, Activ Unlim — 1 690 ₸.\n\nWhatsApp-қа ТАРИФ деп жазыңыз, онлайн қосамыз. Сілтеме профильде.\n\n#тариф #салыстыру #beeline #tele2 #activ #altel #тарифтер"))
# 8. Напиши ТАРИФ — подберём
T.append(("podberem", "ru", [
  {"min": 3.0, "lines": [H("Не знаешь, какой"), H("тариф выбрать?", color=Y, gap=48), S("мы подберём")]},
  {"min": 3.2, "lines": [H("Скажите, сколько", 84, gap=20), H("интернета и звонков", 84, gap=20), H("нужно", 84, Y, 40), S("остальное сделаем мы", 50)]},
  TABLE("Семейный тариф", "в месяц", 4.0), CTA("ru")],
  "Не знаете, какой тариф выбрать? Скажите, сколько интернета и звонков нужно, и мы подберём. Beeline 4 190 ₸, Tele2 3 990 ₸, Activ и Altel 2 990 ₸ в месяц.\n\nНапишите ТАРИФ в WhatsApp, ссылка в профиле.\n\n#тарифы #подбортарифа #beeline #tele2 #activ #altel #казахстан"))
T.append(("podberem", "kz", [
  {"min": 3.0, "lines": [H("Қай тарифті"), H("таңдарыңызды", 100, gap=8), H("білмейсіз бе?", 100, Y, 48), S("біз таңдап береміз")]},
  {"min": 3.2, "lines": [H("Қанша интернет пен", 80, gap=20), H("қоңырау керегін", 80, gap=20), H("айтыңыз", 84, Y, 40), S("қалғанын біз жасаймыз", 50)]},
  TABLE("Отбасылық тариф", "айына", 4.0), CTA("kz")],
  "Қай тарифті таңдарыңызды білмейсіз бе? Қанша интернет пен қоңырау керегін айтыңыз, біз таңдап береміз. Beeline 4 190 ₸, Tele2 3 990 ₸, Activ және Altel айына 2 990 ₸.\n\nWhatsApp-қа ТАРИФ деп жазыңыз, сілтеме профильде.\n\n#тариф #тарифтаңдау #beeline #tele2 #activ #altel #қазақстан"))

manifest = []
for slug, lang, scenes, caption in T:
    spec = {"voice": None, "scenes": scenes}
    sp = f"{OUT}/{slug}_{lang}.json"; json.dump(spec, open(sp, "w", encoding="utf-8"), ensure_ascii=False)
    mp4 = f"{OUT}/{slug}_{lang}.mp4"; cov = f"{OUT}/{slug}_{lang}_cover.jpg"
    r = subprocess.run([sys.executable, "reel.py", sp, mp4, "--cover", cov], capture_output=True, text=True)
    info = json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 else {"error": r.stderr[-300:]}
    manifest.append({"slug": slug, "lang": lang, "file": os.path.basename(mp4), "cover": os.path.basename(cov),
                     "seconds": info.get("seconds"), "caption": caption})
    print(slug, lang, info.get("seconds"), info.get("error", ""))
json.dump(manifest, open(f"{OUT}/manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
