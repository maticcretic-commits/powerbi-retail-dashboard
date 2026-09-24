#!/usr/bin/env python3
"""Render dashboard-mockup.png — the Power BI layout concept for this repo.

KPI numbers are computed from data/retail_sales.csv, so the mockup
reflects the actual dataset. This is a layout mockup (matplotlib), not a
.pbix export — the real build happens in Power BI Desktop using
data-model.md and dax-measures.dax.

Run: python3 make_mockup.py
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.ticker as mticker

df = pd.read_csv("data/retail_sales.csv", parse_dates=["Date"])
df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()

total_rev = df["Revenue"].sum()
orders = len(df)
avg_basket = total_rev / orders
monthly = df.groupby("Month")["Revenue"].sum()
mom = (monthly.iloc[-1] - monthly.iloc[-2]) / monthly.iloc[-2]

NAVY, ACCENT, GREY, LIGHT = "#1F3864", "#2E75B6", "#595959", "#F2F2F2"

fig = plt.figure(figsize=(16, 9), facecolor="white")
fig.text(0.03, 0.94, "Retail Sales Dashboard", fontsize=22,
         fontweight="bold", color=NAVY)
fig.text(0.03, 0.905, "Power BI concept  •  data: retail_sales.csv  •  Jan 2024 – Sep 2025",
         fontsize=11, color=GREY)

# KPI cards
kpis = [
    ("Total Revenue", f"Rs {total_rev / 1e7:.2f} Cr"),
    ("Total Orders", f"{orders:,}"),
    ("Avg Basket Size", f"Rs {avg_basket:,.0f}"),
    ("MoM Growth", f"{mom:+.1%}"),
]
for i, (label, value) in enumerate(kpis):
    ax = fig.add_axes([0.03 + i * 0.24, 0.78, 0.21, 0.10])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02",
                                facecolor=LIGHT, edgecolor=ACCENT,
                                linewidth=1.5))
    ax.text(0.5, 0.62, value, ha="center", va="center", fontsize=20,
            fontweight="bold", color=NAVY)
    ax.text(0.5, 0.28, label, ha="center", va="center", fontsize=11,
            color=GREY)

# Monthly revenue trend
ax1 = fig.add_axes([0.05, 0.42, 0.55, 0.30])
ax1.plot(monthly.index, monthly.values / 1e5, color=ACCENT, linewidth=2.5)
ax1.fill_between(monthly.index, monthly.values / 1e5, alpha=0.15,
                 color=ACCENT)
ax1.set_title("Monthly Revenue (Rs lakh)", fontsize=13, fontweight="bold",
              color=NAVY, loc="left")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}"))
ax1.grid(alpha=0.3)
for s in ("top", "right"):
    ax1.spines[s].set_visible(False)

# Revenue by category
cat = df.groupby("Category")["Revenue"].sum().sort_values()
ax2 = fig.add_axes([0.66, 0.42, 0.29, 0.30])
ax2.barh(cat.index, cat.values / 1e5, color=[ACCENT, "#5B9BD5", "#9DC3E6"])
ax2.set_title("Revenue by Category (Rs lakh)", fontsize=13,
              fontweight="bold", color=NAVY, loc="left")
for s in ("top", "right"):
    ax2.spines[s].set_visible(False)

# Channel share donut
ch = df.groupby("Channel")["Revenue"].sum()
ax3 = fig.add_axes([0.05, 0.06, 0.27, 0.30])
wedges, _, autotexts = ax3.pie(
    ch.values, labels=ch.index, autopct="%1.0f%%",
    colors=[ACCENT, "#9DC3E6"], startangle=90,
    wedgeprops=dict(width=0.45, edgecolor="white"))
ax3.set_title("Revenue by Channel", fontsize=13, fontweight="bold",
              color=NAVY, loc="left")

# Top products
top = df.groupby("Product")["Revenue"].sum().nlargest(5).sort_values()
ax4 = fig.add_axes([0.38, 0.06, 0.57, 0.30])
ax4.barh(top.index, top.values / 1e5, color=NAVY)
ax4.set_title("Top 5 Products by Revenue (Rs lakh)", fontsize=13,
              fontweight="bold", color=NAVY, loc="left")
for s in ("top", "right"):
    ax4.spines[s].set_visible(False)

fig.text(0.03, 0.02,
         "Build this for real in Power BI Desktop: import retail_sales.csv, "
         "apply data-model.md, paste dax-measures.dax.",
         fontsize=10, color=GREY, style="italic")
fig.savefig("dashboard-mockup.png", dpi=130, bbox_inches="tight",
            facecolor="white")
print("Wrote dashboard-mockup.png")
