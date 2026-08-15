import test from 'node:test';
import assert from 'node:assert/strict';
import { validateCommitMessage } from '../bin/git-checkpoint.mjs';

test('accepts type(scope): summary without footers', () => {
  assert.deepEqual(validateCommitMessage('feat(gateway): keep telemetry queries behind the read-only api'), []);
});

test('accepts optional work-item and phase footers', () => {
  const message = `feat(gateway): keep telemetry queries behind the read-only api

Work-Item: gateway-readonly-014
Phase: phase-observability-gateway`;
  assert.deepEqual(validateCommitMessage(message), []);
});

test('rejects vague subjects', () => {
  const errors = validateCommitMessage('updates');
  assert.equal(errors.length, 1);
  assert.match(errors.join('\n'), /type\(scope\)/);
});

test('rejects unsupported phases when a phase footer is present', () => {
  const message = `docs(cli): document doctor flags

Phase: someday`;
  assert.match(validateCommitMessage(message).join('\n'), /unsupported Phase/);
});

test('allows generated merge commits', () => {
  assert.deepEqual(validateCommitMessage('Merge branch feature/gateway'), []);
});
