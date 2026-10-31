const SECRET_ENV = /^(AWS_|AZURE_|GCP_|GH_|GITHUB_|OPENAI_|ANTHROPIC_|SK-|BEARER_|NPM_TOKEN_)/i;
for (const k of Object.keys(env)) if (SECRET_ENV.test(k)) throw new SandboxError(`secret-env-denied:${k}`);
