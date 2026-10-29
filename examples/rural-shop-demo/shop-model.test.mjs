import test from 'node:test';
import assert from 'node:assert/strict';
import { PRODUCTS, createState, reset, quote, purchase, scenarioState } from './shop-model.mjs';

function assertRejectedUnchanged(state, productId, quantity, expectedCode) {
  const before = structuredClone(state);
  const result = purchase(state, productId, quantity);
  assert.equal(result.ok, false);
  assert.equal(result.code, expectedCode);
  assert.equal(result.state, state);
  assert.equal(result.receipt, null);
  assert.deepEqual(state, before);
}

test('shared baseline exposes the same six real Chinese products and capacity rules', () => {
  const state = createState();
  assert.equal(PRODUCTS.length, 6);
  assert.equal(new Set(PRODUCTS.map(p => p.id)).size, 6);
  assert.deepEqual(PRODUCTS.map(p => p.iconIndex), [0, 1, 2, 3, 4, 5]);
  assert.equal(state.balance, 240);
  assert.equal(state.capacity - state.used, 15);
  assert.equal(state.owned.cabbage, 2);
  assert.equal(state.stock.blueberry, 0);
  assert.equal(quote(state, 'cabbage', 3).total, 36);
});

test('one purchase atomically debits money, adds items, consumes slots and stock', () => {
  const initial = createState();
  const before = structuredClone(initial);
  const preview = quote(initial, 'cabbage', 3);
  const result = purchase(initial, 'cabbage', 3, { expectedVersion: preview.stateVersion });
  assert.equal(result.ok, true);
  assert.equal(result.state.balance, 204);
  assert.equal(result.state.owned.cabbage, 5);
  assert.equal(result.state.used, 12);
  assert.equal(result.state.stock.cabbage, 9);
  assert.equal(result.state.version, 1);
  assert.equal(result.receipt.total, 36);
  assert.equal(result.state.lastReceipt, result.receipt);
  assert.deepEqual(initial, before);
  assert.notEqual(result.state.stock, initial.stock);
  assert.notEqual(result.state.owned, initial.owned);
});

test('quote is a side-effect-free preview including money, slots and stock shortfalls', () => {
  const state = { ...scenarioState('low-money'), used: 23 };
  const before = structuredClone(state);
  const q = quote(state, 'radish', 9);
  assert.equal(q.canBuy, false);
  assert.deepEqual(q.shortfall, { money: 150, slots: 8, stock: 1 });
  assert.equal(q.blockers.length, 3);
  assert.equal(q.maxQuantity, 0);
  assert.deepEqual(state, before);
});

test('invalid numeric quantities and unknown goods never change data', () => {
  for (const quantity of [0, -1, 1.5, 100, NaN, Infinity, '2', null, Number.MAX_SAFE_INTEGER]) {
    assertRejectedUnchanged(createState(), 'cabbage', quantity, 'INVALID_QUANTITY');
  }
  assertRejectedUnchanged(createState(), 'missing', 1, 'UNKNOWN_PRODUCT');
  assert.equal(quote(createState(), 'cabbage', 99).code, 'INSUFFICIENT_STOCK');
});

test('insufficient funds, full bags, sold out stock and excess amounts do not debit', () => {
  assertRejectedUnchanged(scenarioState('low-money'), 'radish', 1, 'INSUFFICIENT_FUNDS');
  assertRejectedUnchanged(scenarioState('full-bag'), 'cabbage', 1, 'INSUFFICIENT_CAPACITY');
  assertRejectedUnchanged(createState(), 'blueberry', 1, 'SOLD_OUT');
  assertRejectedUnchanged(createState(), 'cabbage', 13, 'INSUFFICIENT_STOCK');
  for (const product of PRODUCTS) assertRejectedUnchanged(scenarioState('sold-out'), product.id, 1, 'SOLD_OUT');
});

test('exact remaining money and last free slot can be spent once', () => {
  const state = { ...scenarioState('low-money'), used: 23 };
  const result = purchase(state, 'cabbage', 1);
  assert.equal(result.ok, true);
  assert.equal(result.state.balance, 0);
  assert.equal(result.state.used, 24);
  assertRejectedUnchanged(result.state, 'cabbage', 1, 'INSUFFICIENT_FUNDS');
});

test('summer planting information does not prohibit buying chili in spring', () => {
  const state = createState();
  assert.equal(state.season, '春');
  assert.deepEqual(PRODUCTS.find(p => p.id === 'chili').seasons, ['夏']);
  const result = purchase(state, 'chili', 1);
  assert.equal(result.ok, true);
  assert.equal(result.state.balance, 216);
});

test('replaying the displayed quote version cannot apply a second purchase', () => {
  const initial = createState();
  const version = quote(initial, 'cabbage', 2).stateVersion;
  const first = purchase(initial, 'cabbage', 2, { expectedVersion: version });
  const replay = purchase(first.state, 'cabbage', 2, { expectedVersion: version });
  assert.equal(first.ok, true);
  assert.equal(replay.ok, false);
  assert.equal(replay.code, 'STALE_QUOTE');
  assert.equal(replay.state, first.state);
  assert.equal(replay.state.purchaseCount, 1);
  const intentionalSecond = purchase(first.state, 'cabbage', 2, { expectedVersion: first.state.version });
  assert.equal(intentionalSecond.ok, true);
  assert.equal(intentionalSecond.state.purchaseCount, 2);
});

test('fixtures and reset are isolated and recover all state consistently', () => {
  const a = scenarioState('sold-out');
  const b = scenarioState('normal');
  a.stock.cabbage = 200;
  assert.equal(b.stock.cabbage, 12);
  assert.equal(scenarioState('sold-out').stock.cabbage, 0);
  assert.deepEqual(reset(), createState());
  assert.throws(() => scenarioState('unknown'), RangeError);
});

test('corrupted or structurally missing state is rejected safely', () => {
  assert.equal(quote(null, 'cabbage', 1).code, 'INVALID_STATE');
  assertRejectedUnchanged({ ...createState(), used: 25 }, 'cabbage', 1, 'INVALID_STATE');
  assertRejectedUnchanged({ ...createState(), balance: -1 }, 'cabbage', 1, 'INVALID_STATE');
});
