# Hosting and Deployment Adapters

Deployment is an optional phase, never an assumption. Detect the active model from repository files, provider metadata, authenticated CLI state, deployment documentation, and the production response. If identity or scope is ambiguous, do not deploy.

## Detection matrix

| Model | Detection evidence | Scoped activation evidence |
|---|---|---|
| VPS + Nginx + PM2 | SSH target, Nginx site file, web root, PM2/systemd process, deployment docs | exact root, site file, process name, ports, backup, health checks |
| Cloudflare Pages | `wrangler` config, Pages project metadata, `pages.dev` host, Pages dashboard | account/project ID, build output, production branch/environment |
| Cloudflare Workers | Worker entrypoint, `wrangler.jsonc`/`wrangler.toml`, Worker route, bindings | account, Worker name/environment, bindings, compatibility settings |
| Vercel | `vercel.json`, `.vercel/project.json`, Vercel metadata, `vercel.app` host | team/project, environment, preview/prod target, deployment URL |
| Netlify | `netlify.toml`, Netlify metadata, `netlify.app` host, build settings | site ID, context, publish directory, deployment URL |
| Static hosting | artifact directory, object-storage/CDN config, static host | exact bucket/site/root and immutable artifact hash |
| Docker/reverse proxy | Dockerfile/Compose, container name, proxy config, healthcheck | exact service/container, image tag, proxy route, rollback image |
| GitHub Pages | Pages workflow/config, repository Pages metadata, `github.io` host | repository/site, artifact, workflow/environment, custom domain |
| Browser-only control panel | no safe CLI/API, authenticated browser context, documented panel | exact account/project/control-panel target and visible deployment result |

A matching filename is not proof of the active target. Compare it with the production domain, provider project metadata, and deployment history where available.

## Universal release rules

1. Read repository deployment documentation and provider configuration before acting.
2. Build and validate locally before uploading or activating.
3. Create a scoped release artifact with a manifest, file list, and SHA-256 hashes.
4. Validate project/provider identity and environment before activation.
5. Prefer a preview, staging, immutable release, or provider rollback target before production activation.
6. Keep a previous release/configuration reference and an executable rollback action.
7. Activate only after configuration and health gates pass.
8. Verify the exact production URL and response matrix after activation.
9. Do not push Git by default. Deployment and Git publication are separate actions.
10. Never print credentials, tokens, cookies, private keys, or authorization headers.
11. Roll back automatically when activation or health gates fail and the previous scoped release is available.

## VPS + Nginx + PM2 procedure

Use this adapter only after confirming the exact project scope from deployment documentation and the live domain.

1. Identify the exact web root, Nginx site/server block, upstream/port, PM2 process name or systemd unit, and API health endpoint. Record them in the manifest.
2. Inspect neighboring roots, processes, ports, and site files to establish a no-touch boundary. Do not change them.
3. Build locally. Package only the requested project output and required configuration. Exclude credentials, `.env` files, dependencies, caches, and unrelated files.
4. Create a temporary release directory under the scoped project root. Transfer in a throttled or chunked manner when the connection or archive size requires it. Verify local and remote SHA-256 hashes before extraction/activation.
5. Back up only the scoped Nginx site configuration, active release pointer, and project configuration needed for rollback. Do not back up or rewrite the whole server configuration.
6. Extract and inspect the temporary release. Validate ownership/permissions, expected assets, runtime configuration, and the project health check.
7. Run `nginx -t` before reload. Do not reload when syntax validation fails.
8. Activate the new release using the existing project-scoped pointer/alias or documented copy strategy. Reload Nginx only after the syntax gate passes.
9. Check the exact PM2/systemd process, API health, public HTTP status, redirects, response headers, and representative page output.
10. If activation or health checks fail, restore the previous release/configuration, run `nginx -t` again, reload only after it passes, and verify the old release. Record the rollback result.

`nginx -t` is a syntax and referenced-file preflight, not proof that the application is healthy. Process health, API health, and public HTTP verification are separate gates.

## Provider adapters

### Cloudflare Pages

Resolve the account and Pages project before deployment. Confirm whether the project is Git-integrated or direct-upload; do not change that model implicitly. Validate the build output and production/preview environment. Use the installed Wrangler version and current provider documentation; a direct upload is scoped to the exact Pages project and output directory. Verify the deployment URL and custom domain after activation.

### Cloudflare Workers

Resolve the Worker name, environment, routes, bindings, compatibility settings, and account. Run the project-native build/typecheck and a provider dry-run or equivalent validation before activation. Deploy only the requested Worker/environment. Verify route behavior, bindings-backed health, and the production URL after activation.

### Vercel

Resolve team/project/environment from `.vercel/project.json`, provider metadata, or an authenticated CLI. Prefer a preview deployment and validate it before production promotion when the request permits. Use production deployment only when authorized; a Git push is not a substitute for a requested deployment. Verify the deployment URL, custom domain, server functions, headers, and response matrix.

### Netlify

Resolve the site ID, context, build command, publish directory, redirects/headers configuration, and deploy URL. Validate the exact artifact and preview/context before production activation where supported. Verify redirects, headers, functions, assets, and production response behavior.

### Static hosting

Treat the built directory as the release artifact. Generate a file manifest and hashes, transfer only that artifact to the scoped root/bucket, preserve the previous version, and verify the CDN/custom domain. Do not rewrite unrelated bucket prefixes or CDN distributions.

### Docker/reverse proxy

Resolve the exact Compose/service/container and reverse-proxy route. Build/tag an immutable image or artifact, run the existing healthcheck, and deploy only that service. Preserve the prior image/tag and proxy configuration. Verify the container, upstream, public route, headers, and rollback path.

### GitHub Pages

Resolve the exact repository, Pages source, workflow, artifact path, and custom domain. Do not push or merge unless explicitly requested. If a workflow is the deployment mechanism, report that deployment is blocked by `no-push`/`no-merge` rather than mutating Git to trigger it. Verify the published site separately.

### Browser-only control panels

Use an authenticated browser session only for the requested in-scope project action. Confirm account, project, environment, and deployment target from visible UI. Do not copy credentials or persistent browser state into files or logs. Complete routine clicks the skill can safely perform; stop only when the panel requires a human judgment, a credential not present in the session, or an irreversible confirmation outside the authorized scope.

## Failure and rollback states

Use explicit states: `not-detected`, `detected-not-authorized`, `preflight-failed`, `released-not-activated`, `activated-health-failed`, `rolled-back`, `deployed-verified`, and `deployed-unverified`. Never report `deployed-verified` from a successful upload alone.
