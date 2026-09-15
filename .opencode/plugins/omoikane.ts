/**
 * Omoikane session hooks for OpenCode, the counterpart of .claude/settings.json.
 *
 * - experimental.chat.system.transform: the wiki index (omoikane/bin/session-context.py) is added to the system
 *   prompt; computed once per session, like Claude Code's SessionStart.
 * - session idle (once per prompt) and dispose (process exit): the session is fetched through the SDK, written as
 *   the `opencode export` document and captured into omoikane/raw/inbox/sessions/
 *   (omoikane/bin/session-capture.py --harness opencode), like Claude Code's Stop and SessionEnd.
 * - command.executed: remembers the first slash command of each session; session-capture.py skips sessions that
 *   start with an Omoikane operation (/ingest, /distill, /ask, /lint), the guard Claude Code applies from its transcript.
 *
 * Both scripts print one line and exit 0 on any failure, and do nothing when OMOIKANE_NO_CAPTURE is set, so this
 * file needs no error handling of its own. OpenCode loads .opencode/plugins/*.ts and installs @opencode-ai/plugin
 * next to it for the types (https://opencode.ai/docs/plugins). Events reach a plugin only for its own directory.
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import type { Plugin } from "@opencode-ai/plugin";

export const OmoikanePlugin: Plugin = async ({ client, directory, $ }) => {
	const capture = join(directory, "omoikane", "bin", "session-capture.py");
	const context = join(directory, "omoikane", "bin", "session-context.py");
	const firstCommand = new Map<string, string>();
	const indexBySession = new Map<string, string>();
	// Event handlers are fire-and-forget: `opencode run` exits right after the session goes idle, so dispose
	// awaits the capture still in flight (or starts one for a session that never reached idle).
	const inFlight = new Map<string, Promise<void>>();
	const touched = new Set<string>();

	async function exportAndCapture(sessionID: string): Promise<void> {
		const session = await client.session.get({ path: { id: sessionID } });
		const messages = await client.session.messages({ path: { id: sessionID } });
		if (!session.data || !messages.data) return;
		const dir = join(tmpdir(), "omoikane");
		mkdirSync(dir, { recursive: true });
		const file = join(dir, `${sessionID}.json`);
		writeFileSync(file, JSON.stringify({ info: session.data, messages: messages.data }));
		const args = ["--harness", "opencode", "--transcript", file, "--session-id", sessionID];
		const command = firstCommand.get(sessionID);
		if (command) args.push("--first-command", `/${command}`);
		await $`python ${capture} ${args}`.cwd(directory).quiet().nothrow();
	}

	function captureSession(sessionID: string): Promise<void> {
		const pending = inFlight.get(sessionID);
		if (pending) return pending;
		const run = exportAndCapture(sessionID).finally(() => inFlight.delete(sessionID));
		inFlight.set(sessionID, run);
		return run;
	}

	return {
		event: async ({ event }) => {
			if (event.type === "command.executed" && !firstCommand.has(event.properties.sessionID)) {
				firstCommand.set(event.properties.sessionID, event.properties.name);
			}
			if (event.type === "message.updated") touched.add(event.properties.info.sessionID);
			// session.idle is the documented event; session.status {type: "idle"} is its successor in the SDK types.
			// Either one triggers a capture; a capture already in flight for the session is reused, not duplicated.
			if (event.type === "session.idle") await captureSession(event.properties.sessionID);
			if (event.type === "session.status" && event.properties.status.type === "idle") {
				await captureSession(event.properties.sessionID);
			}
		},
		dispose: async () => {
			await Promise.all([...touched].map(captureSession));
		},
		"experimental.chat.system.transform": async (input, output) => {
			const key = input.sessionID ?? "";
			if (!indexBySession.has(key)) {
				const result = await $`python ${context}`.cwd(directory).quiet().nothrow();
				indexBySession.set(key, result.exitCode === 0 ? result.text().trim() : "");
			}
			const index = indexBySession.get(key);
			if (index) output.system.push(index);
		},
	};
};
