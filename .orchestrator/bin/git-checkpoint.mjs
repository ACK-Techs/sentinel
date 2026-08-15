#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const TYPES = new Set(['feat', 'fix', 'docs', 'test', 'refactor', 'perf', 'build', 'ci', 'chore', 'revert']);
export const PHASES = new Set([
  'phase-cli-runtime',
  'phase-observability-gateway',
  'phase-test-platform',
  'phase-installers',
  'phase-charts',
  'phase-ops-lab',
  'phase-skills-docs',
  'phase-security',
  'phase-ci',
  'phase-orchestrator',
]);

function fail(message) {
  process.stderr.write(`Git checkpoint error: ${message}\n`);
  process.exit(1);
}

function git(args, options = {}) {
  try {
    return execFileSync('git', args, {
      cwd: options.cwd ?? process.cwd(),
      encoding: 'utf8',
      stdio: options.stdio ?? ['ignore', 'pipe', 'pipe'],
      env: options.env ?? process.env
    }).trim();
  } catch (error) {
    const detail = error.stderr?.toString().trim() || error.message;
    fail(`git ${args.join(' ')} failed: ${detail}`);
  }
}

function tryGit(args, options = {}) {
  try {
    return {
      ok: true,
      output: execFileSync('git', args, {
        cwd: options.cwd ?? process.cwd(),
        encoding: 'utf8',
        stdio: ['ignore', 'pipe', 'pipe'],
        env: options.env ?? process.env
      }).trim()
    };
  } catch (error) {
    return {
      ok: false,
      output: '',
      error: error.stderr?.toString().trim() || error.message
    };
  }
}

function parseOptions(values) {
  const options = {};
  for (let index = 0; index < values.length; index += 1) {
    const token = values[index];
    if (!token.startsWith('--')) fail(`unexpected argument: ${token}`);
    const value = values[index + 1];
    if (!value || value.startsWith('--')) fail(`missing value for ${token}`);
    options[token.slice(2)] = value;
    index += 1;
  }
  return options;
}

export function validateCommitMessage(message, label = 'commit') {
  const normalized = message.replace(/\r\n/g, '\n').trim();
  const lines = normalized.split('\n');
  const subject = lines[0] ?? '';

  if (/^Merge\b/.test(subject)) return [];

  const errors = [];
  const match = /^([a-z]+)\(([a-z0-9]+(?:-[a-z0-9]+)*)\): ([a-z0-9][^.]*)$/.exec(subject);
  if (!match) {
    errors.push('subject must match type(scope): lowercase imperative English summary without a final period');
  } else if (!TYPES.has(match[1])) {
    errors.push(`unsupported type: ${match[1]}`);
  }

  if (subject.length > 72) errors.push(`subject is ${subject.length} characters; maximum is 72`);
  if (/^(fixup|squash)!/.test(subject)) errors.push('fixup/squash commits cannot enter a checkpoint');

  const workItems = lines.filter((line) => /^Work-Item:\s+\S+/.test(line));
  const phaseLines = lines.filter((line) => /^Phase:\s+\S+/.test(line));
  if (workItems.length > 1) errors.push('at most one Work-Item footer is allowed');
  if (phaseLines.length > 1) {
    errors.push('at most one Phase footer is allowed');
  } else if (phaseLines.length === 1) {
    const phase = phaseLines[0].replace(/^Phase:\s+/, '').trim();
    if (!PHASES.has(phase)) errors.push(`unsupported Phase footer: ${phase}`);
  }

  return errors.map((error) => `${label}: ${error}`);
}

function validateMessageFile(file) {
  const errors = validateCommitMessage(fs.readFileSync(path.resolve(file), 'utf8'), file);
  if (errors.length) fail(errors.join('\n'));
  process.stdout.write(`Commit message valid: ${file}\n`);
}

function commitsInRange(base, head) {
  if (/^0+$/.test(base)) return git(['rev-list', '--reverse', head]).split('\n').filter(Boolean);
  return git(['rev-list', '--reverse', `${base}..${head}`]).split('\n').filter(Boolean);
}

function validateRange(base, head) {
  const commits = commitsInRange(base, head);
  const errors = [];
  for (const sha of commits) {
    const message = git(['show', '-s', '--format=%B', sha]);
    errors.push(...validateCommitMessage(message, sha));
  }
  if (errors.length) fail(errors.join('\n'));
  process.stdout.write(`Validated ${commits.length} commit(s) in ${base}..${head}\n`);
}

function requireCheckpoint(runPath, itemId) {
  const absolute = path.resolve(runPath);
  const run = JSON.parse(fs.readFileSync(absolute, 'utf8'));
  const item = run.items?.find((candidate) => candidate.id === itemId);
  if (!item) fail(`checkpoint item not found: ${itemId}`);
  if (item.kind !== 'git-checkpoint') fail(`${itemId} kind must be git-checkpoint`);
  if (!['ready', 'active'].includes(item.status)) fail(`${itemId} must be ready or active before push; got ${item.status}`);
  const map = new Map(run.items.map((candidate) => [candidate.id, candidate]));
  const dependencies = item.relations?.dependsOn ?? [];
  if (!dependencies.length) fail(`${itemId} must depend on accepted checkpoint inputs`);
  const incomplete = dependencies.filter((id) => map.get(id)?.status !== 'done');
  if (incomplete.length) fail(`checkpoint dependencies are not done: ${incomplete.join(', ')}`);
  return { runId: run.runId, itemId };
}

function pushCheckpoint(values) {
  const options = parseOptions(values);
  if (options.as !== 'upper-orchestrator') fail('push requires --as upper-orchestrator');
  if (!options.run || !options.item) fail('push requires --run and --item');

  const remote = options.remote ?? 'origin';
  const branch = options.branch ?? 'main';
  const repoRoot = git(['rev-parse', '--show-toplevel']);
  const currentBranch = git(['branch', '--show-current']);
  if (currentBranch !== branch) fail(`current branch is ${currentBranch}; expected ${branch}`);
  if (!git(['remote']).split('\n').includes(remote)) fail(`remote does not exist: ${remote}`);

  const checkpoint = requireCheckpoint(options.run, options.item);

  execFileSync(process.execPath, ['.orchestrator/bin/orchestrator.mjs', 'verify-system'], {
    cwd: repoRoot,
    stdio: 'inherit'
  });

  const remoteRef = `${remote}/${branch}`;
  const remoteHead = tryGit(['ls-remote', '--heads', remote, `refs/heads/${branch}`], { cwd: repoRoot });
  if (!remoteHead.ok) fail(`cannot inspect ${remote}/${branch}: ${remoteHead.error}`);

  let outgoing;
  if (remoteHead.output) {
    git(['fetch', remote, branch], { cwd: repoRoot });
    git(['merge-base', '--is-ancestor', remoteRef, 'HEAD'], { cwd: repoRoot });
    outgoing = git(['rev-list', '--reverse', `${remoteRef}..HEAD`], { cwd: repoRoot }).split('\n').filter(Boolean);
  } else {
    outgoing = git(['rev-list', '--reverse', 'HEAD'], { cwd: repoRoot }).split('\n').filter(Boolean);
  }
  if (!outgoing.length) fail(`no outgoing commits for ${remoteRef}`);

  const errors = [];
  for (const sha of outgoing) {
    const message = git(['show', '-s', '--format=%B', sha], { cwd: repoRoot });
    errors.push(...validateCommitMessage(message, sha));
  }
  if (errors.length) fail(errors.join('\n'));

  git(['push', remote, `HEAD:${branch}`], {
    cwd: repoRoot,
    stdio: 'inherit',
    env: { ...process.env, SENTINEL_UPPER_ORCHESTRATOR: '1' }
  });

  const sha = git(['rev-parse', 'HEAD'], { cwd: repoRoot });
  process.stdout.write(`${JSON.stringify({
    outcome: 'pushed',
    runId: checkpoint.runId,
    itemId: checkpoint.itemId,
    remote,
    branch,
    sha,
    commitCount: outgoing.length
  }, null, 2)}\n`);
}

function usage() {
  process.stdout.write(`Usage:\n  git-checkpoint.mjs validate-message <file>\n  git-checkpoint.mjs validate-range <base> <head>\n  git-checkpoint.mjs push --as upper-orchestrator --run <run.json> --item <id> [--remote origin] [--branch main]\n`);
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const [command, ...values] = process.argv.slice(2);
  if (command === 'validate-message' && values.length === 1) validateMessageFile(values[0]);
  else if (command === 'validate-range' && values.length === 2) validateRange(values[0], values[1]);
  else if (command === 'push') pushCheckpoint(values);
  else {
    usage();
    process.exit(command ? 1 : 0);
  }
}
