import sys, asyncio, json
from playwright.async_api import async_playwright
import os
SRC=os.path.join(os.path.dirname(__file__),'..','..','artifacts','portfolio-ledger.html')
MOCK=open(os.path.join(os.path.dirname(__file__),'mock.js')).read()
async def page_for(b, w, dark=False, mock=True):
    ctx = await b.new_context(viewport={'width':w,'height':900}, color_scheme='dark' if dark else 'light')
    pg = await ctx.new_page(); errs=[]
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append('console:'+m.text) if m.type=='error' else None)
    html = open(SRC).read()
    head = '<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width">' + (f'<script>{MOCK}</script>' if mock else '')
    await pg.set_content(head+html, wait_until='domcontentloaded'); await pg.wait_for_timeout(300)
    return pg, errs
async def fill_row(pg, idx, typ, sym, qty, net, profit, loss=False):
    row = pg.locator('#pfRows [data-row]').nth(idx)
    await row.locator('[data-f=type]').select_option(typ)
    await row.locator('[data-f=symbol]').fill(sym); await row.locator('[data-f=qty]').fill(qty); await row.locator('[data-f=net]').fill(net); await row.locator('[data-f=profit]').fill(profit)
    if loss: await row.locator('input[type=radio][value="-1"]').check(force=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg, errs = await page_for(b, 1200)
        assert await pg.is_visible('#welcome'), 'welcome visible on empty'
        await pg.screenshot(path='01-welcome.png')
        await pg.click('#welcome [data-act=new-portfolio]')
        await pg.fill('#pfNameIn','Dime หุ้น US'); await pg.fill('#pfGoalIn','500,000')
        await fill_row(pg,0,'us_stock','nvda','3.5','520','272')
        await pg.click('#pfAddRow'); await fill_row(pg,1,'fund','SCBRMS&P500','4120','60,000','1850',loss=True)
        await pg.wait_for_timeout(100); await pg.locator('#dlgPf').screenshot(path='02-create-dialog.png')
        prev = await pg.inner_text('#pfTotal'); print('total preview:', prev)
        await pg.click('#pfSave'); await pg.wait_for_timeout(600)
        assert await pg.is_visible('#v-pf'), 'went to portfolio view'
        st = await pg.evaluate('window.__store'); print('docs:', sorted(st.keys()))
        h = [v for k,v in st.items() if k.startswith('holdings/') and v['symbol']=='NVDA'][0]
        print('NVDA holding:', h)
        assert h.get('rpId')=='E09E2B', 'rpId resolved to US listing'
        f = [v for k,v in st.items() if k.startswith('holdings/') and v['type']=='fund'][0]
        assert f['profit']==-1850 and f['net']==60000 and f['symbol']=='SCBRMS&P500', f
        await pg.wait_for_timeout(300)
        print('live note:', await pg.inner_text('#pfLiveNote'))
        print('compare:', (await pg.inner_text('#pfCompare'))[:160])
        await pg.screenshot(path='03-portfolio.png', full_page=True)
        # contribution
        await pg.click('#v-pf .pf-head [data-act=new-contrib]')
        await pg.select_option('#cH', label='NVDA · หุ้น/ETF สหรัฐฯ'); await pg.fill('#cAmt','5,000'); await pg.fill('#cQty','0.6')
        print('contrib preview:', await pg.inner_text('#cPreview'))
        await pg.locator('#dlgC').screenshot(path='04-contrib.png')
        await pg.click('#cForm button[value=save]'); await pg.wait_for_timeout(300)
        st = await pg.evaluate('window.__store'); h2=[v for k,v in st.items() if k.startswith('holdings/') and v['symbol']=='NVDA'][0]
        print('NVDA after contrib net/qty:', h2['net'], h2['qty'])
        assert abs(h2['net']-(520+5000/36))<0.01 and abs(h2['qty']-4.1)<1e-9
        # delete contribution then undo
        await pg.click('[data-delc]'); await pg.wait_for_timeout(200)
        st = await pg.evaluate('window.__store'); h3=[v for k,v in st.items() if k.startswith('holdings/') and v['symbol']=='NVDA'][0]
        assert abs(h3['net']-520)<0.01 and abs(h3['qty']-3.5)<1e-9, h3
        assert not any(k.startswith('contributions/') for k in st)
        await pg.click('#toastUndo'); await pg.wait_for_timeout(300)
        st = await pg.evaluate('window.__store'); h4=[v for k,v in st.items() if k.startswith('holdings/') and v['symbol']=='NVDA'][0]
        assert any(k.startswith('contributions/') for k in st) and abs(h4['net']-(520+5000/36))<0.01, 'undo restored'
        # apply live
        await pg.click('[data-act=apply-live]'); await pg.wait_for_timeout(300)
        st = await pg.evaluate('window.__store'); h5=[v for k,v in st.items() if k.startswith('holdings/') and v['symbol']=='NVDA'][0]
        print('after live profit:', h5['profit'], 'expected', round(4.1*226.32-h5['net'],2))
        # update values dialog
        await pg.click('[data-act=update-values]'); await pg.wait_for_timeout(100); await pg.locator('#dlgU').screenshot(path='05-update.png'); await pg.click('#uForm button[value=cancel] >> nth=-1')
        # second portfolio quick
        await pg.click('.back'); await pg.wait_for_timeout(400)
        await pg.click('.pf-new'); await pg.fill('#pfNameIn','ทองกับคริปโต')
        await fill_row(pg,0,'gold','ทองแท่ง 96.5%','0.5','20,500','1700')
        await pg.click('#pfSave'); await pg.wait_for_timeout(500); await pg.click('.back'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='06-home.png', full_page=True)
        # news
        await pg.click('.nav button[data-go=news]'); await pg.click('#fetchNews'); await pg.wait_for_timeout(500)
        print('news status:', await pg.inner_text('#newsStatus'))
        await pg.click('#askBtn'); await pg.wait_for_timeout(200); await pg.click('#askSave'); await pg.wait_for_timeout(200)
        await pg.screenshot(path='07-news.png', full_page=True)
        st = await pg.evaluate('window.__store'); print('news docs', sum(k.startswith('news/') for k in st), 'analyses', sum(k.startswith('analyses/') for k in st), 'checkins', sum(k.startswith('checkins/') for k in st))
        # delete portfolio flow
        await pg.click('.nav button[data-go=home]'); await pg.wait_for_timeout(300)
        await pg.click('.pf-card >> nth=1'); await pg.wait_for_timeout(300); await pg.click('[data-act=edit-portfolio]'); await pg.click('#pfDelete'); await pg.click('#dlgOkBtn'); await pg.wait_for_timeout(400)
        st = await pg.evaluate('window.__store'); print('portfolios left', [v['name'] for k,v in st.items() if k.startswith('portfolios/')])
        print('ERRORS desktop:', errs)
        # phone + dark with demo
        pg2, errs2 = await page_for(b, 400, dark=True)
        await pg2.click('#demoOn'); await pg2.wait_for_timeout(400); await pg2.screenshot(path='08-phone-dark-home.png', full_page=True)
        await pg2.click('.pf-card >> nth=0'); await pg2.wait_for_timeout(400); await pg2.screenshot(path='09-phone-dark-pf.png', full_page=True)
        await pg2.click('[data-act=new-holding]'); await pg2.wait_for_timeout(200); await pg2.screenshot(path='10-phone-dialog.png')
        w = await pg2.evaluate('document.documentElement.scrollWidth'); print('phone scrollWidth', w)
        print('ERRORS phone:', errs2)
        pg3, errs3 = await page_for(b, 1200)
        await pg3.click('#demoOn'); await pg3.wait_for_timeout(400); await pg3.screenshot(path='11-demo-home.png', full_page=True)
        print('ERRORS demo:', errs3)
        await b.close()
asyncio.run(main())
