import { createHash, randomUUID } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const ID_PATTERN = /^[a-z0-9][a-z0-9-]{1,62}$/;
const RELATIONS = ['dependsOn', 'reviews', 'verifies', 'revises', 'integrates'];
const GATE_EXEMPT_KINDS = [
  'analysis',
  'specification',
  'review',
  'verify',
  'integration',
  'comparison',
  'pm-planning',
  'git-checkpoint',
  'acceptance',
];

const asArray = (value) => Array.isArray(value) ? value : [];
const nowIso = () => new Date().toISOString();
const normalizePath = (value) => String(value ?? '').replaceAll('\\', '/').replace(/^\.\//, '').replace(/\/$/, '');
const hash = (value) => createHash('sha256').update(value).digest('hex');

function isInside(root, target) {
  const relative = path.relative(path.resolve(root), path.resolve(target));
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

export async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, 'utf8'));
}

export async function writeTextAtomic(filePath, content) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  const temp = `${filePath}.${process.pid}.${Date.now()}.tmp`;
  await fs.writeFile(temp, content, 'utf8');
  await fs.rename(temp, filePath);
}

export async function writeJsonAtomic(filePath, value) {
  await writeTextAtomic(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

export async function loadConfig(repoRoot = REPO_ROOT) {
  return readJson(path.join(repoRoot, '.orchestrator', 'config.json'));
}

export async function assertSafeArtifactPath(targetPath, repoRoot = REPO_ROOT, config = null) {
  if (!isInside(repoRoot, targetPath)) throw new Error(`Artifact repo dışında olamaz: ${targetPath}`);
  const relative = normalizePath(path.relative(repoRoot, targetPath));
  const effective = config ?? await loadConfig(repoRoot);
  for (const prefix of asArray(effective.repoGuardrails?.protectedPrefixes)) {
    const normalized = normalizePath(prefix);
    if (relative === normalized || relative.startsWith(`${normalized}/`)) throw new Error(`Korumalı path: ${relative}`);
  }
  return true;
}

function runDir(runPath) { return path.dirname(runPath); }
function eventsPath(runPath) { return path.join(runDir(runPath), 'events.jsonl'); }
function lockPath(runPath) { return path.join(runDir(runPath), '.lock'); }

async function appendEvent(runPath, event) {
  await fs.mkdir(runDir(runPath), { recursive: true });
  await fs.appendFile(eventsPath(runPath), `${JSON.stringify(event)}\n`, 'utf8');
}

function makeEvent(runId, itemId, type, actor, payload) {
  return { schemaVersion: '1.0.0', eventId: randomUUID(), timestamp: nowIso(), type, actor, runId, itemId, payload };
}

async function withLock(runPath, action) {
  await fs.mkdir(runDir(runPath), { recursive: true });
  let handle;
  try {
    handle = await fs.open(lockPath(runPath), 'wx');
  } catch (error) {
    if (error.code === 'EEXIST') throw new Error('Run başka bir manager tarafından güncelleniyor; status ile uzlaştırıp tekrar deneyin.');
    throw error;
  }
  try { return await action(); }
  finally { await handle.close(); await fs.rm(lockPath(runPath), { force: true }); }
}

function expectedRevision(run, value) {
  if (value === undefined || value === null || value === true) return;
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed !== (run.revision ?? 0)) {
    throw new Error(`Revision uyuşmazlığı: beklenen ${value}, mevcut ${run.revision ?? 0}`);
  }
}

function advance(run) {
  run.revision = (run.revision ?? 0) + 1;
  run.updatedAt = nowIso();
}

function relation(item, key) { return asArray(item?.relations?.[key]); }
function itemMap(run) { return new Map(asArray(run.items).map((item) => [item.id, item])); }
function dependenciesDone(item, map) { return relation(item, 'dependsOn').every((id) => map.get(id)?.status === 'done'); }

function sensitivePaths(value, fragments, current = '$', found = []) {
  if (Array.isArray(value)) value.forEach((entry, index) => sensitivePaths(entry, fragments, `${current}[${index}]`, found));
  else if (value && typeof value === 'object') {
    for (const [key, entry] of Object.entries(value)) {
      if (fragments.some((fragment) => key.toLowerCase().includes(fragment.toLowerCase()))) found.push(`${current}.${key}`);
      sensitivePaths(entry, fragments, `${current}.${key}`, found);
    }
  }
  return found;
}

function hasCycle(items) {
  const map = new Map(items.map((item) => [item.id, item]));
  const visiting = new Set(); const visited = new Set();
  function visit(id) {
    if (visiting.has(id)) return true;
    if (visited.has(id)) return false;
    visiting.add(id);
    for (const dependency of relation(map.get(id), 'dependsOn')) if (visit(dependency)) return true;
    visiting.delete(id); visited.add(id); return false;
  }
  return items.some((item) => visit(item.id));
}

function needsGates(item, config) {
  if (GATE_EXEMPT_KINDS.includes(item.kind)) return false;
  return asArray(config.riskPolicy.forceQualityGateKinds).includes(item.kind) ||
    asArray(config.riskPolicy.independentGateKinds).includes(item.kind) ||
    asArray(config.riskPolicy.requireIndependentReviewAt).includes(item.risk?.level) ||
    asArray(config.riskPolicy.requireVerificationAt).includes(item.risk?.level);
}

function dependentGate(run, targetId, relationName, kinds) {
  return asArray(run.items).find((item) => kinds.includes(item.kind) && relation(item, relationName).includes(targetId));
}

export function validateRun(run, config, catalog = null) {
  const errors = []; const warnings = [];
  if (run?.schemaVersion !== '1.0.0') errors.push('schemaVersion 1.0.0 olmalı.');
  if (!ID_PATTERN.test(run?.runId ?? '')) errors.push('runId formatı geçersiz.');
  if (!run?.title || !run?.goal) errors.push('title ve goal zorunlu.');
  if (!Array.isArray(run?.items)) errors.push('items array olmalı.');
  const items = asArray(run?.items); const ids = new Set(); const map = itemMap(run);
  for (const item of items) {
    if (!ID_PATTERN.test(item?.id ?? '')) errors.push(`Item id geçersiz: ${item?.id}`);
    if (ids.has(item.id)) errors.push(`Tekrarlı item id: ${item.id}`); ids.add(item.id);
    if (!item.title || !item.kind || !item.objective || !item.responsibility) errors.push(`${item.id}: başlık/tür/amaç/sorumluluk eksik.`);
    if (!asArray(item.domains).length) errors.push(`${item.id}: domains boş.`);
    if (!asArray(item.outputs).length || !asArray(item.acceptanceCriteria).length) errors.push(`${item.id}: output ve acceptance zorunlu.`);
    if (!asArray(config.lifecycle.statuses).includes(item.status)) errors.push(`${item.id}: status geçersiz.`);
    if (!asArray(config.riskPolicy.levels).includes(item.risk?.level)) errors.push(`${item.id}: risk geçersiz.`);
    if (!['inline', 'delegate'].includes(item.execution?.mode)) errors.push(`${item.id}: execution.mode geçersiz.`);
    if (item.execution?.readOnly && asArray(item.execution?.writeScopes).length) errors.push(`${item.id}: readOnly item write scope alamaz.`);
    for (const key of RELATIONS) if (!Array.isArray(item.relations?.[key])) errors.push(`${item.id}: relations.${key} array olmalı.`);
  }
  for (const item of items) {
    for (const key of RELATIONS) for (const target of relation(item, key)) {
      if (!map.has(target)) errors.push(`${item.id}.${key}: bilinmeyen hedef ${target}`);
      if (target === item.id) errors.push(`${item.id}.${key}: kendine referans.`);
    }
    if (item.status === 'ready' && !dependenciesDone(item, map)) errors.push(`${item.id}: bağımlılıklar bitmeden ready.`);
    if (needsGates(item, config)) {
      if (!dependentGate(run, item.id, 'reviews', ['review', 'security-review', 'architecture-review'])) warnings.push(`${item.id}: bağımsız review gate eksik.`);
      if (!dependentGate(run, item.id, 'verifies', ['verify', 'test', 'security-verify'])) warnings.push(`${item.id}: verify gate eksik.`);
    }
  }
  if (hasCycle(items)) errors.push('Dependency graph cycle içeriyor.');
  const sensitive = sensitivePaths(run, asArray(config.historyPolicy.redactKeyFragments));
  if (sensitive.length) errors.push(`Hassas anahtarlar run içine yazılamaz: ${sensitive.join(', ')}`);
  if (catalog && run.context?.catalogSnapshot && catalog.snapshot !== run.context.catalogSnapshot) warnings.push('Catalog snapshot değişmiş; context yeniden doğrulanmalı.');
  if (!items.length) warnings.push('Run henüz work item içermiyor.');
  return { valid: errors.length === 0, errors, warnings };
}

export async function validateEventHistory(runPath, run) {
  try {
    const lines = (await fs.readFile(eventsPath(runPath), 'utf8')).split(/\r?\n/).filter(Boolean);
    const events = lines.map((line) => JSON.parse(line));
    const errors = [];
    for (const event of events) if (event.runId !== run.runId) errors.push(`Event runId uyuşmuyor: ${event.eventId}`);
    return { valid: errors.length === 0, count: events.length, errors };
  } catch (error) {
    if (error.code === 'ENOENT') return { valid: false, count: 0, errors: ['events.jsonl bulunamadı.'] };
    return { valid: false, count: 0, errors: [error.message] };
  }
}

function scopesConflict(a, b) {
  const left = asArray(a.execution?.writeScopes).map(normalizePath);
  const right = asArray(b.execution?.writeScopes).map(normalizePath);
  if (a.execution?.readOnly || b.execution?.readOnly) return false;
  if (!left.length || !right.length || left.includes('*') || right.includes('*')) return true;
  return left.some((x) => right.some((y) => x === y || x.startsWith(`${y}/`) || y.startsWith(`${x}/`)));
}

export function pendingApprovalBoundaries(run, item, config) {
  return asArray(item.risk?.approvalBoundaries).filter((boundary) => {
    return !asArray(run.decisions).some((decision) => decision.extensions?.type === 'approval' &&
      decision.extensions.itemId === item.id && decision.extensions.boundary === boundary && decision.extensions.outcome === 'approved');
  });
}

export function qualityGateBlockers(run, config) {
  const blockers = [];
  for (const item of asArray(run.items).filter((candidate) => needsGates(candidate, config))) {
    const review = dependentGate(run, item.id, 'reviews', ['review', 'security-review', 'architecture-review']);
    const verify = dependentGate(run, item.id, 'verifies', ['verify', 'test', 'security-verify']);
    if (!review || review.status !== 'done') blockers.push({ itemId: item.id, gate: 'review', gateItemId: review?.id ?? null });
    if (!verify || verify.status !== 'done') blockers.push({ itemId: item.id, gate: 'verify', gateItemId: verify?.id ?? null });
  }
  return blockers;
}

export function computeParallelBatches(run, config) {
  const map = itemMap(run);
  const runnable = asArray(run.items).filter((item) => item.status === 'ready' && dependenciesDone(item, map) && !pendingApprovalBoundaries(run, item, config).length);
  const batches = [];
  for (const item of runnable) {
    let placed = false;
    for (const batch of batches) {
      const writers = batch.filter((entry) => !entry.execution?.readOnly).length;
      if (writers >= (config.parallelPolicy.defaultMaxWriters ?? 1) && !item.execution?.readOnly) continue;
      if (!batch.some((entry) => scopesConflict(entry, item))) { batch.push(item); placed = true; break; }
    }
    if (!placed) batches.push([item]);
  }
  return batches.map((batch) => batch.map((item) => item.id));
}

export function statusReport(run, config) {
  const counts = Object.fromEntries(asArray(config.lifecycle.statuses).map((status) => [status, asArray(run.items).filter((item) => item.status === status).length]));
  return {
    runId: run.runId, title: run.title, revision: run.revision ?? 0, counts,
    batches: computeParallelBatches(run, config),
    active: asArray(run.items).filter((item) => item.status === 'active').map((item) => ({ id: item.id, owner: item.execution?.owner ?? null })),
    blocked: asArray(run.items).filter((item) => item.status === 'blocked').map((item) => item.id),
    approvalBlockers: asArray(run.items).map((item) => ({ id: item.id, boundaries: pendingApprovalBoundaries(run, item, config) })).filter((entry) => entry.boundaries.length),
    qualityGateBlockers: qualityGateBlockers(run, config),
  };
}

export async function createRun({ id, title, goal, outputDirectory, repoRoot = REPO_ROOT, actor = 'pm-manager' }) {
  if (!ID_PATTERN.test(id)) throw new Error('Run id 2-63 karakter; küçük harf, rakam ve tire olmalı.');
  const config = await loadConfig(repoRoot);
  const directory = outputDirectory ? path.resolve(repoRoot, outputDirectory) : path.join(repoRoot, config.paths.runs, id);
  const runPath = path.join(directory, 'run.json');
  await assertSafeArtifactPath(runPath, repoRoot, config);
  try { await fs.access(runPath); throw new Error(`Run zaten var: ${runPath}`); } catch (error) { if (error.code !== 'ENOENT') throw error; }
  let snapshot = null; try { snapshot = (await readJson(path.join(repoRoot, config.paths.catalog))).snapshot ?? null; } catch {}
  const timestamp = nowIso();
  const run = {
    schemaVersion: '1.0.0', runId: id, title, goal, createdAt: timestamp, updatedAt: timestamp, revision: 0,
    context: { requiredPaths: config.paths.requiredContext, optionalPaths: [], catalogSnapshot: snapshot, assumptions: [] },
    constraints: [
      'Kapsam süre uğruna daraltılmaz; sıra bağımlılık, risk ve acceptance kriterlerine göre belirlenir.',
      'Write item atomik Conventional Commit ile kaydedilir; mesaj type(scope): summary biçimindedir. Work-Item ve Phase footer isteğe bağlıdır. Mesaj uygunsa git add / commit / push serbesttir; force-push yasaktır.',
      'observability-gateway read-only kalır; write, alert, dashboard veya Grafana proxy eklemek gateway-write-expansion approval boundary\'sidir.',
      'agentic/ referans koddur. Ürün cli/, observability-gateway/, test-platform/, charts/, for-download/, scripts/, skills/ ve documantations/ içindedir.',
      'Compose, Kubernetes ve COS kurulum yolları birbirine karıştırılmaz. COS installer tamamlanmış iddia edilmez.',
      'Secret, token, API key, cookie veya ham telemetry dump run/result içine yazılmaz.',
    ],
    policy: { requiresIntegration: false }, decisions: [], items: []
  };
  await writeJsonAtomic(runPath, run); await fs.mkdir(path.join(directory, 'results'), { recursive: true });
  await appendEvent(runPath, makeEvent(id, null, 'run-created', actor, { title, goal }));
  return { runPath, run };
}

export async function syncReady(runPath, actor = 'pm-manager', repoRoot = REPO_ROOT, options = {}) {
  return withLock(runPath, async () => {
    const run = await readJson(runPath); expectedRevision(run, options.expectedRevision); const map = itemMap(run); const changed = [];
    for (const item of asArray(run.items)) if (item.status === 'draft' && dependenciesDone(item, map)) { item.status = 'ready'; changed.push(item.id); }
    if (changed.length) { advance(run); await writeJsonAtomic(runPath, run); for (const id of changed) await appendEvent(runPath, makeEvent(run.runId, id, 'item-ready', actor, { reason: 'dependencies-done' })); }
    return { changed, revision: run.revision ?? 0, report: statusReport(run, await loadConfig(repoRoot)) };
  });
}

export async function transitionItem(runPath, itemId, toStatus, reason, actor = 'pm-manager', options = {}) {
  return withLock(runPath, async () => {
    const config = await loadConfig(); const run = await readJson(runPath); expectedRevision(run, options.expectedRevision); const map = itemMap(run); const item = map.get(itemId);
    if (!item) throw new Error(`Work item bulunamadı: ${itemId}`);
    if (!asArray(config.lifecycle.transitions[item.status]).includes(toStatus)) throw new Error(`Geçersiz transition: ${item.status} -> ${toStatus}`);
    if (['ready', 'active'].includes(toStatus) && !dependenciesDone(item, map)) throw new Error('Bağımlılıklar tamamlanmadı.');
    if (toStatus === 'active' && pendingApprovalBoundaries(run, item, config).length) throw new Error('Approval boundary tamamlanmadı.');
    if (toStatus === 'done' && !item.resultRef) throw new Error('done için result contract zorunlu; record kullanın.');
    const from = item.status; item.status = toStatus; if (toStatus === 'active') item.attempt = (item.attempt ?? 0) + 1;
    advance(run); await writeJsonAtomic(runPath, run); await appendEvent(runPath, makeEvent(run.runId, itemId, 'status-transition', actor, { from, to: toStatus, reason }));
    return { run, item };
  });
}

export function validateResult(result, run, item, config = null) {
  const errors = [];
  if (result?.schemaVersion !== '1.0.0' || result.runId !== run.runId || result.itemId !== item.id) errors.push('Result kimliği veya schemaVersion uyuşmuyor.');
  if (!['pass', 'revise', 'blocked', 'fail'].includes(result.outcome)) errors.push('Result outcome geçersiz.');
  const acceptance = asArray(result.acceptance); const expected = asArray(item.acceptanceCriteria);
  for (const criterion of expected) if (!acceptance.some((entry) => entry.criterion === criterion)) errors.push(`Acceptance eksik: ${criterion}`);
  if (result.outcome === 'pass' && acceptance.some((entry) => entry.status !== 'passed')) errors.push('pass için bütün acceptance kriterleri passed olmalı.');
  if (result.outcome === 'pass' && asArray(result.checks).some((check) => check.status === 'failed')) errors.push('Başarısız check varken pass olamaz.');
  for (const artifact of asArray(result.artifacts)) {
    if (artifact.path && (path.isAbsolute(artifact.path) || normalizePath(artifact.path).startsWith('../'))) errors.push(`Artifact repo-relative olmalı: ${artifact.path}`);
  }
  return { valid: errors.length === 0, errors };
}

export async function recordResult(runPath, resultPath, actor = 'pm-manager', repoRoot = REPO_ROOT, options = {}) {
  return withLock(runPath, async () => {
    const run = await readJson(runPath); expectedRevision(run, options.expectedRevision); const item = itemMap(run).get((await readJson(resultPath)).itemId); const result = await readJson(resultPath);
    if (!item) throw new Error('Result bilinmeyen item için.');
    const validation = validateResult(result, run, item); if (!validation.valid) throw new Error(`Result geçersiz: ${validation.errors.join('; ')}`);
    if (item.execution?.independent && [...relation(item, 'reviews'), ...relation(item, 'verifies')].length) {
      for (const targetId of [...relation(item, 'reviews'), ...relation(item, 'verifies')]) {
        const target = itemMap(run).get(targetId); if (!target?.resultRef) throw new Error(`Review/verify hedef sonucu yok: ${targetId}`);
        const prior = await readJson(path.join(runDir(runPath), target.resultRef));
        if (`${prior.agent.platform}:${prior.agent.identity}:${prior.agent.sessionRef}` === `${result.agent.platform}:${result.agent.identity}:${result.agent.sessionRef}`) throw new Error('Bağımsız gate aynı agent/session tarafından tamamlanamaz.');
      }
    }
    const name = `${item.id}-${result.completedAt.replace(/[:.]/g, '-')}.json`; const stored = path.join(runDir(runPath), 'results', name);
    await writeJsonAtomic(stored, result); item.resultRef = normalizePath(path.relative(runDir(runPath), stored));
    const from = item.status; item.status = ({ pass: 'done', revise: 'failed', blocked: 'blocked', fail: 'failed' })[result.outcome];
    advance(run); await writeJsonAtomic(runPath, run);
    await appendEvent(runPath, makeEvent(run.runId, item.id, 'result-recorded', actor, { outcome: result.outcome, resultRef: item.resultRef }));
    await appendEvent(runPath, makeEvent(run.runId, item.id, 'status-transition', actor, { from, to: item.status, reason: `result:${result.outcome}` }));
    return { itemId: item.id, status: item.status, resultRef: item.resultRef, revision: run.revision };
  });
}

export async function recordDecision(runPath, decision, actor = 'pm-manager', repoRoot = REPO_ROOT, options = {}) {
  return withLock(runPath, async () => {
    const config = await loadConfig(repoRoot); const run = await readJson(runPath); expectedRevision(run, options.expectedRevision);
    if (!ID_PATTERN.test(decision.id) || asArray(run.decisions).some((entry) => entry.id === decision.id)) throw new Error('Decision id geçersiz veya tekrar ediyor.');
    if (decision.extensions?.type === 'approval') {
      const item = itemMap(run).get(decision.extensions.itemId); if (!item) throw new Error('Approval item bulunamadı.');
      if (!asArray(item.risk.approvalBoundaries).includes(decision.extensions.boundary)) throw new Error('Approval boundary item üzerinde yok.');
      if (asArray(config.riskPolicy.requireHumanDecisionFor).includes(decision.extensions.boundary) && !['user-confirmed', 'platform-approved'].includes(decision.extensions.provenance)) throw new Error('Bu boundary kullanıcı/platform onayı gerektirir.');
    }
    const normalized = { ...decision, decidedAt: nowIso(), actor }; run.decisions.push(normalized); advance(run); await writeJsonAtomic(runPath, run);
    await appendEvent(runPath, makeEvent(run.runId, decision.extensions?.itemId ?? null, 'decision-recorded', actor, normalized)); return normalized;
  });
}

async function walk(root, predicate) {
  const output = []; try { for (const entry of await fs.readdir(root, { withFileTypes: true })) { const full = path.join(root, entry.name); if (entry.isDirectory()) output.push(...await walk(full, predicate)); else if (predicate(full)) output.push(full); } } catch (error) { if (error.code !== 'ENOENT') throw error; }
  return output;
}

function gitCommit(repoRoot) { try { return execFileSync('git', ['rev-parse', 'HEAD'], { cwd: repoRoot, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim(); } catch { return null; } }

export async function discoverRepository(repoRoot = REPO_ROOT, outputPath = null) {
  const config = await loadConfig(repoRoot); const skills = [];
  for (const root of asArray(config.paths.skillRoots)) for (const file of await walk(path.join(repoRoot, root), (candidate) => path.basename(candidate) === 'SKILL.md')) {
    const content = await fs.readFile(file, 'utf8'); const name = content.match(/^name:\s*(.+)$/m)?.[1]?.trim() ?? path.basename(path.dirname(file)); const description = content.match(/^description:\s*(.+)$/m)?.[1]?.trim() ?? '';
    skills.push({ name, description, path: normalizePath(path.relative(repoRoot, file)), fingerprint: hash(content) });
  }
  const adapters = [];
  for (const file of await walk(path.join(repoRoot, config.paths.adapters), (candidate) => candidate.endsWith('.json'))) { const value = await readJson(file); adapters.push({ id: value.id, path: normalizePath(path.relative(repoRoot, file)), capabilities: value.nativeCapabilities }); }
  const roots = {};
  for (const root of asArray(config.paths.sourceRoots)) { try { const stat = await fs.stat(path.join(repoRoot, root)); roots[root] = { exists: true, mtimeMs: stat.mtimeMs }; } catch { roots[root] = { exists: false }; } }
  const catalog = {
    schemaVersion: '1.0.0', generatedAt: nowIso(),
    repository: { root: '.', name: path.basename(repoRoot), commit: gitCommit(repoRoot), roots },
    skills, capabilities: [...new Set(skills.map((entry) => entry.name))].sort(),
    maps: { semantic: [], dependency: null },
    mapHealth: { stale: false, note: 'Source roots catalog snapshot ile doğrudan izlenir.' },
    adapters
  };
  const stable = { ...catalog }; delete stable.generatedAt; catalog.snapshot = hash(JSON.stringify(stable));
  const destination = outputPath ? path.resolve(repoRoot, outputPath) : path.join(repoRoot, config.paths.catalog); await writeJsonAtomic(destination, catalog); return { destination, catalog };
}

export async function writeMapManifest(repoRoot = REPO_ROOT) {
  const config = await loadConfig(repoRoot); const manifest = { schemaVersion: '1.0.0', generatedAt: nowIso(), sourceRoots: config.paths.sourceRoots };
  const destination = path.join(repoRoot, '.orchestrator', 'catalog', 'map-manifest.json'); await writeJsonAtomic(destination, manifest); return { destination, manifest };
}

const bullets = (values) => values.length ? values.map((value) => `- ${value}`).join('\n') : '- Yok';

export async function renderPrompt(run, itemId, platform, repoRoot = REPO_ROOT) {
  const item = itemMap(run).get(itemId); if (!item) throw new Error(`Work item bulunamadı: ${itemId}`);
  const adapter = await readJson(path.join(repoRoot, '.orchestrator', 'adapters', `${platform}.json`));
  const inputs = asArray(item.inputs).map((input) => `${input.type}: ${input.value}${input.description ? ` — ${input.description}` : ''}`);
  return `# Orchestrator Handoff\n\nRun: ${run.runId} — ${run.title}\nItem: ${item.id} — ${item.title}\nPlatform: ${adapter.displayName}\n\n` +
    `## Önce okunacaklar\n\n${bullets([...asArray(run.context.requiredPaths), ...asArray(item.inputs).filter((i) => i.type === 'path').map((i) => i.value)])}\n\n` +
    `## Rol\n\n- Kind: ${item.kind}\n- Domains: ${asArray(item.domains).join(', ')}\n- Risk: ${item.risk.level}\n- Capabilities: ${asArray(item.capabilities).join(', ') || 'Yok'}\n\n` +
    `## Amaç\n\n${item.objective}\n\n## Sorumluluk sınırı\n\n${item.responsibility}\n\n## Girdiler\n\n${bullets(inputs)}\n\n` +
    `## Çıktılar\n\n${bullets(asArray(item.outputs))}\n\n## Kabul kriterleri\n\n${bullets(asArray(item.acceptanceCriteria))}\n\n` +
    `## Yazma kapsamı\n\n- Read-only: ${item.execution.readOnly}\n- Paths: ${asArray(item.execution.writeScopes).join(', ') || 'Yok'}\n- Do not touch: agentic/\n\n` +
    `## Proje kuralları\n\n${bullets(asArray(run.constraints))}\n- Kapsam dışı refactor yapma. Write item kontrolleri geçince yalnız atanmış scope'u atomik Conventional Commit ile kaydet; mesajı type(scope): summary biçiminde yaz. Mesaj uygunsa git push serbesttir; force-push yapma. Kritik belirsizlikte blocker sonucu üret.\n\n` +
    `## ${adapter.displayName} notları\n\n${bullets(asArray(adapter.dispatchGuidance))}\n\n` +
    `## Teslim\n\nSonucu \`.orchestrator/contracts/result.schema.json\` biçiminde üret. Rolüne göre \`.orchestrator/roles/\` altındaki talimatı uygula. Implementasyon item'ları \`.orchestrator/roles/code-implementer.md\`, review ve verify item'ları bağımsız rol protokollerini kullanır.\n`;
}

export async function verifySystem(repoRoot = REPO_ROOT) {
  const report = { valid: true, checkedJson: [], errors: [] };
  const roots = ['config.json', 'contracts', 'adapters', 'templates'].map((entry) => path.join(repoRoot, '.orchestrator', entry));
  const files = [];
  for (const root of roots) { try { const stat = await fs.stat(root); if (stat.isFile()) files.push(root); else files.push(...await walk(root, (candidate) => candidate.endsWith('.json'))); } catch (error) { report.errors.push(`${normalizePath(path.relative(repoRoot, root))}: ${error.message}`); } }
  for (const file of files) try { await readJson(file); report.checkedJson.push(normalizePath(path.relative(repoRoot, file))); } catch (error) { report.errors.push(`${normalizePath(path.relative(repoRoot, file))}: ${error.message}`); }
  try { const config = await loadConfig(repoRoot); const required = asArray(config.paths.requiredContext); for (const target of required) await fs.access(path.join(repoRoot, target)); } catch (error) { report.errors.push(`Required context: ${error.message}`); }
  report.valid = report.errors.length === 0; return report;
}
