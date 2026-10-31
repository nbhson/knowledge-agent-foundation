export interface Plugin<C = any> {
  name: string;
  apply(ctx: Context, config?: C): void | Promise<void>;
}
