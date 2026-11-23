/* Project Assessment-I / Paper Assessment deck — PICT E&TC, Group 02 (Oct 2026).
   Plain language: "investor profile", "safety engine", no jargon left undefined. */
const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.layout = "LAYOUT_WIDE";
p.author = "Malhar Inamdar, Omkar Joshi, Piyush Ochani";
p.company = "PICT Dept of E and TC";
p.title = "Policy-Conditioned Multi-Agent LLM Trading Decision Support - Assessment I";

const INK="14243A", INKBG="0F1E33", GREEN="006633", GREEN2="1C7A4A", GOLD="B9820F", GOLDBR="E3B23C",
      MUTED="5C6B7A", LIGHT="F5F8F6", CARD="EEF3F0", BORDER="D5DED8", WHITE="FFFFFF", RED="B03A2E",
      SDG8="A21942", SDG9="FD6925";
const F="Calibri", W=13.33, MX=0.6, CW=W-2*MX;
const chipW = t => Math.min(Math.max(t.length*0.105+0.44,1.3),4.8);

function footer(s,n){
  s.addText("Dept. of E&TC, PICT  ·  B.E. Project Assessment – I  ·  A.Y. 2026–27",{x:MX,y:7.04,w:9.5,h:0.3,fontFace:F,fontSize:9,color:MUTED,margin:0});
  s.addText(String(n),{x:W-1.2,y:7.04,w:0.6,h:0.3,fontFace:F,fontSize:9,color:MUTED,align:"right",margin:0});
}
function head(s,kicker,title){
  s.addText(kicker.toUpperCase(),{x:MX,y:0.46,w:chipW(kicker),h:0.34,shape:p.ShapeType.roundRect,rectRadius:0.05,
    fill:{color:GREEN},color:WHITE,fontFace:F,fontSize:11.5,bold:true,align:"center",valign:"middle",charSpacing:1.2,margin:0});
  s.addText(title,{x:MX-0.02,y:0.9,w:CW,h:0.8,fontFace:F,fontSize:26,bold:true,color:INK,valign:"top",margin:0});
}
const bl = (arr,fs=13.5,color=INK,gap=7) => arr.map(t=>({text:t,options:{bullet:{code:"2022"},fontFace:F,fontSize:fs,color,paraSpaceAfter:gap,breakLine:true}}));
function card(s,x,y,w,h,fill=LIGHT){ s.addShape(p.ShapeType.roundRect,{x,y,w,h,fill:{color:fill},line:{color:BORDER,width:1},rectRadius:0.07}); }
let n=0; const slide=()=>{n++; return p.addSlide();};

// 1 · TITLE
(function(){ const s=slide(); s.background={color:WHITE};
  s.addImage({path:"logo.png",x:(W-1.02)/2,y:0.34,w:1.02,h:0.93});
  s.addText("Society for Computer Technology and Research's",{x:0,y:1.32,w:W,h:0.3,align:"center",fontFace:F,fontSize:13,italic:true,color:MUTED});
  s.addText("Pune Institute of Computer Technology, Pune – 43",{x:0,y:1.58,w:W,h:0.42,align:"center",fontFace:F,fontSize:20,bold:true,color:INK});
  s.addText("Department of Electronics & Telecommunication Engineering",{x:0,y:1.98,w:W,h:0.3,align:"center",fontFace:F,fontSize:12.5,color:GREEN,bold:true});
  s.addText("B.E. PROJECT  ·  ASSESSMENT – I  ·  GROUP NO. 02",{x:0,y:2.42,w:W,h:0.3,align:"center",fontFace:F,fontSize:12,bold:true,color:GOLD,charSpacing:1.5});
  s.addText("A Policy-Conditioned Multi-Agent LLM Framework for\nAuditable, Evidence-Driven Trading Decision Support",{x:1.0,y:2.78,w:W-2,h:1.25,align:"center",fontFace:F,fontSize:26,bold:true,color:INK});
  s.addText("A team of AI agents that analyses a stock the way the investor wants, says how sure it is, and shows its reasons — US and Indian markets",{x:1.4,y:4.02,w:W-2.8,h:0.5,align:"center",fontFace:F,fontSize:12.5,italic:true,color:MUTED});
  const th={fontFace:F,fontSize:12.5,bold:true,color:WHITE,fill:{color:GREEN},align:"center",valign:"middle"};
  const td={fontFace:F,fontSize:12.5,color:INK,align:"center",valign:"middle"};
  s.addTable([[{text:"Roll No.",options:th},{text:"Seat No.",options:th},{text:"Name",options:th}],
    [{text:"42205",options:td},{text:"",options:td},{text:"Malhar Inamdar",options:td}],
    [{text:"42333",options:td},{text:"",options:td},{text:"Omkar Joshi",options:td}],
    [{text:"42364",options:td},{text:"",options:td},{text:"Piyush Ochani",options:td}]],
    {x:3.9,y:4.7,w:5.53,colW:[1.4,1.6,2.53],rowH:0.34,border:{type:"solid",pt:0.5,color:BORDER}});
  s.addText([{text:"Project Guide:  ",options:{fontFace:F,fontSize:13,color:MUTED}},{text:"Dr. P. S. Varade",options:{fontFace:F,fontSize:13,bold:true,color:INK}},
    {text:"     ·     Mentor:  ",options:{fontFace:F,fontSize:13,color:MUTED}},{text:"Dr. Mousami Turuk",options:{fontFace:F,fontSize:13,bold:true,color:INK}}],{x:0,y:6.28,w:W,h:0.3,align:"center"});
  s.addText("Academic Year 2026–27  ·  October 2026",{x:0,y:6.62,w:W,h:0.3,align:"center",fontFace:F,fontSize:11.5,color:MUTED});
  s.addNotes("Group 02. Title matches the submitted synopsis. Fill seat numbers before printing.");
})();

// 2 · CONTENTS
(function(){ const s=slide(); s.background={color:INKBG};
  s.addText("CONTENTS",{x:MX,y:0.55,w:6,h:0.6,fontFace:F,fontSize:30,bold:true,color:WHITE});
  const items=["Introduction","Problem definition & objectives","Literature survey","What others have already done","Proposed system & flowchart",
    "Core logic","Implementation","Experiment & results","Progress vs plan","Plan ahead","SDG mapping","Paper publication details","Conclusions & references"];
  const col=(arr,x,off)=>s.addText(arr.map((it,i)=>({text:`${String(off+i+1).padStart(2,"0")}   ${it}`,options:{fontFace:F,fontSize:15,color:WHITE,paraSpaceAfter:12,breakLine:true}})),{x,y:1.6,w:5.9,h:5.1,valign:"top"});
  col(items.slice(0,7),MX,0); col(items.slice(7),7.0,7); footer(s,n);
})();

// 3 · INTRODUCTION
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Introduction","What we are building — and why");
  s.addText(bl([
    "AI “trading assistants” are now common: you ask about a stock and get buy, sell or hold.",
    "Three problems remain: they ignore the investor's own risk limits, their “90% sure” is often wrong, and the profits they report in tests are usually exaggerated.",
    "Our project: a team of AI agents that analyses a stock according to a written investor policy (how much to risk, how sure to be), shows the reasons for every decision, and is checked by a fixed safety engine — on US and Indian (NSE) stocks.",
    "Our focus is measurement: does the AI follow the investor's rules, is its confidence accurate, and is extra analysis worth it — instead of chasing profit, which cannot be trusted.",
  ],14),{x:MX,y:1.8,w:7.55,h:4.9,valign:"top"});
  card(s,8.5,1.85,4.23,4.85);
  s.addText("THE 3 THINGS WE CHECK",{x:8.75,y:2.02,w:3.8,h:0.3,fontFace:F,fontSize:12,bold:true,color:GOLD,charSpacing:1});
  s.addText([{text:"1 · Does it follow the investor's rules?\n\n",options:{fontFace:F,fontSize:14.5,bold:true,color:INK,breakLine:true}},
             {text:"2 · Is its confidence accurate?\n\n",options:{fontFace:F,fontSize:14.5,bold:true,color:INK,breakLine:true}},
             {text:"3 · Does gathering more evidence actually help?",options:{fontFace:F,fontSize:14.5,bold:true,color:INK}}],{x:8.75,y:2.45,w:3.8,h:2.6,valign:"top"});
  s.addText("No real money is used — paper trading only.",{x:8.75,y:5.6,w:3.8,h:0.8,fontFace:F,fontSize:12.5,italic:true,color:GREEN,valign:"top"});
  footer(s,n);
})();

// 4 · PROBLEM & OBJECTIVES
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Problem Definition & Objectives","What we build, and what we measure");
  card(s,MX,1.82,CW,1.2);
  s.addText("PROBLEM STATEMENT",{x:MX+0.25,y:1.95,w:5,h:0.3,fontFace:F,fontSize:12,bold:true,color:GOLD,charSpacing:1.2});
  s.addText("To build a multi-agent LLM trading system whose behaviour is governed by an explicit investor policy under a rule-based risk check, and to evaluate how faithfully it follows that policy, how reliable its confidence is, and how efficiently it uses evidence, using paper trading on US and Indian equities.",{x:MX+0.25,y:2.22,w:CW-0.5,h:0.75,fontFace:F,fontSize:14,color:INK,valign:"top"});
  const objs=[["01","Build the system: real data, specialist AI agents, finance-maths tools, a fixed safety engine and paper trading."],
    ["02","Measure how faithfully it follows different investor policies when given exactly the same market facts."],
    ["03","Measure how accurate its confidence is, and whether more evidence is worth the extra cost."],
    ["04","Validate on US + Indian stocks with paper trading — profit is a secondary check, not the goal."]];
  let y=3.3; objs.forEach(([k,t])=>{ s.addText(k,{x:MX,y,w:0.62,h:0.7,shape:p.ShapeType.roundRect,rectRadius:0.05,fill:{color:INK},color:WHITE,fontFace:F,fontSize:17,bold:true,align:"center",valign:"middle"});
    s.addText(t,{x:MX+0.8,y,w:CW-0.9,h:0.7,fontFace:F,fontSize:14,color:INK,valign:"middle"}); y+=0.84; });
  footer(s,n);
})();

// 5 · LITERATURE SURVEY
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Literature Survey","32 papers reviewed — what each group taught us");
  const th={fontFace:F,fontSize:11.5,bold:true,color:WHITE,fill:{color:GREEN},valign:"middle"};
  const td={fontFace:F,fontSize:11,color:INK,valign:"middle"}, ti={...td,italic:true};
  const rows=[["Group","Key papers","What we took from it"],
    ["AI agent teams for trading","TradingAgents (2024), FinCon (2024), FinMem, FinAgent","How to organise agents as a team. We reuse this design — it is not our contribution."],
    ["Can the results be trusted?","Look-ahead bias test (2025), The Alpha Illusion (2026)","Reported AI trading profits are often exaggerated, so we measure behaviour, not profit."],
    ["Fair testing","StockBench (2025), Agent Market Arena (2026)","Test only on data the AI could not have seen during training."],
    ["Following the investor's rules","FinPersona-Bench, PortBench, BiasMix-Finance (2026)","Raw AI proposals often break the investor's limits; a repair layer fixes them."],
    ["Safety layers & audit","OpenPM, CLQT, Policy-as-Skill (2026)","How to count when a fixed safety layer overrides the AI, and whether that helps."],
    ["Confidence & finance maths","Guo et al. (2017), KTD-Fin (2026), Sharpe, Kelly, López de Prado","How to check that “70% sure” means right 70% of the time; proven sizing and scoring formulas."]];
  s.addTable(rows.map((r,i)=>r.map((t,j)=>({text:t,options:i===0?th:(j===1?ti:td)}))),
    {x:MX,y:1.78,w:CW,colW:[2.6,4.0,5.53],rowH:[0.4,0.66,0.66,0.6,0.66,0.66,0.7],border:{type:"solid",pt:0.5,color:BORDER}});
  s.addText("Full survey table (32 papers, approach · data · reported result) is in the paper.",{x:MX,y:6.62,w:CW,h:0.3,fontFace:F,fontSize:11,italic:true,color:MUTED});
  footer(s,n);
})();

// 6 · WHAT OTHERS ALREADY DID (honest)
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"What Others Have Already Done","Honest check: the system is not new — the question we answer is");
  card(s,MX,1.85,6.05,4.0);
  s.addText("ALREADY DONE BY OTHERS (Aug–Sep 2026)",{x:MX+0.25,y:2.0,w:5.6,h:0.3,fontFace:F,fontSize:12,bold:true,color:RED,charSpacing:0.5});
  s.addText(bl(["Multi-agent trading teams — TradingAgents, FinCon","AI proposes, a fixed layer enforces the investor's rules — OpenPM, BiasMix-Finance, CLQT",
    "Different risk profiles give different allocations — PortBench","Raw AI proposals often break mandates — BiasMix-Finance (48–86%)",
    "Confidence of trading agents measured once — KTD-Fin"],12.5,INK,6),{x:MX+0.25,y:2.38,w:5.6,h:3.4,valign:"top"});
  card(s,6.9,1.85,5.83,4.0,CARD);
  s.addText("STILL OPEN — OUR FOCUS",{x:7.15,y:2.0,w:5.4,h:0.3,fontFace:F,fontSize:12,bold:true,color:GREEN,charSpacing:0.5});
  s.addText(bl(["When the safety engine overrides the AI, does the outcome get better or worse? Nobody has measured this.",
    "Same real market facts replayed under four investor profiles, with the AI free to break the rules.",
    "Numeric policy file vs. a text-only investor description.",
    "Indian NSE stocks — no leakage-controlled study found."],12.5,INK,6),{x:7.15,y:2.38,w:5.35,h:3.4,valign:"top"});
  s.addShape(p.ShapeType.roundRect,{x:MX,y:6.05,w:CW,h:0.75,fill:{color:INKBG},rectRadius:0.06});
  s.addText("Decision: keep the project. The system is the working instrument; the new contribution is the measurement.",{x:MX+0.3,y:6.12,w:CW-0.6,h:0.6,fontFace:F,fontSize:13.5,bold:true,color:WHITE,valign:"middle"});
  footer(s,n);
  s.addNotes("If asked 'is this already done?': yes, the architecture is (OpenPM, BiasMix-Finance, CLQT). We say so openly. What is open is whether the safety layer's overrides help or hurt outcomes, and NSE coverage.");
})();

// 7 · BLOCK DIAGRAM
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Proposed System","Block diagram — input, processing, output");
  const iw=8.75, ih=iw/1.786; s.addImage({path:"fig_block_diagram.png",x:(W-iw)/2,y:1.62,w:iw,h:ih});
  s.addText("The investor policy controls the planner. The safety engine has fixed rules (no AI) and can block any trade that breaks the policy.",{x:MX,y:6.6,w:CW,h:0.36,align:"center",fontFace:F,fontSize:12,italic:true,color:MUTED});
  footer(s,n);
})();

// 8 · FLOWCHART
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Flowchart","How one decision is made");
  const ih=5.25, iw=ih*0.667; s.addImage({path:"fig_flowchart.png",x:MX,y:1.7,w:iw,h:ih});
  card(s,4.6,1.85,8.13,4.95);
  s.addText("IN SIMPLE STEPS",{x:4.85,y:2.0,w:7.6,h:0.3,fontFace:F,fontSize:12,bold:true,color:GOLD,charSpacing:1});
  s.addText([
    "Read the investor policy — it decides which agents to ask first and how sure the system must be.",
    "Ask agents one by one (chart, news, company numbers, market trend, price model) and combine their views.",
    "Stop as soon as the system is sure enough or the evidence budget is used up.",
    "Decide: either code sets the trade size from risk (guarded), or the AI proposes it (unguarded — used for testing).",
    "Safety engine checks size limit, stop-loss and confidence; it can block the trade.",
    "Save the decision with all its evidence and reasons, so it can be checked and replayed later."
  ].map((t,i)=>({text:`${i+1}.  ${t}`,options:{fontFace:F,fontSize:13,color:INK,paraSpaceAfter:9,breakLine:true}})),{x:4.85,y:2.4,w:7.65,h:4.3,valign:"top"});
  footer(s,n);
})();

// 9 · CORE LOGIC
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Core Logic","A small settings file controls the whole system");
  s.addShape(p.ShapeType.roundRect,{x:MX,y:1.82,w:5.2,h:4.9,fill:{color:"16283F"},rectRadius:0.07});
  s.addText("CONSERVATIVE INVESTOR POLICY (real file)",{x:MX+0.22,y:1.97,w:4.8,h:0.3,fontFace:F,fontSize:11,bold:true,color:GOLDBR});
  s.addText(['{','  "max_position_pct": 2.0,','  "stop_loss_pct": 3.0,','  "take_profit_pct": 6.0,','  "confidence_to_act": 0.75,','  "evidence_budget": 6,',
    '  "target_vol": 0.02,','  "tool_priorities":','    ["fundamental","macro",','     "news","technical"],','  "forbidden_evidence":','    ["order_book",','     "intraday_momentum"]','}'].join("\n"),
    {x:MX+0.22,y:2.32,w:4.8,h:4.3,fontFace:"Courier New",fontSize:11.5,color:"D9F2E4",valign:"top"});
  const rows=[["Never put more than 2% of the money in one stock","Safety engine blocks bigger trades"],
    ["Only trade if at least 75% sure","Below that, the system waits"],
    ["Look at company numbers and the economy first","Planner asks agents in this order"],
    ["Use at most 6 units of analysis","Stops early to save cost"],
    ["Size by risk: calmer stock → bigger position","Volatility-target sizing (Kelly-style)"]];
  card(s,6.05,1.82,6.68,4.9);
  s.addText("WHAT EACH LINE MEANS",{x:6.3,y:1.97,w:6.2,h:0.3,fontFace:F,fontSize:11,bold:true,color:GOLD,charSpacing:1});
  let y=2.38; rows.forEach(([a,b])=>{ s.addText(a,{x:6.3,y,w:6.2,h:0.36,fontFace:F,fontSize:13,bold:true,color:INK,margin:0});
    s.addText(b,{x:6.3,y:y+0.36,w:6.2,h:0.32,fontFace:F,fontSize:12,color:MUTED,margin:0}); y+=0.85; });
  footer(s,n);
})();

// 10 · IMPLEMENTATION
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Implementation","What is built and running today");
  const g=[["AI agents & planner","Python · LangGraph planner · OpenAI agents: technical, news, company numbers, economy"],
    ["Live market data","Yahoo Finance + Finnhub · real prices, news, company numbers · any US or NSE stock"],
    ["Finance maths","Signal score (IC) · return-vs-risk (Sharpe) · worst drop · risk-based sizing"],
    ["Safety & records","Fixed safety engine (can block a trade) · every decision saved with reasons · replayable"],
    ["Testing modes (new)","Guarded · AI with numeric rules · AI with text profile — all on the same frozen facts"],
    ["Quality","9 automated tests passing · 40-stock list frozen · code public on GitHub"]];
  g.forEach(([a,b],i)=>{ const yy=1.95+i*0.74;
    s.addText(a,{x:MX,y:yy,w:3.35,h:0.64,fontFace:F,fontSize:12.5,bold:true,color:WHITE,fill:{color:i%2?GREEN2:GREEN},valign:"middle",margin:[0,0,0,10]});
    s.addText(b,{x:MX+3.45,y:yy,w:CW-3.45,h:0.64,fontFace:F,fontSize:12.5,color:INK,valign:"middle",fill:{color:i%2?"F3F6F4":WHITE},margin:[0,0,0,10]}); });
  s.addText("Paper trading only — no real money.  ·  github.com/malharinamdar/policy-trading-agents",{x:MX,y:6.55,w:CW,h:0.3,fontFace:F,fontSize:11.5,italic:true,color:MUTED,align:"center"});
  footer(s,n);
})();

// 11 · EXPERIMENT
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Experiment","Does the AI follow the investor's limits when it is free not to?");
  const c=[["40 stocks","20 US + 20 NSE large caps; one set of real facts gathered per stock and frozen",GREEN],
           ["4 investor profiles","Conservative · Long-term · Day-trader · Aggressive — each replayed on the same facts",INK],
           ["3 decision modes","Guarded (code decides) · AI shown the numeric rules · AI shown only a text description",GOLD]];
  let x=MX; c.forEach(([t,b,col])=>{ card(s,x,1.85,3.9,2.3);
    s.addText(t,{x:x+0.22,y:2.0,w:3.5,h:0.5,fontFace:F,fontSize:20,bold:true,color:col});
    s.addText(b,{x:x+0.22,y:2.55,w:3.5,h:1.5,fontFace:F,fontSize:12.5,color:INK,valign:"top"}); x+=4.06; });
  card(s,MX,4.4,CW,2.35,CARD);
  s.addText("HOW WE SCORE IT",{x:MX+0.25,y:4.53,w:6,h:0.3,fontFace:F,fontSize:12,bold:true,color:GREEN,charSpacing:1});
  s.addText(bl(["480 decisions in total (40 × 4 × 3), model gpt-4o-mini, every AI proposal saved exactly as given.",
    "A decision “breaks the rules” if the position is above the cap, the stop-loss is missing or looser than allowed, or it trades below the confidence threshold.",
    "The safety engine checks the same proposal and records every block it makes."],12.5,INK,5),{x:MX+0.25,y:4.88,w:CW-0.5,h:1.8,valign:"top"});
  footer(s,n);
})();

// 12 · RESULT 1
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Result 1 — Rule-Following","Numeric rules are followed. A text description is not.");
  const iw=7.3, ih=iw/2.0; s.addImage({path:"fig_violations_by_profile.png",x:MX,y:1.85,w:iw,h:ih});
  card(s,8.15,1.85,4.58,4.9);
  const k=[["0%","Code-decided (by design)",MUTED],["0%","AI shown numeric rules (160 decisions)",GREEN],["64%","AI shown only a text profile — 98% of its trades broke a limit",GOLD]];
  let y=2.0; k.forEach(([v,t,col])=>{ s.addText(v,{x:8.37,y,w:1.5,h:0.7,fontFace:F,fontSize:30,bold:true,color:col,valign:"middle"});
    s.addText(t,{x:9.85,y,w:2.75,h:0.7,fontFace:F,fontSize:12,color:INK,valign:"middle"}); y+=0.95; });
  s.addText("The safety engine blocked 103 proposals (all from text mode). US 70% vs NSE 59%.",{x:8.37,y:4.95,w:4.2,h:0.9,fontFace:F,fontSize:12,italic:true,color:MUTED,valign:"top"});
  s.addText("Honest note: in text mode the AI was never shown the numbers, so this shows a written persona does not produce the intended limits — the case for a machine-readable policy.",
    {x:MX,y:5.65,w:7.3,h:1.1,fontFace:F,fontSize:12,color:INK,valign:"top"});
  footer(s,n);
})();

// 13 · RESULT 2
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Result 2 — Position Size vs. the Limit","Text profile: the “conservative” investor bet the most");
  const iw=9.0, ih=iw/2.0; s.addImage({path:"fig_size_vs_cap.png",x:(W-iw)/2,y:1.8,w:iw,h:ih});
  s.addText([{text:"Read it: ",options:{fontFace:F,fontSize:13,bold:true,color:GREEN}},
    {text:"dashed red = each profile's cap. Guarded and numeric-rule modes stay on the cap; text mode proposes 8–12% for every profile — conservative 11.5% against a 2% cap. No risk ordering at all.",options:{fontFace:F,fontSize:13,color:INK}}],
    {x:MX+0.4,y:1.8+ih+0.15,w:CW-0.8,h:0.8,valign:"top"});
  footer(s,n);
})();

// 14 · RESULT 3
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Result 3 — Baselines on 3 Years of Data","Simple signals have no edge, and their confidence is over-stated");
  const a=5.15, ah=a/1.35; s.addImage({path:"fig_reliability.png",x:MX+0.3,y:1.72,w:a,h:ah});
  const b=5.6, bh=b/1.5; s.addImage({path:"fig_cost_quality.png",x:6.9,y:1.8,w:b,h:bh});
  s.addText(bl(["Signal score (IC) ≈ 0 for all 4 simple signals; significant in 0% of stocks.",
    "Said 73% sure → right only 52%. Correction cut the calibration error 0.071 → 0.025.",
    "More evidence (2.0 → 2.9 sources) did not raise accuracy (50.1%).",
    "These are baselines; the AI agents must beat them — next experiment."],12,INK,4),{x:MX,y:5.68,w:CW,h:1.3,valign:"top"});
  footer(s,n);
})();

// 15 · PROGRESS vs PLAN
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Progress vs. Plan","Core system running and first experiment done");
  const m=[["Jul–Aug '26","Synopsis; real data pipeline; AI agents; risk sizing; safety engine; evaluation suite; 9 tests; code on GitHub","done"],
    ["Sep '26","Literature & venue study; code audit found the rule-following test could never fail; plan to fix it","done"],
    ["Oct '26 (wk 1)","Fixed it (unguarded AI modes); 40-stock experiment; 32-paper survey; paper written in both formats","done"],
    ["Oct–Nov '26","Safety-override analysis on real outcomes; replay AI agents over post-training history; more models","wip"],
    ["Dec '26","Live daily paper trading on US + NSE; full results; paper submission","plan"],
    ["Jan–May '27","Workshop/conference submission; web dashboard; final report & viva","plan"]];
  const cm={done:GREEN,wip:"C0801A",plan:MUTED}, cl={done:"DONE",wip:"NEXT",plan:"PLANNED"};
  m.forEach(([d,t,st],i)=>{ const y=1.9+i*0.75;
    s.addText(d,{x:MX,y,w:1.75,h:0.64,fontFace:F,fontSize:12,bold:true,color:WHITE,fill:{color:INK},align:"center",valign:"middle",shape:p.ShapeType.roundRect,rectRadius:0.05});
    s.addText(t,{x:MX+1.95,y,w:CW-3.75,h:0.64,fontFace:F,fontSize:12.3,color:INK,valign:"middle"});
    s.addText(cl[st],{x:W-MX-1.55,y:y+0.13,w:1.55,h:0.36,fontFace:F,fontSize:10.5,bold:true,color:WHITE,fill:{color:cm[st]},align:"center",valign:"middle",shape:p.ShapeType.roundRect,rectRadius:0.06}); });
  s.addText("Team: Malhar — data, maths & evaluation  ·  Omkar — AI agents & planner  ·  Piyush — full-stack & dashboard",{x:MX,y:6.55,w:CW,h:0.32,fontFace:F,fontSize:11.5,italic:true,color:MUTED,align:"center"});
  footer(s,n);
})();

// 16 · PLAN AHEAD
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Plan Ahead","Two tracks: a research paper and a usable product");
  card(s,MX,1.85,6.05,4.0);
  s.addText("RESEARCH (paper)",{x:MX+0.25,y:2.0,w:5.5,h:0.3,fontFace:F,fontSize:13,bold:true,color:GREEN});
  s.addText(bl(["Main study: when the safety engine overrides the AI, does the trade's real outcome improve or get worse?",
    "Replay the AI agents on 2025–26 history (after the model's training) to score their signal and confidence.",
    "Repeat with 3 AI models and repeated runs; add over-fitting checks (Deflated Sharpe, PBO).",
    "US vs. India comparison."],12.3,INK,6),{x:MX+0.25,y:2.38,w:5.6,h:3.4,valign:"top"});
  card(s,6.9,1.85,5.83,4.0,CARD);
  s.addText("PRODUCT",{x:7.15,y:2.0,w:5.4,h:0.3,fontFace:F,fontSize:13,bold:true,color:GOLD});
  s.addText(bl(["Web dashboard: decision feed, “why” page, profile comparison, safety log.",
    "Investor questionnaire that writes the policy file automatically.",
    "Daily paper-trading loop with alerts.","Portfolio view (many stocks, overall risk)."],12.3,INK,6),{x:7.15,y:2.38,w:5.35,h:3.4,valign:"top"});
  s.addShape(p.ShapeType.roundRect,{x:MX,y:6.05,w:CW,h:0.75,fill:{color:INKBG},rectRadius:0.06});
  s.addText("Limitations today: one AI model, one run per decision, current-day facts only, no real outcomes yet for the AI agents.",{x:MX+0.3,y:6.12,w:CW-0.6,h:0.6,fontFace:F,fontSize:12.5,color:WHITE,valign:"middle"});
  footer(s,n);
})();

// 17 · SDG
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"SDG Mapping","Linked to two UN Sustainable Development Goals");
  [[MX,SDG8,"SDG 8 · PRIMARY","Decent Work & Economic Growth","Trustworthy, explainable decision support that protects ordinary investors from opaque advice and excessive risk.","FBE4EC"],
   [6.9,SDG9,"SDG 9 · SECONDARY","Industry, Innovation & Infrastructure","An open, reusable tool and method for checking whether AI systems in finance follow their rules.","FFE7D6"]]
  .forEach(([x,col,t,sub,b,tc])=>{ s.addShape(p.ShapeType.roundRect,{x,y:1.9,w:5.83,h:3.0,fill:{color:col},rectRadius:0.08});
    s.addText(t,{x:x+0.3,y:2.1,w:5.3,h:0.5,fontFace:F,fontSize:22,bold:true,color:WHITE});
    s.addText(sub,{x:x+0.3,y:2.65,w:5.3,h:0.4,fontFace:F,fontSize:15,bold:true,color:WHITE});
    s.addText(b,{x:x+0.3,y:3.15,w:5.3,h:1.5,fontFace:F,fontSize:13.5,color:tc,valign:"top"}); });
  s.addText("Responsible by design: paper trading only, no profit promises, every decision recorded with its reasons.",{x:MX,y:5.3,w:CW,h:0.5,fontFace:F,fontSize:13.5,italic:true,color:GREEN,align:"center"});
  footer(s,n);
})();

// 18 · PAPER PUBLICATION
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"Paper Publication Details","Survey + partial implementation paper — status");
  const r=[["Title","A Policy-Conditioned Multi-Agent LLM Framework for Auditable, Evidence-Driven Trading Decision Support"],
    ["Type","Survey (32 papers, tabulated) + partial implementation with results"],
    ["Formats","Single column (12 pp) and IEEE double column (9 pp) — complete"],
    ["Contents","Block diagram, flowchart, algorithm, evaluation parameters, survey table + column chart, result line charts (300 dpi)"],
    ["Next","Plagiarism & AI check (≤5%) → guide sign-off → submit to a conference"],
    ["Target venues","Scopus conference from the department list; research track: AAAI-27 / ICLR-27 finance workshops"]];
  r.forEach(([a,b],i)=>{ const y=1.95+i*0.74;
    s.addText(a,{x:MX,y,w:2.6,h:0.64,fontFace:F,fontSize:12.5,bold:true,color:WHITE,fill:{color:i%2?GREEN2:GREEN},valign:"middle",margin:[0,0,0,10]});
    s.addText(b,{x:MX+2.7,y,w:CW-2.7,h:0.64,fontFace:F,fontSize:12.5,color:INK,valign:"middle",fill:{color:i%2?"F3F6F4":WHITE},margin:[0,0,0,10]}); });
  footer(s,n);
})();

// 19 · CONCLUSIONS
(function(){ const s=slide(); s.background={color:INKBG};
  s.addText("CONCLUSIONS",{x:MX,y:0.55,w:8,h:0.6,fontFace:F,fontSize:30,bold:true,color:WHITE});
  const pts=[["Working system","Real US + NSE data, 4 AI agents, risk-based sizing, safety engine, full decision records, 9 tests."],
    ["First real result","AI follows numeric limits (0% violations) but not a text description (64%)."],
    ["Honest baselines","Simple signals have no edge; stated confidence is over-confident and can be corrected."],
    ["Clear next step","Measure whether the safety engine's overrides improve real outcomes — still open in the field."]];
  pts.forEach(([h,b],i)=>{ const x=MX+(i%2)*6.15, y=1.6+Math.floor(i/2)*1.75;
    s.addShape(p.ShapeType.roundRect,{x,y,w:5.9,h:1.5,fill:{color:"16283F"},line:{color:"27405C",width:1},rectRadius:0.06});
    s.addText(h,{x:x+0.25,y:y+0.15,w:5.4,h:0.4,fontFace:F,fontSize:15,bold:true,color:GOLDBR});
    s.addText(b,{x:x+0.25,y:y+0.6,w:5.4,h:0.8,fontFace:F,fontSize:13,color:"DDE6EE",valign:"top"}); });
  s.addText("The system is the instrument; the measurement is the contribution.",{x:MX,y:5.4,w:CW,h:0.5,fontFace:F,fontSize:16,italic:true,color:WHITE,align:"center"});
  footer(s,n);
})();

// 20 · REFERENCES
(function(){ const s=slide(); s.background={color:WHITE};
  head(s,"References","Selected (full list of 32 in the paper)");
  const refs=["Y. Xiao et al., “TradingAgents: Multi-Agents LLM Financial Trading Framework,” arXiv:2412.20138, 2024.",
    "Y. Yu et al., “FinCon: A Synthesized LLM Multi-Agent System …,” NeurIPS, 2024.",
    "“The Alpha Illusion: Reported Alpha from LLM Trading Agents …,” arXiv:2605.16895, 2026.",
    "“StockBench: Can LLM Agents Trade Stocks Profitably …,” arXiv:2510.02209, 2025.",
    "“FinPersona-Bench: Longitudinal Psychometric Stability of Financial Agents,” arXiv:2606.31522, 2026.",
    "“CLQT: A Closed-Loop, Cost-Aware, Strategy-Consistent Benchmark …,” arXiv:2606.29771, 2026.",
    "“OpenPM: Auditable Point-in-Time Evaluation for LLM PM Agents,” arXiv:2608.09988, 2026.",
    "“BiasMix-Finance: Post-Generation KYC Guardrails,” arXiv:2608.28646, 2026 (ICLR 2026 FinAI workshop).",
    "“PortBench,” arXiv:2605.27887, 2026.",
    "K. Mohsenzadegan et al., “Policy-as-Skill: Governed LLM Decision Support …,” arXiv:2609.27087, 2026.",
    "C. Guo et al., “On Calibration of Modern Neural Networks,” ICML, 2017.",
    "D. Bailey, M. López de Prado, “The Deflated Sharpe Ratio,” J. Portfolio Management, 2014."];
  s.addText(refs.map((r,i)=>({text:`[${i+1}]  ${r}`,options:{fontFace:F,fontSize:11.5,color:INK,paraSpaceAfter:5,breakLine:true}})),{x:MX,y:1.8,w:CW,h:5.1,valign:"top"});
  footer(s,n);
})();

// 21 · THANK YOU
(function(){ const s=slide(); s.background={color:INKBG};
  s.addImage({path:"logo.png",x:(W-1.15)/2,y:1.5,w:1.15,h:1.05});
  s.addText("Thank You",{x:0,y:2.85,w:W,h:0.9,align:"center",fontFace:F,fontSize:44,bold:true,color:WHITE});
  s.addText("Questions & Discussion",{x:0,y:3.85,w:W,h:0.5,align:"center",fontFace:F,fontSize:18,italic:true,color:GOLDBR});
  s.addText("Group 02  ·  Malhar Inamdar (42205)  ·  Omkar Joshi (42333)  ·  Piyush Ochani (42364)",{x:0,y:4.7,w:W,h:0.4,align:"center",fontFace:F,fontSize:13,color:"DDE6EE"});
  s.addText("Guide: Dr. P. S. Varade  ·  Dept. of E&TC, PICT",{x:0,y:5.1,w:W,h:0.4,align:"center",fontFace:F,fontSize:13,color:"AEBFCF"});
})();

p.writeFile({fileName:"BE_Assessment_Oct2026_Group02.pptx"}).then(f=>console.log("WROTE",f,n,"slides"));
