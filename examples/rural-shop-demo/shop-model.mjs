/**
 * Shared, deterministic shop rules for the three rural-shop interface samples.
 * These are demonstration values, not a change to an existing game's rules.
 * State is in memory. All quantities are whole units; one unit uses one slot.
 */
export const DEMO_NOTICE = '界面小样 · 演示价格与库存 · 每份商品占 1 格';

export const PRODUCTS = Object.freeze([
  {
    id: 'cabbage', name: '小青菜种子', fullName: '春秋早熟小青菜种子',
    price: 12, unit: '包', seasons: ['春', '秋'], growthDays: 4, initialStock: 12,
    description: '一包种下一畦小青菜。生长快，适合给春日菜篮添一把嫩叶。',
    plantingNote: '适种春、秋；播种后 4 天成熟。每天浇水，成熟后收获一次。',
    effect: '种植小青菜 · 4 天成熟', iconIndex: 0,
  },
  {
    id: 'radish', name: '白萝卜种子', fullName: '清甜白萝卜种子',
    price: 18, unit: '包', seasons: ['春', '秋'], growthDays: 6, initialStock: 8,
    description: '长成脆甜的白萝卜，可留着炖汤，也可在集市出售。',
    plantingNote: '适种春、秋；播种后 6 天成熟。每天浇水，成熟后收获一次。',
    effect: '种植白萝卜 · 6 天成熟', iconIndex: 1,
  },
  {
    id: 'rice', name: '水稻种子', fullName: '江南早稻种子',
    price: 28, unit: '袋', seasons: ['春', '夏'], growthDays: 8, initialStock: 6,
    description: '一袋稻种，用于水田育苗。留一块田，秋前就能闻见新米香。',
    plantingNote: '适种春、夏；播种后 8 天成熟。需种在水田，保持田中有水。',
    effect: '种植水稻 · 8 天成熟', iconIndex: 2,
  },
  {
    id: 'chili', name: '朝天椒种子', fullName: '红果朝天椒种子',
    price: 24, unit: '包', seasons: ['夏'], growthDays: 7, initialStock: 10,
    description: '小小一株，结一簇红辣椒。现在可以买回家，等入夏再播种。',
    plantingNote: '适种夏季；播种后 7 天成熟。当前是春季，可先购买并存放。',
    effect: '种植朝天椒 · 夏季播种', iconIndex: 3,
  },
  {
    id: 'blueberry', name: '四季蓝莓盆栽苗', fullName: '四季蓝莓盆栽苗（带营养土）',
    price: 48, unit: '盆', seasons: ['春', '秋'], growthDays: 12, initialStock: 0,
    description: '已经配好营养土的蓝莓小苗。摆在院里慢慢养，等第一串果子变蓝。',
    plantingNote: '适宜在春、秋定植；养护 12 天结出第一批果。今天已售罄。',
    effect: '栽培蓝莓 · 12 天首熟', iconIndex: 4,
  },
  {
    id: 'compost', name: '腐熟农家堆肥', fullName: '腐熟农家堆肥（稻壳混合装）',
    price: 16, unit: '袋', seasons: ['通用'], growthDays: 0, initialStock: 9,
    description: '稻壳与草叶充分腐熟后的肥料。播种前拌进土里，让菜地更肥沃。',
    plantingNote: '四季通用；对一块空耕地使用，立即施肥。小样只演示购买。',
    effect: '一块空耕地施肥 · 即时使用', iconIndex: 5,
  },
].map(product => Object.freeze({ ...product, seasons: Object.freeze(product.seasons) })));

const BY_ID = new Map(PRODUCTS.map(product => [product.id, product]));
const INITIAL_OWNED = Object.freeze({ cabbage: 2, radish: 1, rice: 0, chili: 0, blueberry: 0, compost: 0 });
const isCount = value => Number.isSafeInteger(value) && value >= 0;

export const SCENARIOS = Object.freeze([
  Object.freeze({ id: 'normal', label: '正常营业', description: '240 钱，背包 9 / 24 格；蓝莓苗今天已售罄。' }),
  Object.freeze({ id: 'low-money', label: '钱不够', description: '审核场景：只剩 12 钱，可买一包小青菜，其他商品会提示缺款。' }),
  Object.freeze({ id: 'full-bag', label: '背包已满', description: '审核场景：背包 24 / 24 格，购买前需要腾出空间。' }),
  Object.freeze({ id: 'sold-out', label: '全部售罄', description: '审核场景：所有商品库存为 0，购买不会扣钱。' }),
]);

export function createState() {
  return {
    balance: 240,
    capacity: 24,
    used: 9,
    owned: { ...INITIAL_OWNED },
    stock: Object.fromEntries(PRODUCTS.map(product => [product.id, product.initialStock])),
    season: '春',
    version: 0,
    scenario: 'normal',
    purchaseCount: 0,
    lastReceipt: null,
  };
}

export const reset = () => createState();

export function scenarioState(key = 'normal') {
  if (!SCENARIOS.some(scenario => scenario.id === key)) {
    throw new RangeError(`Unknown review scenario: ${String(key)}`);
  }
  const state = createState();
  state.scenario = key;
  if (key === 'low-money') state.balance = 12;
  if (key === 'full-bag') state.used = state.capacity;
  if (key === 'sold-out') state.stock = Object.fromEntries(PRODUCTS.map(product => [product.id, 0]));
  return state;
}

function validState(state) {
  return Boolean(state && isCount(state.balance) && isCount(state.capacity)
    && isCount(state.used) && state.used <= state.capacity && isCount(state.version)
    && isCount(state.purchaseCount) && state.stock && state.owned
    && PRODUCTS.every(product => isCount(state.stock[product.id]) && isCount(state.owned[product.id])));
}

function rejectedQuote(code, reason, productId, quantity, product = null) {
  return {
    ok: false, canBuy: false, code, reason, productId, quantity, product,
    unitPrice: product?.price ?? null, total: null, balance: null, balanceAfter: null,
    used: null, usedAfter: null, capacity: null, freeSlots: null, stock: null,
    stockAfter: null, owned: null, ownedAfter: null, maxQuantity: 0, stateVersion: null,
    blockers: [{ code, reason }], shortfall: null,
  };
}

/** Quote without mutating state. Quantity must be a number, not a numeric string. */
export function quote(state, productId, quantity = 1) {
  const product = BY_ID.get(productId);
  if (!product) return rejectedQuote('UNKNOWN_PRODUCT', '找不到这件商品，请重新选择。', productId, quantity);
  if (!Number.isSafeInteger(quantity) || quantity < 1 || quantity > 99) {
    return rejectedQuote('INVALID_QUANTITY', '购买数量须为 1 至 99 的整数。', productId, quantity, product);
  }
  if (!validState(state)) {
    return rejectedQuote('INVALID_STATE', '演示数据异常，请恢复初始状态后再试。', productId, quantity, product);
  }

  const total = product.price * quantity;
  const stock = state.stock[productId];
  const freeSlots = state.capacity - state.used;
  const shortfall = {
    money: Math.max(0, total - state.balance),
    slots: Math.max(0, quantity - freeSlots),
    stock: Math.max(0, quantity - stock),
  };
  const blockers = [];
  if (stock === 0) blockers.push({ code: 'SOLD_OUT', reason: '今天已售罄，请选其他商品。' });
  else if (quantity > stock) blockers.push({ code: 'INSUFFICIENT_STOCK', reason: `只剩 ${stock} ${product.unit}，请减少数量。` });
  if (shortfall.money) blockers.push({ code: 'INSUFFICIENT_FUNDS', reason: `还差 ${shortfall.money} 钱，请减少数量或选其他商品。` });
  if (shortfall.slots) blockers.push({ code: 'INSUFFICIENT_CAPACITY', reason: `背包还需腾出 ${shortfall.slots} 格，请减少数量或整理背包。` });
  const canBuy = blockers.length === 0;
  return {
    ok: canBuy, canBuy,
    code: canBuy ? 'OK' : blockers[0].code,
    reason: canBuy ? `花费 ${total} 钱，购买 ${quantity} ${product.unit}${product.name}。` : blockers[0].reason,
    productId, quantity, product, unitPrice: product.price, total,
    balance: state.balance, balanceAfter: state.balance - total,
    used: state.used, usedAfter: state.used + quantity, capacity: state.capacity, freeSlots,
    stock, stockAfter: stock - quantity,
    owned: state.owned[productId], ownedAfter: state.owned[productId] + quantity,
    maxQuantity: Math.max(0, Math.min(99, stock, freeSlots, Math.floor(state.balance / product.price))),
    stateVersion: state.version, blockers, shortfall,
  };
}

/**
 * Apply one synchronous purchase. Caller keeps the returned state.
 * Pass the displayed quote's stateVersion as expectedVersion to reject replayed
 * confirmations. The UI should additionally disable repeated activation while
 * displaying an in-progress state. A new, intentional buy is a new transaction.
 */
export function purchase(state, productId, quantity = 1, options = {}) {
  const currentQuote = quote(state, productId, quantity);
  if (validState(state) && options.expectedVersion !== undefined && options.expectedVersion !== state.version) {
    return {
      ok: false, code: 'STALE_QUOTE', reason: '库存或余额已变化，请重新确认本次购买。',
      state, receipt: null, quote: currentQuote,
    };
  }
  if (!currentQuote.canBuy) {
    return { ok: false, code: currentQuote.code, reason: currentQuote.reason, state, receipt: null, quote: currentQuote };
  }

  const receipt = Object.freeze({
    id: `purchase-${state.purchaseCount + 1}`,
    productId, productName: currentQuote.product.name, quantity,
    unit: currentQuote.product.unit, unitPrice: currentQuote.unitPrice, total: currentQuote.total,
    balanceBefore: state.balance, balanceAfter: currentQuote.balanceAfter,
    usedBefore: state.used, usedAfter: currentQuote.usedAfter,
    ownedAfter: currentQuote.ownedAfter, stockAfter: currentQuote.stockAfter,
    message: `已购入 ${quantity} ${currentQuote.product.unit}${currentQuote.product.name}，花费 ${currentQuote.total} 钱。`,
  });
  const nextState = {
    ...state,
    balance: currentQuote.balanceAfter,
    used: currentQuote.usedAfter,
    owned: { ...state.owned, [productId]: currentQuote.ownedAfter },
    stock: { ...state.stock, [productId]: currentQuote.stockAfter },
    version: state.version + 1,
    purchaseCount: state.purchaseCount + 1,
    lastReceipt: receipt,
  };
  return { ok: true, code: 'OK', reason: receipt.message, state: nextState, receipt, quote: currentQuote };
}
