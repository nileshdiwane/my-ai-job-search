#!/usr/bin/env python3
"""Builds the four resume PDFs (India/US x Analytics-management/Strategy).
Edit the text below, then run:  python3 build_resumes.py
Requires Node.js with Playwright and Chromium."""
import os, pathlib, subprocess

OUT = pathlib.Path(__file__).parent

def content(region, track):
    us = region == "US"
    ise = "ize" if us else "ise"
    nat = "nationwide" if us else "PAN-India"
    ray_rev = "~US$800M" if us else "~Rs. 7,000 Cr"
    channels = ("Wholesale, multi-brand store (MBO) and exclusive-brand store (EBO) channels" if us
                else "Wholesale, MBO and EBO channels")
    mis = "sales reporting (MIS)" if us else "sales MIS"
    loc_old = "India" if us else "Mumbai"

    if track == "Analytics":
        headline = "Sales Analytics &amp; BI | Team Leadership · Executive Reporting · KPI Design"
        summary = (
            "Commercial analytics professional with close to 8 years in sales reporting and operations across food "
            "distribution, apparel retail and banking. Analytics partner to the <b>Chief of Sales at House of Spices</b> "
            "(US &amp; Canada, 11 distribution centers), owning the weekly leadership report and an automated dashboard "
            "that flags about <b>US$3M a month</b> in unmoved stock for sales managers to act on. At <b>Raymond Lifestyle</b>, "
            f"cut {nat} sales reporting from 2–3 days to under an hour for 50+ users. Earlier promoted to lead a "
            "<b>35-person MIS team</b>.")
        business = ("Sales &amp; commercial analytics · BI &amp; reporting automation · KPI frameworks &amp; target setting · "
                    "Team leadership (25–35 people) · Executive reporting · Cross-functional stakeholder management")
    else:
        headline = "Commercial Strategy &amp; Sales Analytics | Sales Performance · Executive Reporting · KPI Design"
        summary = (
            "Commercial analytics professional with close to 8 years turning sales data into leadership decisions across "
            "food distribution, apparel retail and banking. Analytics partner to the <b>Chief of Sales at House of Spices</b> "
            "(US &amp; Canada, 11 distribution centers): analysis of unmoved stock worth about <b>US$3M a month</b> led sales "
            "managers to act, with roughly 70% of it converted into sales. At <b>Raymond Lifestyle</b>, designed the "
            f"target-allocation models for {ray_rev} in sales targets. Earlier promoted to lead a <b>35-person MIS team</b>.")
        business = ("Sales &amp; commercial analytics · Revenue-risk &amp; opportunity analysis · KPI frameworks &amp; target setting · "
                    "Performance reviews · Executive storytelling · Cross-functional stakeholder management")

    hos_unmoved = ("Created an automated dashboard that flags <b>unmoved stock worth about US$3M a month</b>; sales managers "
                   "acted on the flags and converted <b>roughly 70%</b> of it into sales.")
    hos_report = ("Own the <b>weekly Sales Leadership report</b> for the Chief of Sales, turning distribution-center, team and "
                  "category data into clear calls on performance trends, sales gaps and margin opportunities across <b>11 DCs</b>.")
    hos_focus = ("Set up <b>focus-item tracking</b> for sales managers, giving them visibility of stock and slow-moving items "
                 "alongside category shortfalls, customer concentration and underperforming territories.")
    hos_dash = ("Replaced manual number-pulling in leadership reviews with a <b>sales performance dashboard</b> "
                "(revenue vs. target, cases sold, new-customer acquisition, gross profit).")
    hos_kpi = (f"Agreed KPI logic and a governed reporting framework with Sales, IT and Marketing; <b>senior IT leadership "
               f"endorsed it</b> as the base for future automation and standard{ise[:-1]}ation.")
    hos = [hos_unmoved, hos_report, hos_focus, hos_dash, hos_kpi]

    ray_run = (f"Ran {nat} <b>{mis} across {channels}</b> covering <b>1,000+ SKUs</b> – the numbers Sales and Finance "
               "leadership used for monthly reviews and annual planning.")
    ray_auto = ("Automated core reporting with SQL, Excel VBA and Google Apps Script, cutting turnaround from "
                "<b>2–3 days to under 1 hour</b> and removing <b>15+ hours</b> of manual work a week.")
    ray_pbi = ("Developed a <b>Power BI reporting suite</b> (data model, DAX, row-level security) used by <b>50+ stakeholders</b> "
               "across regions and channels.")
    ray_tgt = (f"Designed region- and channel-level <b>target-allocation and KPI models covering {ray_rev} in sales targets</b>; "
               "analysed SKU-level trends, variance and categories to flag growth pockets and underperforming segments.")
    ray_llm = "Introduced LLM-based workflows to draft insight summaries and management commentary from report outputs."
    ray = [ray_tgt, ray_run, ray_auto, ray_pbi, ray_llm] if track == "Strategy" else [ray_auto, ray_pbi, ray_run, ray_tgt, ray_llm]

    axis = [f"Led a <b>25-member vendor operations team</b> monitoring Axis Bank’s <b>5,000+ branch and ATM network</b>, sustaining "
            f"<b>99%+ uptime</b> against strict SLAs; tightened escalation workflows and standard{ise}d reporting SOPs."]
    modern = ["<b>Promoted from Operations Executive to Team Leader</b>; led a <b>35-member team</b> running MIS and operations for "
              "cash logistics across <b>10,000+ bank branches and ATMs</b>.",
              "Wrote Excel VBA validation checks that caught data anomalies before reports went out, reducing errors and escalations."]

    jobs = [
        ("MIS &amp; Sales Analyst", "(reporting to Chief of Sales)", "Jul 2026 – Present",
         "HOSINDIA Distributions Pvt. Ltd. – India arm of House of Spices Inc. (USA &amp; Canada)", "Mumbai", hos),
        ("MIS Analyst", "", "May 2023 – Jun 2026",
         f"Raymond Lifestyle Ltd. – Listed apparel &amp; textile company, {ray_rev} revenue", "Mumbai", ray),
        ("Senior Operations Representative", "(vendor-side)", "Dec 2022 – Apr 2023",
         "Axis Bank – Branch &amp; ATM Network Operations", loc_old, axis),
        ("Operations Executive to Team Leader, MIS &amp; Operations", "(35 people)", "Nov 2018 – Oct 2022",
         "Modern Informatics Pvt. Ltd. – Banking operations &amp; IT services", loc_old, modern),
    ]
    return dict(us=us, headline=headline, summary=summary, business=business, jobs=jobs)

CSS = """
@page { size: %(size)s; margin: 0; }
* { box-sizing: border-box; }
body { font-family: Arial, Helvetica, 'Liberation Sans', sans-serif; font-size: %(fs)spt; line-height: %(lh)s; color: #111;
       margin: 0; padding: %(pad)s; }
h1 { text-align: center; font-size: 19pt; margin: 0 0 2pt; letter-spacing: .3pt; }
.hl, .contact, .visa { text-align: center; margin: 0; }
.hl { color: #1f3f94; font-size: 10pt; }
.contact { margin-top: 2pt; }
.visa { color: #1f3f94; font-weight: bold; margin-top: 2pt; }
h2 { color: #1f3f94; font-size: 9.2pt; margin: 8pt 0 3pt; padding-bottom: 1.5pt; border-bottom: .8pt solid #1f3f94; letter-spacing: .3pt; }
p { margin: 0 0 2pt; text-align: justify; }
.row { display: flex; justify-content: space-between; gap: 8pt; }
.row .r { white-space: nowrap; }
.title { font-weight: bold; font-size: 9.8pt; margin-top: 5pt; }
.title span.n { font-weight: normal; font-size: 9.2pt; color: #444; }
.title .r { font-weight: normal; font-size: 9.2pt; }
.co { color: #1f3f94; font-weight: bold; }
.co .r { font-weight: normal; font-style: italic; color: #333; }
ul { margin: 1.5pt 0 0; padding-left: 13pt; }
li { margin: 0 0 1pt; text-align: justify; }
"""

def render(region, track):
    c = content(region, track)
    size = "Letter" if c["us"] else "A4"
    jobs = ""
    for t, note, dates, co, loc, bullets in c["jobs"]:
        jobs += (f'<div class="row title"><span>{t} <span class="n">{note}</span></span><span class="r">{dates}</span></div>'
                 f'<div class="row co"><span>{co}</span><span class="r">{loc}</span></div>'
                 "<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>")
    visa = '<p class="visa">Open to relocation across the US · Requires H-1B visa sponsorship</p>' if c["us"] else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Nilesh Diwane – Resume</title>
<style>{CSS % dict(size=size, fs="8.9" if c["us"] else "9.2", lh="1.27" if c["us"] else "1.32", pad="8mm 12mm 6mm" if c["us"] else "11mm 13mm 9mm")}</style></head><body>
<h1>NILESH DIWANE</h1>
<p class="hl">{c['headline']}</p>
<p class="contact">Navi Mumbai, India | +91-8767222251 | diwanenil543@gmail.com | linkedin.com/in/nilesh-diwane</p>
{visa}
<h2>SUMMARY</h2><p>{c['summary']}</p>
<h2>SKILLS</h2>
<p><b>Business:</b> {c['business']}</p>
<p><b>Tools:</b> Power BI (DAX, data modeling, RLS) · SQL · Advanced Excel &amp; VBA · Python (Pandas) · Google Apps Script · SAP &amp; ERP · PowerPoint · GenAI/LLM workflow automation</p>
<h2>EXPERIENCE</h2>{jobs}
<h2>EDUCATION &amp; CERTIFICATIONS</h2>
<div class="row"><span><b>Bachelor of Computer Applications (BCA), Data Analytics</b> – Amity University</span><span class="r">2026</span></div>
<div class="row"><span><b>Diploma, Hospitality &amp; Operations Management</b> – Frankfinn Institute</span><span class="r">2021</span></div>
<p style="margin-top:2pt"><b>Certifications:</b> Google – AI for Data Analysis; Foundations of Data Science · Vanderbilt University – Prompt Engineering; ChatGPT Advanced Data Analysis · TCS iON – Data Modeling &amp; Visualization · Microsoft PL-300 (in progress)</p>
</body></html>"""

NODE = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  for (const f of process.argv.slice(1)) {
    await pg.goto('file://' + f);
    await pg.pdf({ path: f.replace(/\\.html$/, '.pdf'), preferCSSPageSize: true, printBackground: true });
    console.log('wrote', f.replace(/\\.html$/, '.pdf'));
  }
  await b.close();
})();
"""

def main():
    files = []
    for region in ("India", "US"):
        for track in ("Analytics", "Strategy"):
            f = OUT / f"Nilesh_Diwane_Resume_{region}_{track}.html"
            f.write_text(render(region, track), encoding="utf-8")
            files.append(str(f))
    subprocess.run(["node", "-e", NODE, *files], check=True)
    for f in files:
        os.remove(f)

main()
