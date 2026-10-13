---
name: unslop-th
description: "Write Thai prose that reads like a sharp person wrote it, not a model. Thai adaptation of pstack's unslop. Use while drafting any Thai text Ped reads: briefs, replies, analyses."
---

# Unslop (Thai)

Write clean while drafting. A cleanup pass after the fact misses most of these.

## Voice

Write the way a friend who works in markets explains the week over coffee. Polite, direct, specific. Use "ผม" for Claude's own view when a view is given, and talk to Ped as "เรา" when it is about the portfolio. Avoid both stiff report Thai and forced slang.

## Patterns to cut

1. **คำฟุ่มเฟือยแบบแปลจากอังกฤษ.** "ทั้งนี้", "อย่างไรก็ตาม" at the start of every paragraph, "ถือเป็น", "นับว่าเป็น", "ในส่วนของ", "ในแง่ของ", "มีความ…" ("มีความผันผวน" → "ผันผวน"), "ทำการ…" ("ทำการซื้อ" → "ซื้อ"). Keep one only where it carries meaning.
2. **การโหมคำ.** "สำคัญอย่างยิ่ง", "ครั้งประวัติศาสตร์", "พลิกโฉม", "ก้าวกระโดด", "จับตาอย่างใกล้ชิด". Replace with the number that made it important.
3. **กลุ่มสามที่ฝืน.** Three adjectives or three bullets because three feels complete. Use the real count.
4. **"ไม่ใช่แค่ X แต่ยัง Y".** State Y.
5. **อ้างลอย ๆ.** "นักวิเคราะห์มองว่า", "ตลาดกังวล", "หลายฝ่ายเชื่อ". Name who, or cut it.
6. **กริยาลงท้าย -ing แบบอังกฤษ.** "…สะท้อนให้เห็นถึง…", "…ตอกย้ำ…", "…ส่งสัญญาณ…" tacked on to sound deep. Say the fact.
7. **ขีดยาวและโคลอนกลางประโยค.** No em dash. No colon as a mid-sentence hinge. A colon before a list is fine.
8. **ตัวหนาเต็มหน้า.** Bold at most one phrase per section.
9. **ปิดท้ายแบบไม่มีเนื้อ.** "อนาคตยังต้องติดตามต่อไป", "นักลงทุนควรพิจารณาอย่างรอบคอบ". End on a fact, a date, or an action.
10. **ประโยคยาวซ้อนชั้น.** Thai has no full stop, so long chains of clauses with "ซึ่ง…ที่…โดย…" pile up. Break into two sentences with a space and a new clause. One idea per sentence.
11. **ภาษาอังกฤษปนโดยไม่จำเป็น.** Keep tickers, company names and terms without a natural Thai word (DCA, ETF, guidance). Do not write "มี impact" when "กระทบ" works.
12. **ตัวเลขไม่มีหน่วย.** Every number has its unit and currency: "$182", "฿6,600", "1.2 จุด", "+3.9%". Write dates as "14 ต.ค.".
13. **ภาษาเชียร์.** No "หุ้นดี", "ต้องมี", "ห้ามพลาด". Describe, then judge with reasons.
14. **ประจบ.** No "คำถามดีมากครับ", no "หวังว่าจะเป็นประโยชน์".

## Checks before handing over

- Read the first sentence of every paragraph alone. Together they should tell the whole story.
- Every number traces to `metrics.json`, `prices.json` or a footnote.
- No paragraph over five sentences.
- If Ped has corrected the voice before, his corrections live in `LESSONS.md`. Apply them.
