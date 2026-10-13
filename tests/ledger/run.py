import sys, os, asyncio, json
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(HERE,'..','..','artifacts','portfolio-ledger.html')
MOCK=open(os.path.join(HERE,'mock.js')).read()
OUT=os.environ.get('SHOTS', HERE)
async def page_for(b, w, dark=False, mock=True):
    ctx = await b.new_context(viewport={'width':w,'height':900}, color_scheme='dark' if dark else 'light')
    pg = await ctx.new_page(); errs=[]
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append('console:'+m.text) if m.type=='error' and 'ERR_TUNNEL' not in m.text and 'Failed to load resource' not in m.text else None)
    head = '<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width">' + (f'<script>{MOCK}</script>' if mock else '')
    await pg.set_content(head+open(SRC).read(), wait_until='domcontentloaded'); await pg.wait_for_timeout(400)
    return pg, errs
def shot(name): return os.path.join(OUT, name)
async def store(pg): return await pg.evaluate('window.__store')
def find(st, pre, **kv):
    return [v for k,v in st.items() if k.startswith(pre) and all(v.get(a)==b for a,b in kv.items())]
async def fill_row(pg, idx, typ, sym, qty, net, profit, loss=False, thb=None):
    row = pg.locator('#pfRows [data-row]').nth(idx)
    await row.locator('[data-f=type]').select_option(typ)
    await row.locator('[data-f=symbol]').fill(sym); await row.locator('[data-f=qty]').fill(qty); await row.locator('[data-f=net]').fill(net); await row.locator('[data-f=profit]').fill(profit)
    if loss: await row.locator('input[type=radio][value="-1"]').check(force=True)
    if thb: await row.locator('[data-f=netTHB]').fill(thb)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg, errs = await page_for(b, 1200)
        assert await pg.is_visible('#welcome'), 'welcome on empty'
        assert (await pg.inner_text('#fxVal'))=='33.54', 'live fx from market snapshot: '+await pg.inner_text('#fxVal')
        await pg.screenshot(path=shot('01-welcome.png'))
        await pg.click('#welcome [data-act=new-portfolio]')
        await pg.fill('#pfNameIn','Dime US stocks'); await pg.fill('#pfGoalIn','500,000')
        await pg.click('#pfGlyphs label:nth-child(7)')
        await fill_row(pg,0,'us_stock','nvda','3.5','520','272', thb='18,000')
        await pg.click('#pfAddRow'); await fill_row(pg,1,'gold','Gold bar','0.5','20,500','1700')
        await pg.wait_for_timeout(100); await pg.locator('#dlgPf').screenshot(path=shot('02-create.png'))
        await pg.click('#pfSave'); await pg.wait_for_timeout(700)
        st=await store(pg); nv=find(st,'holdings/',symbol='NVDA')[0]; gd=find(st,'holdings/',type='gold')[0]; pf=find(st,'portfolios/')[0]
        print('portfolio icon', pf['icon']); assert pf['icon']=={'kind':'glyph','key':'rocket'}
        assert nv['netTHB']==18000 and nv['rpId']=='E09E2B', nv
        assert gd['unit']=='baht', gd
        await pg.wait_for_timeout(300)
        print('compare:', (await pg.inner_text('#pfCompare'))[:200].replace('\n',' '))
        await pg.screenshot(path=shot('03-portfolio.png'), full_page=True)
        # invest: buy NVDA with fee + new asset VOO
        await pg.click('#v-pf .pf-head [data-act=invest]'); await pg.fill('#tFx','33.10'); await pg.fill('#tCash','10,000')
        r0=pg.locator('#tRows [data-trow]').nth(0)
        await r0.locator('[data-t=h]').select_option(label='NVDA · USD'); await r0.locator('[data-t=price]').fill('200'); await r0.locator('[data-t=qty]').fill('0.5'); await r0.locator('[data-t=fee]').fill('0.5')
        await pg.click('#tAddRow'); r1=pg.locator('#tRows [data-trow]').nth(1)
        await r1.locator('[data-t=h]').select_option('__new'); await r1.locator('[data-t=ntype]').select_option('us_stock'); await r1.locator('[data-t=nsym]').fill('voo'); await r1.locator('[data-t=price]').fill('700'); await r1.locator('[data-t=qty]').fill('0.1'); await r1.locator('[data-t=fee]').fill('0.2')
        print('invest preview 0:', (await r0.locator('[data-tprev]').inner_text()).replace('\n',' '))
        print('invest total:', (await pg.inner_text('#tTotal')).replace('\n',' '))
        await pg.locator('#dlgT').screenshot(path=shot('04-invest.png'))
        await pg.click('#tForm button[value=save]'); await pg.wait_for_timeout(500)
        st=await store(pg); nv=find(st,'holdings/',symbol='NVDA')[0]; voo=find(st,'holdings/',symbol='VOO')[0]; txs=find(st,'transactions/')
        print('NVDA after buy:', {k:nv[k] for k in ('qty','net','netTHB','profit')})
        assert abs(nv['qty']-4.0)<1e-9 and abs(nv['net']-620.5)<1e-6 and abs(nv['netTHB']-(18000+100.5*33.1))<0.01 and abs(nv['profit']-(4*200-620.5))<0.01
        print('VOO new:', {k:voo[k] for k in ('qty','net','netTHB','profit','currency')})
        assert abs(voo['net']-70.2)<1e-6 and abs(voo['netTHB']-70.2*33.1)<0.01
        assert len(txs)==2 and all(t['fxRate']==33.1 for t in txs) and {t['fee'] for t in txs}=={0.5,0.2}
        # sell part of NVDA
        await pg.click('#v-pf .pf-head [data-act=invest]'); r0=pg.locator('#tRows [data-trow]').nth(0)
        await r0.locator('input[type=radio][value=sell]').check(force=True); await r0.locator('[data-t=h]').select_option(label='NVDA · USD'); await r0.locator('[data-t=price]').fill('250'); await r0.locator('[data-t=qty]').fill('1'); await r0.locator('[data-t=fee]').fill('0.5')
        await pg.click('#tForm button[value=save]'); await pg.wait_for_timeout(400)
        st=await store(pg); nv2=find(st,'holdings/',symbol='NVDA')[0]; sell=find(st,'transactions/',kind='sell')[0]
        avg=620.5/4; print('after sell:', {k:nv2[k] for k in ('qty','net','profit')}, 'realized', sell['realized'])
        assert abs(nv2['qty']-3)<1e-9 and abs(nv2['net']-(620.5-avg))<0.01 and abs(sell['realized']-(250-0.5-avg))<0.01
        assert abs((nv2['net']+nv2['profit'])-(800-250))<0.01, 'value drops by the sale proceeds'
        # delete the sell, undo restores
        await pg.click(f'[data-deltx="{[k for k,v in st.items() if k.startswith("transactions/") and v["kind"]=="sell"][0].split("/")[1]}"]'); await pg.wait_for_timeout(300)
        st=await store(pg); nv3=find(st,'holdings/',symbol='NVDA')[0]
        assert abs(nv3['qty']-4)<1e-9 and abs(nv3['net']-620.5)<0.01 and abs(nv3['net']+nv3['profit']-800)<0.01, nv3
        await pg.click('#toastUndo'); await pg.wait_for_timeout(300)
        st=await store(pg); assert find(st,'transactions/',kind='sell'), 'undo restored the sell'
        print('cost summary:', (await pg.inner_text('#costSum')).replace('\n',' | '))
        await pg.screenshot(path=shot('05-portfolio-after.png'), full_page=True)
        # charts
        await pg.click('.nav button[data-go=charts]'); await pg.wait_for_timeout(600)
        print('chart note:', await pg.inner_text('#chNote'))
        await pg.fill('#watchIn','qqq'); await pg.click('#watchForm button'); await pg.wait_for_timeout(600)
        st=await store(pg); assert find(st,'watchlist/',symbol='QQQ')
        await pg.click('[data-range="3M"]'); await pg.wait_for_timeout(200)
        await pg.screenshot(path=shot('06-charts.png'), full_page=True)
        st=await store(pg); print('pricehist docs:', sorted(k for k in st if k.startswith('pricehist/')))
        # news + summary
        await pg.click('.nav button[data-go=news]'); await pg.click('#fetchNews'); await pg.wait_for_timeout(600)
        print('news:', await pg.inner_text('#newsStatus'))
        await pg.click('#askBtn'); await pg.wait_for_timeout(200); await pg.click('#askSave'); await pg.wait_for_timeout(200)
        await pg.screenshot(path=shot('07-news.png'), full_page=True)
        await pg.click('.nav button[data-go=home]'); await pg.wait_for_timeout(400); await pg.screenshot(path=shot('08-home.png'), full_page=True)
        st=await store(pg); print('settings/app', st.get('settings/app'))
        print('ERRORS desktop:', errs)
        pg2, errs2 = await page_for(b, 400, dark=True)
        await pg2.click('#demoOn'); await pg2.wait_for_timeout(400); await pg2.screenshot(path=shot('09-phone-dark-home.png'), full_page=True)
        await pg2.click('.pf-card >> nth=0'); await pg2.wait_for_timeout(400); await pg2.screenshot(path=shot('10-phone-dark-pf.png'), full_page=True)
        await pg2.click('#v-pf .pf-head [data-act=invest]'); await pg2.wait_for_timeout(200); await pg2.screenshot(path=shot('11-phone-invest.png'))
        print('phone scrollWidth', await pg2.evaluate('document.documentElement.scrollWidth'), 'ERRORS phone:', errs2)
        pg3, errs3 = await page_for(b, 1200)
        await pg3.click('#demoOn'); await pg3.wait_for_timeout(400); await pg3.screenshot(path=shot('12-demo-home.png'), full_page=True)
        await pg3.click('.nav button[data-go=charts]'); await pg3.wait_for_timeout(400); await pg3.screenshot(path=shot('13-demo-charts.png'))
        print('ERRORS demo:', errs3)
        await b.close()
asyncio.run(main())
