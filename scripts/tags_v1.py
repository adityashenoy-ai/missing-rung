"""Seniority tags v1 — assigned from task wording only, blind to AI-usage numbers.
Rubric (see docs/METHODOLOGY.md):
  J  Junior rung  — executes defined work: produce, fix, test, document, enter/collect data, answer standard queries, follow procedures.
  M  Mid rung     — owns a piece: analyses, designs within constraints, diagnoses non-routine problems, recommends, coordinates.
  S  Senior rung  — sets direction or standards, decides/approves, owns budgets, negotiates, supervises, hires, mentors, advises clients on high-stakes matters.
  X  Excluded     — not representative of the role as practised by early-career people in India (kept in data, hidden from ladder).
Reason codes: exec, fix, test, doc, data, support, learn | analyze, design, diagnose, recommend, coordinate | direct, decide, people, client, budget, standards | offrole
Drafted by Claude (AI) from the rubric; to be reviewed by the author before launch.
"""
T = {
# software-engineer (15-1252.00 Software Developers + 15-1251.00 Computer Programmers)
"21662":"M analyze","21669":"M coordinate","21664":"M coordinate","21670":"J fix","21673":"J doc","21661":"M recommend",
"21676":"J data","21667":"M design","21668":"S standards","21665":"M coordinate","21663":"M coordinate","21671":"J support",
"21666":"M coordinate","21678":"S people","21677":"S people","21672":"M analyze","21679":"J support",
"1273":"J exec","1267":"J fix","1272":"M design","1270":"J exec","1271":"M coordinate","1268":"J test","1276":"J exec",
"1269":"J doc","1278":"M diagnose","1277":"M exec","1274":"J doc","1275":"M diagnose","1279":"S people","1281":"S people",
"21049":"J exec","21050":"J support","1280":"S direct",
# qa-engineer (15-1253.00)
"14642":"J test","14641":"J doc","14640":"M design","14638":"M design","14648":"J doc","14653":"M recommend","14652":"J exec",
"14639":"J test","14644":"J data","14649":"S standards","14643":"J exec","14650":"J exec","14646":"M coordinate","14645":"S decide",
"14654":"J exec","14655":"J test","14651":"M diagnose","14647":"M analyze","14658":"M recommend","14661":"J diagnose",
"14659":"M design","14656":"M exec","14657":"M client","14660":"M coordinate","14662":"X offrole","14664":"M analyze",
"14663":"S decide","21680":"J fix","21681":"X offrole","21682":"J data",
# web-developer (15-1254.00)
"14707":"J exec","14694":"J exec","14698":"J exec","14711":"S decide","14700":"J test","14704":"M design","14710":"J test",
"14695":"J exec","14701":"J learn","14702":"M analyze","14713":"J support","14705":"J exec","14697":"S decide","14708":"J support",
"14706":"S direct","14726":"J doc","14717":"J exec","14719":"M recommend","14728":"J doc","14714":"M design","14724":"M design",
"14722":"M doc","14725":"S decide","14723":"J exec","14729":"J exec","14727":"M analyze","14730":"M design","21683":"M design",
"21684":"M design",
# it-support (15-1232.00)
"1285":"M exec","1286":"J exec","1288":"J support","1282":"J support","1284":"J fix","1289":"M analyze","1283":"J test",
"1287":"J doc","1291":"J support","1292":"M recommend","1290":"M doc","1295":"J exec","1293":"J learn","1297":"S analyze",
"15204":"S people","1296":"M design",
# data-analyst (15-2051.01 BI Analysts + 15-2051.00 Data Scientists)
"16150":"J exec","16139":"J exec","16140":"J exec","16134":"J support","16141":"M analyze","16142":"J doc","16144":"M design",
"16146":"J data","16143":"J doc","16145":"J test","16149":"M recommend","16148":"M analyze","16136":"J data","16138":"M coordinate",
"16135":"J doc","16137":"M doc","16147":"S direct","21823":"J data","21828":"J exec","21837":"M analyze","21829":"M client",
"21836":"S client","21831":"S direct","21827":"M analyze","21826":"J data","21833":"S decide","21824":"M analyze","21832":"M analyze",
"21838":"J exec","21835":"J learn","21834":"M recommend","21825":"M design","21830":"M design",
# business-analyst (15-1211.00 Computer Systems Analysts)
"20950":"J fix","3464":"J support","3465":"J test","3482":"M analyze","3468":"M coordinate","3466":"J exec","3474":"M design",
"3469":"S client","3484":"M design","3470":"M design","3473":"J support","3475":"M analyze","3472":"M recommend","3480":"J learn",
"3477":"M doc","3479":"M recommend","3476":"M design","3467":"M client","3478":"J fix","3471":"J data","3481":"S people",
"3483":"S decide",
# financial-analyst (13-2051.00)
"21579":"S client","21580":"M analyze","21581":"M analyze","21582":"M coordinate","21583":"S client","21584":"X offrole",
"21585":"S client","21586":"J exec","21587":"S decide","21588":"S client","21589":"J exec","21590":"M analyze","21591":"M analyze",
"21592":"S client","21593":"M analyze","21594":"M analyze","21595":"J learn","21596":"J data","21597":"M analyze","21598":"J exec",
"21599":"M recommend","21600":"M client","21601":"S decide","21602":"S decide","21603":"X offrole","21604":"S people",
# accountant (13-2011.00 Accountants & Auditors + 43-3031.00 Bookkeeping, Accounting & Auditing Clerks)
"21514":"M analyze","21533":"J exec","21516":"J data","21526":"J exec","21515":"J exec","21508":"M analyze","21505":"M doc",
"21532":"M analyze","21507":"M analyze","21534":"M analyze","21520":"S client","21522":"M analyze","21509":"S people",
"21521":"M design","21510":"S client","21525":"M analyze","21517":"J data","21512":"J test","21511":"M recommend","21513":"M analyze",
"21519":"M analyze","21531":"M analyze","21528":"S client","21529":"S people","21524":"M analyze","21523":"S analyze",
"21530":"M analyze","21527":"S client","21518":"J test","21506":"S recommend",
"2487":"J data","2486":"J test","2488":"J exec","2495":"J exec","2500":"J exec","2493":"J data","2497":"J exec","2496":"J data",
"2498":"J support","2494":"J support","2490":"J data","2489":"J data","2509":"J data","18561":"J exec","2499":"J exec","2501":"J exec",
"2505":"J exec","2503":"J data","2507":"J data","2502":"J test","2506":"J data","2510":"J exec","2491":"J exec","2508":"J exec",
"2514":"J exec","2504":"J exec","2492":"J doc","2511":"J data",
# digital-marketer (13-1161.01 Search Marketing Strategists + 13-1161.00 Market Research Analysts & Marketing Specialists)
"20328":"J data","20329":"J exec","16192":"J data","16182":"M coordinate","16190":"M analyze","20320":"M coordinate","20318":"J exec",
"20326":"M analyze","20321":"S direct","20319":"M analyze","16189":"M coordinate","20330":"M analyze","20327":"M analyze","16191":"J exec",
"16186":"M analyze","16179":"S direct","20322":"S recommend","16188":"J coordinate","16175":"S decide","16193":"J coordinate",
"16172":"J learn","20331":"S decide","16185":"M coordinate","20325":"J exec","16187":"M analyze","16174":"M design","16184":"X offrole",
"16183":"M design","16177":"S direct","20324":"J exec","16178":"S decide","16181":"J exec","16180":"M design","20323":"J exec",
"16173":"J support","16176":"X offrole",
"5434":"J doc","5437":"M analyze","5439":"M analyze","5433":"J data","5443":"M design","5441":"J data","5435":"J data","5442":"J learn",
"5445":"S people","5438":"M analyze","5436":"M analyze","5440":"S client","5444":"M design",
# technical-writer (27-3042.00)
"3966":"J exec","3967":"J doc","3968":"J exec","3977":"M analyze","3970":"M recommend","3971":"J exec","3969":"S client",
"3976":"J exec","3972":"J learn","3975":"J exec","20243":"J exec","3978":"J learn","3973":"J learn","3974":"J learn","3979":"J exec",
# ux-designer (15-1255.00 Web & Digital Interface Designers + 27-1024.00 Graphic Designers)
"21702":"J fix","21692":"J exec","21714":"J exec","21706":"J test","21686":"M coordinate","21694":"M design","21704":"J learn",
"21711":"J support","21688":"M analyze","21705":"J exec","21701":"J test","21699":"S direct","21687":"J support","21709":"M design",
"21693":"S standards","21712":"S decide","21689":"S decide","21713":"J doc","21698":"M design","21697":"M design","21703":"M design",
"21710":"M analyze","21685":"S direct","21691":"M design","21707":"M doc","21700":"J doc","21695":"M design","21708":"J exec",
"21690":"J exec","21696":"M design",
"307":"J exec","304":"M recommend","300":"J exec","306":"J exec","299":"M design","301":"J exec","23970":"J exec","305":"M client",
"23971":"M analyze","303":"J exec","302":"J exec","309":"M analyze","15228":"J doc","310":"J doc","308":"J exec","15229":"J learn",
"313":"X offrole","312":"X offrole","23972":"J exec",
# project-manager (13-1082.00 Project Management Specialists + 15-1299.09 IT Project Managers)
"21463":"M client","21467":"M analyze","21481":"M exec","21464":"M diagnose","21473":"J coordinate","21479":"J exec","21470":"J exec",
"21462":"S people","21465":"J doc","21475":"J doc","21472":"S client","21469":"J data","21477":"S people","21471":"S people",
"21466":"M design","21478":"J doc","21476":"S decide","21468":"S decide","21480":"J coordinate","21474":"J doc",
"16169":"S direct","16154":"M diagnose","16157":"J exec","16152":"M exec","16155":"M analyze","16159":"S decide","16156":"J coordinate",
"16163":"S people","16164":"M analyze","16162":"M analyze","16170":"M design","16151":"M analyze","16168":"J doc","16160":"S decide",
"16166":"S budget","16161":"M design","16171":"M design","16153":"S people","16165":"S people","16167":"S people","16158":"S client",
}
