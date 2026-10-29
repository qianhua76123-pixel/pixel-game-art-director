import { PRODUCTS, createState, quote, purchase, scenarioState } from './shop-model.mjs';
const $ = id => document.getElementById(id);
let state = createState(), selectedId = PRODUCTS[0].id, quantity = 1, variant = 'wood', opened = true, busy = false;
let lastMessage = '选好种子，再定数量。';
const variantCopy = {
  wood: {heading:'青禾种子铺', kicker:'阿禾婶的春日货架', catalog:'今日货架', action:'买下', footer:'先看时节，再看余钱。', note:'一 · 稳定的列表与详情，同屏比较'},
  ledger: {heading:'青禾铺 · 春账', kicker:'四日晴 · 买种账', catalog:'货名与价目', action:'记账购入', footer:'货钱两清，春种入囊。', note:'二 · 左页挑货，右页算账；把交易写进账本'},
  world: {heading:'阿禾婶的种子铺', kicker:'青禾村 · 当面买种', catalog:'挑些种子', action:'买下', footer:'', note:'三 · 从店主进入，交易时保留村落与人物'}
};
function iconPosition(el, index) {
  el.style.setProperty('--sx', `${(index % 3) * 50}%`);
  el.style.setProperty('--sy', `${Math.floor(index / 3) * 100}%`);
}
for (const p of PRODUCTS) {
  const button = document.createElement('button');
  button.type = 'button'; button.className = 'product'; button.dataset.product = p.id;
  button.setAttribute('aria-pressed','false');
  const icon = document.createElement('span'); icon.className='item-art'; icon.setAttribute('aria-hidden','true'); iconPosition(icon,p.iconIndex);
  const name = document.createElement('span'); name.className='product-name'; name.textContent=p.name;
  const price = document.createElement('span'); price.className='product-price';
  const priceText=document.createElement('span');priceText.textContent=p.price+' 钱';
  const stock=document.createElement('span');stock.className='product-stock';
  price.append(priceText,stock); button.append(icon,name,price); $('product-list').append(button);
  button.addEventListener('click',()=>{selectedId=p.id;paint();});
  button.addEventListener('keydown',event=>{
    const keys=['ArrowDown','ArrowUp','ArrowLeft','ArrowRight','Home','End']; if(!keys.includes(event.key))return;
    event.preventDefault();const index=PRODUCTS.findIndex(p=>p.id===selectedId);const gridStyle=getComputedStyle($('product-list'));
    const columns=gridStyle.display==='grid'?gridStyle.gridTemplateColumns.split(/\s+/).length:1;
    const step=['ArrowDown','ArrowUp'].includes(event.key)?columns:1;
    let next=event.key==='Home'?0:event.key==='End'?PRODUCTS.length-1:index+(['ArrowDown','ArrowRight'].includes(event.key)?step:-step);
    next=(next+PRODUCTS.length)%PRODUCTS.length;selectedId=PRODUCTS[next].id;paint();document.querySelector(`[data-product="${selectedId}"]`).focus();
  });
}
function paint() {
  const p=PRODUCTS.find(x=>x.id===selectedId), q=quote(state,selectedId,quantity), copy=variantCopy[variant];
  document.body.dataset.variant=variant;document.body.dataset.shopOpen=String(opened);
  $('shop').hidden=!opened;$('shop-entry').hidden=opened;$('welcome').hidden=opened;
  for(const button of document.querySelectorAll('nav [data-variant]'))button.setAttribute('aria-pressed',String(button.dataset.variant===variant));
  $('shop-heading').textContent=copy.heading;$('surface-kicker').textContent=copy.kicker;$('catalog-label').textContent=copy.catalog;
  $('mode-note').textContent=copy.note;$('shop-footer-note').textContent=copy.footer;
  for(const button of document.querySelectorAll('[data-product]')){
    const product=PRODUCTS.find(p=>p.id===button.dataset.product),stock=state.stock[product.id];
    button.setAttribute('aria-pressed',String(product.id===selectedId));button.classList.toggle('sold-out',stock===0);
    button.querySelector('.product-stock').textContent=stock===0?'今日售罄':`余 ${stock} ${product.unit}`;
    button.setAttribute('aria-label',`${product.name}，${product.price} 钱，${stock===0?'今日售罄':`余 ${stock} ${product.unit}`}`);
    button.title=product.fullName+(stock===0?' · 今日售罄':'');
  }
  $('balance').textContent=state.balance+' 钱';$('bag').textContent=`${state.used} / ${state.capacity} 格`;
  $('world-coins').textContent=state.balance+' 钱';$('world-bag').textContent=`行囊 ${state.used} / ${state.capacity}`;
  $('item-name').textContent=p.fullName;$('item-owned').textContent=`行囊已有 ${state.owned[p.id]} ${p.unit} · 店里余 ${state.stock[p.id]} ${p.unit}`;
  $('item-category').textContent=p.growthDays?`${p.seasons.join('、')}季适种 · ${p.unit==='盆'?'苗木':'种子'}`:'四季通用 · 农事用品';
  $('description').textContent=p.description;
  const growingNotes={cabbage:'每天浇水；成熟后收获一次。',radish:'每天浇水；成熟后收获一次。',rice:'需要水田；保持田中有水。',chili:'春季可购买；请等夏季再播种。',blueberry:'已配营养土；今天已售罄。',compost:'对一块空耕地使用，即刻施肥。'};
  $('planting-note').textContent=growingNotes[p.id];$('planting-note').title=p.plantingNote;
  $('planting-note').classList.toggle('out-of-season',!p.seasons.includes(state.season)&&!p.seasons.includes('通用'));
  $('growth-label').textContent=p.growthDays?'长成':'使用';$('growth').textContent=p.growthDays?p.growthDays+' 天':'即时';
  $('seasons').textContent=p.seasons.join(' / ');$('unit-price').textContent=p.price+' 钱';
  iconPosition($('detail-art'),p.iconIndex);$('detail-art').setAttribute('aria-label',p.name+'图标');
  $('minus').disabled=busy||(Number.isFinite(quantity)&&quantity<=1);$('plus').disabled=busy||(Number.isFinite(quantity)&&quantity>=99);
  document.querySelector('.quantity-unit').textContent=p.unit;
  $('total').textContent=q.total===null?'—':q.total+' 钱';
  $('remaining').textContent=q.balanceAfter===null?'—':q.balanceAfter<0?'差 '+(-q.balanceAfter)+' 钱':q.balanceAfter+' 钱';
  $('remaining').classList.toggle('negative',q.balanceAfter!==null&&q.balanceAfter<0);
  $('blocker').textContent=q.canBuy?'':q.blockers.map(x=>x.reason).join(' ');
  $('buy').disabled=busy||!q.canBuy;
  $('buy-label').textContent=busy?'正在结账…':q.canBuy?`${copy.action} ${quantity} ${p.unit}`:q.code==='SOLD_OUT'?'今日售罄':q.code==='INSUFFICIENT_FUNDS'?'钱还不够':q.code==='INSUFFICIENT_CAPACITY'?'先腾出行囊':'暂时无法购买';
  $('buy-cost').textContent=q.total===null?'':q.total+' 钱';
  $('receipt').textContent=lastMessage;
}
function chooseVariant(id) {
  if(!variantCopy[id])return;variant=id;opened=id!=='world';paint();
  history.replaceState(null,'','#'+id);
}
function setQuantity(value) {quantity=value; $('quantity').value=Number.isNaN(value)?'':String(value);paint();}
function openShop() {opened=true;paint();document.querySelector(`[data-product="${selectedId}"]`).focus();}
function closeShop() {opened=false;paint();$('shop-entry').focus();}
for(const button of document.querySelectorAll('nav [data-variant]'))button.addEventListener('click',()=>chooseVariant(button.dataset.variant));
$('quantity').addEventListener('input',()=>{quantity=$('quantity').value===''?NaN:Number($('quantity').value);paint();});
$('minus').addEventListener('click',()=>setQuantity(Number.isFinite(quantity)?Math.max(1,quantity-1):1));
$('plus').addEventListener('click',()=>setQuantity(Number.isFinite(quantity)?Math.min(99,quantity+1):1));
$('buy').addEventListener('click',()=>{
  if(busy)return;const q=quote(state,selectedId,quantity);const result=purchase(state,selectedId,quantity,{expectedVersion:q.stateVersion});
  if(!result.ok){lastMessage=result.reason;paint();return;}
  state=result.state;busy=true;lastMessage=`${result.receipt.message} 钱袋还剩 ${state.balance} 钱。`;paint();
  setTimeout(()=>{busy=false;paint();},450);
});
$('shop-entry').addEventListener('click',openShop);$('close-shop').addEventListener('click',closeShop);
function loadScenario(key) {state=scenarioState(key);quantity=1;$('quantity').value='1';selectedId='cabbage';lastMessage=key==='normal'?'选好种子，再定数量。':'已切换审核场景；上方可恢复初始状态。';paint();}
$('scenario').addEventListener('change',()=>loadScenario($('scenario').value));
$('reset').addEventListener('click',()=>{$('scenario').value='normal';loadScenario('normal');});
document.addEventListener('keydown',event=>{
  if(event.key==='Escape'&&opened){event.preventDefault();closeShop();return;}
  if(event.target instanceof HTMLInputElement||event.target instanceof HTMLSelectElement)return;
  if(event.key.toLowerCase()==='e'&&!opened){event.preventDefault();openShop();}
});
if(variantCopy[location.hash.slice(1)])chooseVariant(location.hash.slice(1));else paint();
