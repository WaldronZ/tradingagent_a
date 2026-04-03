from tradingagents.data_tools.executor import CachedDataToolExecutor
from tradingagents.data_tools.types import DataCollectionJob, ToolExecutionResult


class DataCollectionService:
    """独立运行数据采集任务并将结果沉淀到本地。"""

    def __init__(self, executor: CachedDataToolExecutor):
        """
        初始化数据采集服务。

        参数：
            executor: 数据工具执行器。

        返回：
            None: 无返回值。
        """
        self.executor = executor

    def collect(self, job: DataCollectionJob) -> ToolExecutionResult:
        """
        执行单个数据采集任务。

        参数：
            job: 数据采集任务定义。

        返回：
            ToolExecutionResult: 工具执行结果对象。
        """
        return self.executor.execute(
            job.tool_name,
            use_cache=job.use_cache,
            persist_snapshot=True,
            snapshot_group=job.snapshot_group,
            snapshot_date=job.snapshot_date,
            **job.params,
        )

    def collect_many(self, jobs: list[DataCollectionJob]) -> list[ToolExecutionResult]:
        """
        批量执行数据采集任务。

        参数：
            jobs: 数据采集任务列表。

        返回：
            list[ToolExecutionResult]: 工具执行结果列表。
        """
        return [self.collect(job) for job in jobs]
