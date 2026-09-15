/**
 * Omoikane session hooks for Pi, the counterpart of .claude/settings.json.
 *
 * - session_start / before_agent_start: the wiki index (omoikane/bin/session-context.py) is appended to the
 *   system prompt of every prompt in the session; computed once per session, like Claude Code's SessionStart.
 * - agent_end / session_shutdown: the session file is captured into omoikane/raw/inbox/sessions/
 *   (omoikane/bin/session-capture.py --harness pi), like Claude Code's Stop and SessionEnd.
 *
 * Both scripts print one line and exit 0 on any failure, and do nothing when OMOIKANE_NO_CAPTURE is set, so
 * this file needs no error handling of its own. Pi loads .pi/extensions/*.ts once the project is trusted
 * (docs/extensions.md of @earendil-works/pi-coding-agent, "Extension Locations").
 */
import { join } from "node:path";
import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";

const CAPTURE = join("omoikane", "bin", "session-capture.py");
const CONTEXT = join("omoikane", "bin", "session-context.py");

export default function omoikane(pi: ExtensionAPI) {
	let firstCommand = "";
	let index: string | undefined;

	async function capture(ctx: ExtensionContext): Promise<void> {
		const file = ctx.sessionManager.getSessionFile();
		if (!file) return; // --no-session: nothing on disk to read
		const args = [join(ctx.cwd, CAPTURE), "--harness", "pi", "--transcript", file, "--session-id", ctx.sessionManager.getSessionId()];
		if (firstCommand) args.push("--first-command", firstCommand);
		await pi.exec("python", args, { cwd: ctx.cwd, timeout: 15_000 });
	}

	pi.on("session_start", async () => {
		firstCommand = "";
		index = undefined;
	});

	// Records the first slash command of the session: session-capture.py skips sessions that start with an
	// Omoikane operation (/ingest, /distill, /ask, /lint), the same guard Claude Code applies from its transcript.
	pi.on("input", async (event) => {
		const text = event.text.trim();
		if (!firstCommand && text.startsWith("/")) firstCommand = text.split(/\s+/)[0];
	});

	pi.on("before_agent_start", async (event, ctx) => {
		if (index === undefined) {
			const result = await pi.exec("python", [join(ctx.cwd, CONTEXT)], { cwd: ctx.cwd, timeout: 10_000 });
			index = result.code === 0 ? result.stdout.trim() : "";
		}
		if (!index) return;
		return { systemPrompt: `${event.systemPrompt}\n\n${index}` };
	});

	pi.on("agent_end", async (_event, ctx) => capture(ctx));
	pi.on("session_shutdown", async (_event, ctx) => capture(ctx));
}
