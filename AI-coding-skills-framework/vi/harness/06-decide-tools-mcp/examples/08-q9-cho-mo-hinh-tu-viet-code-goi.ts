const ctx = vm.createContext({ dsh: this.sdk, console, setTimeout });
const s = new vm.Script(`(async () => { ${code} })();`);
return s.runInContext(ctx, { timeout: 30000 });
