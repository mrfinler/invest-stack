# invest-stack

ชุด workflow สำหรับดูแลพอร์ตหุ้นสหรัฐฯ ที่ถือผ่าน Dime ใช้กับ Claude Code (หรือ Claude ในแอป) ดัดแปลงแนวคิดจาก [pstack](https://github.com/michael-denyer/pstack-claude) ของ Lauren Tan มาใช้กับงานลงทุนแทนงานเขียนโค้ด

pstack มีตัวเลือก workflow กลาง (poteto-mode) หลักการ (principles) และ playbook ทีละขั้น repo นี้ใช้โครงเดียวกัน

| pstack | invest-stack |
|---|---|
| `poteto-mode` เลือก playbook ตามงาน | `invest-mode` เลือก playbook ตามงานลงทุน |
| principle เช่น Explain the Number, Attack the Premise | Explain the Number (แยกผลราคากับผลค่าเงิน), Attack the Thesis, Fact/Inference/Guess, Cite the Source, Size Before Conviction |
| `arena` แข่งหลายแบบแล้วเลือก | `bull-bear-arena` ให้ฝั่งบวกกับฝั่งลบเถียงจากหลักฐานชุดเดียวกัน มีกรรมการต่างโมเดล |
| `unslop` ตัดสำนวน AI | `unslop-th` ตัดสำนวน AI ในภาษาไทย |
| playbook Bug fix, Feature, Investigation | Weekly brief, Monthly review, Log trades, Ticker deep dive, Rebalance plan, Thesis check |

## สามชิ้นหลัก

1. **สมุดพอร์ต** (artifact ใน claude.ai) สร้างได้หลายพอร์ต ใส่สินทรัพย์อะไรก็ได้ด้วย จำนวน เงินที่ลงไป และกำไร บันทึกการลงทุนรายเดือน ดูมูลค่ารวมเป็นบาท ราคาตลาดและข่าวจาก Bigdata.com และสรุปโดย Claude ลิงก์อยู่ใน `invest.config.json` ซอร์สอยู่ที่ `artifacts/portfolio-ledger.html` เหตุผลการออกแบบอยู่ที่ `docs/ledger-v2-design.md`
2. **Ped Weekly** รายงานรายสัปดาห์แบบหน้าเว็บข่าว สร้างจาก `content.json` ด้วย `editorial-brief` กราฟและภาพปกวาดจากข้อมูลจริงทั้งหมด ไม่ดึงรูปจากสำนักข่าว (ลิงก์ไปอ่านต้นฉบับได้)
3. **Skills** ใน `plugins/invest-stack/skills/`

## ติดตั้งใน Claude Code

```
/plugin marketplace add mrfinler/invest-stack
/plugin install invest-stack@invest-stack
```

แล้วพิมพ์ `/invest-mode` ตามด้วยงาน เช่น "ทำ weekly brief สัปดาห์นี้" หรือ "บันทึกว่าซื้อ VOO 0.3 หุ้นที่ 571"

ถ้าติดตั้ง pstack ไว้ด้วย skill อย่าง `figure-it-out`, `swarm`, `how` ใช้ร่วมกันได้

## ตัวช่วยที่แนะนำ

- [Bigdata.com](https://bigdata.com) เป็นแหล่งข้อมูลหลัก: ราคาล่าสุด เป้าราคานักวิเคราะห์ sentiment ข่าว งบ transcript ปฏิทินเศรษฐกิจ และเก็บรายงานของเรากลับเข้าไปค้นภายหลังได้ สมุดพอร์ตมีปุ่มดึงราคาจาก Bigdata.com โดยตรง
- Financial Datasets สำหรับข้อมูลมหภาคและราคาย้อนหลัง (ต้องมีเครดิตในบัญชี)
- ตารางว่าใช้ connector ตัวไหนกับงานอะไรอยู่ใน skill `market-data`
- Skills ใน claude.ai: `deep-research` สำหรับเจาะลึก, `artifact-design` และ `dataviz` เวลาเพิ่มกราฟแบบใหม่

## โครงสร้าง

```
invest.config.json        ลิงก์สมุดพอร์ตและค่าตั้งต้น
plugins/invest-stack/     ปลั๊กอิน (skills, playbooks, scripts)
artifacts/                ซอร์สของหน้า artifact สมุดพอร์ต
briefs/                   ฉบับรายสัปดาห์ที่เผยแพร่แล้ว
work/                     ไฟล์ทำงานชั่วคราว (ไม่ commit)
LESSONS.md                บทเรียนที่เปลี่ยนสคริปต์หรือ playbook
```

ควรตั้ง repo นี้เป็น private เพราะ `briefs/` มีสัดส่วนพอร์ต

Claude ไม่ใช่ที่ปรึกษาการลงทุนที่มีใบอนุญาต ทุกอย่างในนี้เป็นข้อมูลประกอบการตัดสินใจ

## License

MIT ดู `LICENSE` และ `NOTICE.md` สำหรับเครดิต pstack
