import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

class ParallelWorkflow:
    """Workflow chạy song song — nhiều bước cùng lúc"""
    
    def __init__(self, name: str = "parallel", max_workers: int = 4):
        self.name = name
        self.parallel_groups = []
        self.max_workers = max_workers
        self.history = []
    
    def add_parallel_group(self, steps):
        """
        Thêm một nhóm các bước chạy song song.
        steps: list of (name, func, args_dict)
        """
        self.parallel_groups.append({"type": "parallel", "steps": steps})
        return self
    
    def add_sequential_step(self, name: str, func: Callable):
        self.parallel_groups.append({
            "type": "sequential",
            "steps": [(name, func, {})],
        })
        return self
    
    def run(self, initial_input: Any) -> Any:
        current_input = initial_input
        
        for group_idx, group in enumerate(self.parallel_groups):
            if group["type"] == "sequential":
                name, func, args = group["steps"][0]
                current_input = func(current_input, **args)
            else:
                # Parallel group
                results = {}
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = {}
                    for name, func, args in group["steps"]:
                        future = executor.submit(func, current_input, **args)
                        futures[future] = name
                    
                    for future in as_completed(futures):
                        name = futures[future]
                        try:
                            results[name] = future.result()
                        except Exception as e:
                            results[name] = {"error": str(e)}
                
                current_input = results
        
        return current_input
    
    def run_async(self, initial_input: Any) -> Any:
        """Async version for I/O-bound workflows"""
        return asyncio.run(self._run_async_impl(initial_input))
    
    async def _run_async_impl(self, initial_input: Any) -> Any:
        current_input = initial_input
        
        for group in self.parallel_groups:
            if group["type"] == "sequential":
                name, func, args = group["steps"][0]
                if asyncio.iscoroutinefunction(func):
                    current_input = await func(current_input, **args)
                else:
                    current_input = func(current_input, **args)
            else:
                tasks = []
                for name, func, args in group["steps"]:
                    if asyncio.iscoroutinefunction(func):
                        tasks.append(func(current_input, **args))
                    else:
                        loop = asyncio.get_event_loop()
                        tasks.append(loop.run_in_executor(None, func, current_input, **args))
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                current_input = {
                    group["steps"][i][0]: r 
                    for i, r in enumerate(results)
                }
        
        return current_input
