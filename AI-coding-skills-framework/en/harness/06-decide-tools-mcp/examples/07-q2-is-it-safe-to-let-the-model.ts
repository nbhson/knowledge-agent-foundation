const wrapped = `(async () => { ${code} })();`;
const script = new vm.Script(wrapped);
await script.runInContext(vm.createContext(sandboxContext), { timeout: timeoutMs });
