from data.types.run import Run


class RunsManager:
    runs: list[Run] = []

    @staticmethod
    def add_run(run: Run):
        RunsManager.runs.append(run)