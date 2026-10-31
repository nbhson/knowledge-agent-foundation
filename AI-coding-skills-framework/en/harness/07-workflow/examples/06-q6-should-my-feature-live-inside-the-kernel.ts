const GitPlugin = {
  name: 'git',
  provides: 'git',
  apply(ctx: Context) {
    ctx.provide('git', { log: () => run('git log') });
    ctx.onDispose(() => console.log('[git] released'));  // removable again
  },
};
