import matplotlib.pyplot as plt
import json
from aquarel import load_theme
from pathlib import Path
from datetime import datetime
import numpy as np
import matplotlib.dates as mdates
from collections import defaultdict
import warnings
from matplotlib.figure import Figure
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image


warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")


# cs_CZ  9896ba3c28b84b1357d877695e834e565f8d8c88
# de_DE  6b324d124379bd762502125f7ee3b3932896b6ec
# es_ES  aa873db268a961fddd0b8723e8e7d3cd9e045831
# fr_FR  aa873db268a961fddd0b8723e8e7d3cd9e045831
# hu_HU  e63147f2fe72ee3121e876797226dc670b6b498c
# it_IT  eb31eb851b5c9525b13069fb2fe9f832b4293964
# ja_JP  9b7e0c38c26ad0493fce8ca2fdca80ff5dd9df12
# mn_MN  f6a84489eb769da27b4d3cccaeaf27f326cd902e
# pl_PL  5bd3d3adf88ba1afaf1e7916c0273b9719947353
# pt_BR  5f64c2e6b44159145296f6d2824c2c6db638f653
# sv_SE  e6e95b61c77da6cca4039c3918fffa916a81b384
# tr_TR  05939f80d15108586a1db7e1c66d98c3b03ff4eb
# uk_UA  69f7cc3141bcdd360ff8ce1be5918e22d065f964
# zh_Hans_CN  dcbe9e71e2d4415ac57df1e28efc76ef93da1902


# 9896ba3c28b84b1357d877695e834e565f8d8c88
# 6b324d124379bd762502125f7ee3b3932896b6ec
# aa873db268a961fddd0b8723e8e7d3cd9e045831
# aa873db268a961fddd0b8723e8e7d3cd9e045831
# e63147f2fe72ee3121e876797226dc670b6b498c
# eb31eb851b5c9525b13069fb2fe9f832b4293964
# 9b7e0c38c26ad0493fce8ca2fdca80ff5dd9df12
# f6a84489eb769da27b4d3cccaeaf27f326cd902e
# 5bd3d3adf88ba1afaf1e7916c0273b9719947353
# 5f64c2e6b44159145296f6d2824c2c6db638f653
# e6e95b61c77da6cca4039c3918fffa916a81b384
# 05939f80d15108586a1db7e1c66d98c3b03ff4eb
# 69f7cc3141bcdd360ff8ce1be5918e22d065f964
# dcbe9e71e2d4415ac57df1e28efc76ef93da1902

# 2023-06-27 14:09:48 +0200
# 2022-08-23 11:14:44 +0200
# 2014-10-09 16:29:49 +0200
# 2014-10-09 16:29:49 +0200
# 2024-06-20 10:50:56 +0200
# 2023-10-05 12:14:09 +0200
# 2024-09-23 12:10:47 +0200
# 2021-04-16 14:09:44 +0200
# 2021-04-12 15:52:13 +0200
# 2019-06-07 14:00:28 +0200
# 2024-08-30 15:04:36 +0200
# 2021-06-25 13:40:41 +0200
# 2021-01-08 14:00:11 +0100
# 2020-08-10 17:15:53 +0200


# git bisect reset && git bisect start && git bisect bad HEAD && git bisect good 9033fd434a093dfdd0fd4064035868e5535e8d5d && git bisect run ../indico-presentations/stats/bisect.py


formatter = mdates.DateFormatter("%Y")  ### formatter of the date
locator = mdates.YearLocator()


translations = json.loads(Path("translations.json").read_text())
dates = [datetime.fromisoformat(dt) for dt in translations["dates"]]
languages = translations["languages"]

dates_languages = sorted(zip(dates, languages), key=lambda x: x[0])
levels = [
    0.7,
    -0.7,
    0.7,
    -0.2,
    0.7,
    -0.7,
    0.7,
    -0.7,
    0.7,
    -0.2,
]
full_levels = [1, -1] * 5

date_map = defaultdict(list)
for dt, lang in dates_languages:
    date_map[dt].append(lang)


# "cs_CZ",
# "de_DE",
# "hu_HU",
# "it_IT",
# "ja_JP",
# "mn_MN",
# "pl_PL",
# "pt_BR",
# "sv_SE",
# "tr_TR",
# "uk_UA",
# "zh_Hans_CN"

images = (
    "cs.png",
    "de.png",
    "hu.png",
    "it.png",
    "ja.png",
    "mn.png",
    "pl.png",
    "pt.png",
    "sv.png",
    "tr.png",
    "uk.png",
    "zh.png",
)


def plot():
    # Plot when laguages were added
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_title("Supported Languages Over Time")
    ax.xaxis.set(
        major_locator=mdates.YearLocator(), major_formatter=mdates.DateFormatter("%Y")
    )
    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)
    ax.spines["bottom"].set_position("center")
    ax.set_axisbelow(True)

    ax.vlines(
        list(date_map.keys()),
        0,
        levels,
        color=[("tab:red", 1) for dt in date_map.keys()],
        zorder=200000,
    )
    ax.vlines(
        list(date_map.keys()),
        0,
        full_levels,
        color=[("none", 1) for dt in date_map.keys()],
        zorder=200000,
    )
    # The baseline.
    # ax.axhline(0, c="black")
    ax.plot(
        list(date_map.keys()),
        np.zeros_like(list(date_map.keys())),
        "ko",
        mfc="tab:red",
        markersize=8,
        zorder=200000,
    )
    ax.plot(
        list(date_map.keys()), levels, "ko", mfc="tab:red", markersize=8, zorder=200000
    )

    for date, level, lang in zip(date_map.keys(), full_levels, date_map.values()):
        print(f"{date}: {lang} {level}")
        _lang = "+".join([lg[:2] for lg in lang])
        ax.annotate(
            _lang,
            xy=(date, level),
            xytext=(-3, np.sign(level) * 3),
            textcoords="offset points",
            verticalalignment="bottom" if level > 0 else "top",
            # fontname="Noto Color Emoji",
        )
        lg = lang[0][:2]
        filename = f"../assets/slides/stats/{lg}.png"
        arr_img = Image.open(filename)
        arr_img = np.array(arr_img)
        im = OffsetImage(arr_img)
        ab = AnnotationBbox(
            im,
            xy=(date, level),
            pad=0,
            bboxprops=dict(facecolor=[0, 0, 0, 0], edgecolor="none"),
        )
        ax.add_artist(ab)

        if len(lang) > 1:
            lg = lang[1][:2]
            filename = f"../assets/slides/stats/{lg}.png"
            arr_img = Image.open(filename)
            arr_img = np.array(arr_img)
            im = OffsetImage(arr_img)
            ab = AnnotationBbox(
                im,
                xy=(date, level - np.sign(level) * 0.5),
                pad=0,
                bboxprops=dict(facecolor=[0, 0, 0, 0], edgecolor="none"),
            )
            ax.add_artist(ab)

    for lang, dt, offset in zip(
        ("en", "fr", "es"),
        ((2019, 6, 1), (2019, 10, 1), (2020, 2, 1)),
        (-1.6, -1.6, -1.6),
    ):
        filename = f"../assets/slides/stats/{lang}.png"
        arr_img = Image.open(filename)
        half = 0.7
        arr_img = arr_img.resize([int(half * s) for s in arr_img.size])
        arr_img = np.array(arr_img)
        im = OffsetImage(arr_img)
        ab = AnnotationBbox(
            im,
            xy=(datetime(*dt), offset),
            pad=0,
            bboxprops=dict(facecolor=[0, 0, 0, 0], edgecolor="none"),
        )
        ax.add_artist(ab)

    # plt.subplots_adjust(top=0.5)
    ax.set_ymargin(0.3)
    fig.tight_layout()
    plt.savefig(
        "../assets/slides/stats/translations_over_time.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()
    # print(date_map)


with load_theme("gruvbox_dark"):
    plot()
