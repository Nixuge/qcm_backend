from data.types.run import Run


class RunsManager:
    # dict for easier access
    runs: dict[str, Run] = {}

    @classmethod
    def add_run(cls, run: Run):
        cls.runs[run.uuid] = run
    
    @classmethod
    def get_run(cls, uuid: str):
        return cls.runs.get(uuid)

    @classmethod
    def remove_save_run(cls, uuid: str):
        cls.runs.pop(uuid).save_to_disk()
        