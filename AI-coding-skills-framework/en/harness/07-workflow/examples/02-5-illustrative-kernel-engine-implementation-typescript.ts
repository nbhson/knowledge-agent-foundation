export class Context {
  public services: Map<string, any> = new Map();
  private events: Map<string, Function[]> = new Map();

  // Register a Service in the Kernel
  public provide(name: string, service: any) {
    this.services.set(name, service);
  }

  // Fetch a Service for use
  public inject<T>(name: string): T {
    const service = this.services.get(name);
    if (!service) throw new Error(`Service ${name} not found in Kernel Context`);
    return service as T;
  }

  // Event System for Middleware
  public on(event: string, handler: Function) {
    const handlers = this.events.get(event) || [];
    handlers.push(handler);
    this.events.set(event, handlers);
  }

  public async emit(event: string, ...args: any[]) {
    const handlers = this.events.get(event) || [];
    for (const handler of handlers) {
      await handler(...args);
    }
  }

  // Load a Plugin
  public plugin(plugin: { name: string; apply: (ctx: Context) => void }) {
    console.log(`[Kernel] Mounting Plugin: ${plugin.name}`);
    plugin.apply(this);
  }
}
