import test from 'node:test';
import assert from 'node:assert/strict';
import { computeParallelBatches, statusReport, validateResult, validateRun } from '../src/core.mjs';
import config from '../config.json' with { type: 'json' };

function item(id, overrides = {}) {
  return {
    id,
    title: id,
    kind: 'specification',
    domains: ['cli'],
    objective: 'Doğrulanabilir çıktı üret.',
    responsibility: 'Yalnız atanmış kapsam.',
    inputs: [],
    outputs: ['artifact'],
    acceptanceCriteria: ['çıktı doğrulandı'],
    capabilities: [],
    relations: { dependsOn: [], reviews: [], verifies: [], revises: [], integrates: [] },
    risk: { level: 'low', reasons: [], approvalBoundaries: [] },
    execution: { mode: 'delegate', isolation: 'platform-default', readOnly: true, independent: false, writeScopes: [], preferredPlatforms: ['codex'], owner: null },
    status: 'ready', attempt: 0, resultRef: null,
    ...overrides
  };
}

function run(items) {
  return {
    schemaVersion: '1.0.0', runId: 'test-run', title: 'Test', goal: 'Test graph',
    createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), revision: 0,
    context: { requiredPaths: [], optionalPaths: [], catalogSnapshot: null, assumptions: [] },
    constraints: [], policy: { requiresIntegration: false }, decisions: [], items
  };
}

test('valid read-only graph passes', () => {
  const result = validateRun(run([item('scope-item')]), config);
  assert.equal(result.valid, true);
});

test('dependency cycle fails', () => {
  const a = item('item-a'); const b = item('item-b');
  a.relations.dependsOn = ['item-b']; b.relations.dependsOn = ['item-a'];
  assert.equal(validateRun(run([a, b]), config).valid, false);
});

test('disjoint writers share a batch and overlapping writers serialize', () => {
  const writer = (id, scope) => item(id, { kind: 'implement', execution: { mode: 'delegate', isolation: 'worktree', readOnly: false, independent: false, writeScopes: [scope], preferredPlatforms: ['codex'], owner: null } });
  const batches = computeParallelBatches(run([writer('writer-a', 'cli/src'), writer('writer-b', 'observability-gateway'), writer('writer-c', 'cli/src/sentinel_cli')]), config);
  assert.deepEqual(batches[0], ['writer-a', 'writer-b']);
  assert.deepEqual(batches[1], ['writer-c']);
});

test('pass result requires all acceptance evidence', () => {
  const work = item('verify-me'); const graph = run([work]);
  const result = { schemaVersion: '1.0.0', runId: graph.runId, itemId: work.id, agent: { platform: 'manual', identity: 'tester', sessionRef: null }, outcome: 'pass', summary: 'ok', artifacts: [], acceptance: [{ criterion: 'çıktı doğrulandı', status: 'not_verified', evidence: 'çalıştırılmadı' }], checks: [], risks: [], followUps: [], completedAt: new Date().toISOString() };
  assert.equal(validateResult(result, graph, work).valid, false);
});

test('status exposes safe batches', () => {
  const report = statusReport(run([item('ready-item')]), config);
  assert.deepEqual(report.batches, [['ready-item']]);
});

test('git-checkpoint items do not require independent gates', () => {
  const checkpoint = item('push-checkpoint', { kind: 'git-checkpoint', status: 'draft' });
  const result = validateRun(run([checkpoint]), config);
  assert.equal(result.valid, true);
  assert.equal(result.warnings.some((warning) => warning.includes('bağımsız review')), false);
});
