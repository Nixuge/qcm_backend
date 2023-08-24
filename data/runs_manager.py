from data.types.run import Run


class RunsManager:
    # dict for easier access
    runs: dict[str, Run] = {}

    @staticmethod
    def add_run(run: Run):
        RunsManager.runs[run.uuid] = run
    
    @staticmethod
    def get_run(uuid: str):
        return RunsManager.runs.get(uuid)